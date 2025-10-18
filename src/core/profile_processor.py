"""
Profile Processor Module
Handles profile data loading, validation, and processing for TOPSIS evaluation
Author: Abdel YEZZA (Ph.D) - Combined System
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path

from .skill_transformer import SkillTransformer, WeightGenerator
from .topsis_engine import TopsisEngine


class ProfileProcessor:
    """
    Main processor for profile-based TOPSIS evaluation.
    Integrates profile data, activity requirements, and TOPSIS ranking.
    """

    def __init__(
        self,
        profiles_df: pd.DataFrame,
        activities_df: pd.DataFrame,
        threshold: float = 3.0,
        min_threshold: float = 0.0,
        max_threshold: float = 5.0,
        proximity_formula: str = "standard"
    ):
        """
        Initialize profile processor.

        Args:
            profiles_df: DataFrame with profiles (rows) and skills (columns)
            activities_df: DataFrame with activities (rows) and required skill levels (columns)
            threshold: Skill level threshold for determining criterion type
            min_threshold: Minimum possible skill level
            max_threshold: Maximum possible skill level
            proximity_formula: TOPSIS proximity formula ("standard" or "variant")
        """
        self.profiles_df = profiles_df.copy()
        self.activities_df = activities_df.copy()
        self.threshold = threshold
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.proximity_formula = proximity_formula

        # Initialize skill transformer
        self.skill_transformer = SkillTransformer(
            threshold=threshold,
            min_threshold=min_threshold,
            max_threshold=max_threshold
        )

        # Extract profile and activity names
        self.profile_names = self.profiles_df.index.tolist()
        self.activity_names = self.activities_df.index.tolist()

        # Validate data
        self._validate_data()

        # Storage for results
        self.results = {}

    def _validate_data(self):
        """Validate input data consistency."""
        # Check that skill columns match
        profile_skills = set(self.profiles_df.columns)
        activity_skills = set(self.activities_df.columns)

        if profile_skills != activity_skills:
            missing_in_activities = profile_skills - activity_skills
            missing_in_profiles = activity_skills - profile_skills

            error_msg = "Skill columns must match between profiles and activities.\n"
            if missing_in_activities:
                error_msg += f"Missing in activities: {missing_in_activities}\n"
            if missing_in_profiles:
                error_msg += f"Missing in profiles: {missing_in_profiles}\n"

            raise ValueError(error_msg)

        # Check for numeric values
        if not all(self.profiles_df.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
            raise ValueError("All profile skill values must be numeric")

        if not all(self.activities_df.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
            raise ValueError("All activity skill values must be numeric")

        # Validate skill level ranges
        is_valid, msg = self.skill_transformer.validate_skill_levels(self.profiles_df.values)
        if not is_valid:
            raise ValueError(f"Profile data validation failed: {msg}")

        is_valid, msg = self.skill_transformer.validate_skill_levels(self.activities_df.values)
        if not is_valid:
            raise ValueError(f"Activity data validation failed: {msg}")

    def process_activity(
        self,
        activity_name: str,
        weights: Optional[np.ndarray] = None,
        weight_strategy: str = "uniform",
        verbose: bool = False
    ) -> Dict:
        """
        Process a single activity: rank profiles using TOPSIS.

        Args:
            activity_name: Name of the activity
            weights: Custom weights for skills (optional)
            weight_strategy: Strategy for weight generation if weights not provided
                           ("uniform", "requirement_based")
            verbose: If True, print detailed information

        Returns:
            Dictionary with ranking results
        """
        if activity_name not in self.activity_names:
            raise ValueError(f"Activity '{activity_name}' not found in activities data")

        # Get required skill levels for this activity
        required_skills = self.activities_df.loc[activity_name].values
        skill_names = self.activities_df.columns.tolist()

        # Determine criteria types based on threshold
        criteria_types = self.skill_transformer.determine_criteria_types(required_skills)

        # Generate weights if not provided
        if weights is None:
            if weight_strategy == "uniform":
                weights = WeightGenerator.uniform_weights(len(skill_names))
            elif weight_strategy == "requirement_based":
                weights = WeightGenerator.requirement_based_weights(required_skills, self.threshold)
            else:
                raise ValueError(f"Unknown weight strategy: {weight_strategy}")

        if verbose:
            print(f"\n{'='*80}")
            print(f"Processing Activity: {activity_name}")
            print(f"{'='*80}")
            self.skill_transformer.print_criteria_analysis(skill_names, required_skills)
            print(f"\nWeights Strategy: {weight_strategy}")
            print(f"Weights: {weights}")

        # Get profile skill matrix
        decision_matrix = self.profiles_df.values

        # Create TOPSIS engine
        topsis = TopsisEngine(
            decision_matrix=decision_matrix,
            weights=weights,
            criteria_types=criteria_types,
            alternative_names=self.profile_names,
            criteria_names=skill_names,
            proximity_formula=self.proximity_formula
        )

        # Calculate TOPSIS
        topsis.calculate(verbose=verbose)

        # Get results
        results = topsis.get_results_dict()
        results['activity_name'] = activity_name
        results['required_skills'] = required_skills.tolist()
        results['criteria_types'] = criteria_types.tolist()
        results['weight_strategy'] = weight_strategy

        # Store results
        self.results[activity_name] = results

        return results

    def process_all_activities(
        self,
        weights: Optional[np.ndarray] = None,
        weight_strategy: str = "uniform",
        verbose: bool = False
    ) -> Dict[str, Dict]:
        """
        Process all activities and rank profiles for each.

        Args:
            weights: Custom weights for skills (optional, applied to all activities)
            weight_strategy: Strategy for weight generation
            verbose: If True, print detailed information

        Returns:
            Dictionary mapping activity names to ranking results
        """
        all_results = {}

        for activity_name in self.activity_names:
            if verbose:
                print(f"\n\n{'#'*80}")
                print(f"# Processing Activity {self.activity_names.index(activity_name) + 1}/{len(self.activity_names)}")
                print(f"{'#'*80}")

            results = self.process_activity(
                activity_name=activity_name,
                weights=weights,
                weight_strategy=weight_strategy,
                verbose=verbose
            )

            all_results[activity_name] = results

        return all_results

    def get_ranking_matrix(self, top_n: int = 3) -> pd.DataFrame:
        """
        Generate ranking matrix showing top N profiles for each activity.

        Args:
            top_n: Number of top profiles to include

        Returns:
            DataFrame with ranking matrix
        """
        if not self.results:
            raise ValueError("No results available. Run process_all_activities() first.")

        ranking_data = []

        for activity_name, results in self.results.items():
            row = {'Activity': activity_name}

            for i in range(min(top_n, len(results['ranked_results']))):
                rank = i + 1
                result = results['ranked_results'][i]
                row[f'Rank {rank}'] = f"{result['alternative']} ({result['coefficient']:.4f})"

            ranking_data.append(row)

        return pd.DataFrame(ranking_data)

    def get_full_results_matrix(self) -> pd.DataFrame:
        """
        Generate full results matrix with all profiles for all activities.

        Returns:
            DataFrame with activities as rows and profiles as columns
        """
        if not self.results:
            raise ValueError("No results available. Run process_all_activities() first.")

        results_data = {}

        for activity_name, results in self.results.items():
            row = {}
            for result in results['ranked_results']:
                profile_name = result['alternative']
                row[profile_name] = result['coefficient']

            results_data[activity_name] = row

        return pd.DataFrame(results_data).T

    def save_results(self, output_dir: Path):
        """
        Save all results to files.

        Args:
            output_dir: Directory to save results
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        rankings_dir = output_dir / "rankings"
        rankings_dir.mkdir(exist_ok=True)

        # Save ranking matrix
        ranking_matrix = self.get_ranking_matrix(top_n=3)
        ranking_matrix.to_csv(rankings_dir / "ranking_matrix.csv", index=False)

        # Save full results matrix
        full_results = self.get_full_results_matrix()
        full_results.to_csv(rankings_dir / "full_results_matrix.csv")

        # Save detailed results for each activity
        for activity_name, results in self.results.items():
            safe_name = activity_name.replace(' ', '_').replace('/', '_')
            with open(rankings_dir / f"ranking_{safe_name}.txt", 'w') as f:
                f.write(f"{'='*80}\n")
                f.write(f"Activity: {activity_name}\n")
                f.write(f"{'='*80}\n\n")

                f.write(f"Best Profile: {results['best_alternative']}\n")
                f.write(f"Best Coefficient: {results['best_coefficient']:.6f} ({results['best_coefficient']*100:.2f}%)\n\n")

                f.write(f"Complete Ranking:\n")
                f.write(f"{'-'*80}\n")
                f.write(f"{'Rank':<6} {'Profile':<30} {'Coefficient':<15} {'Percentage':<15}\n")
                f.write(f"{'-'*80}\n")

                for result in results['ranked_results']:
                    f.write(f"{result['rank']:<6} {result['alternative']:<30} "
                           f"{result['coefficient']:<15.6f} {result['percentage']:<15.2f}%\n")

        print(f"\nResults saved to: {output_dir}")
        print(f"  - Ranking matrix: {rankings_dir / 'ranking_matrix.csv'}")
        print(f"  - Full results: {rankings_dir / 'full_results_matrix.csv'}")
        print(f"  - Detailed rankings: {rankings_dir / 'ranking_*.txt'}")

    def print_summary(self):
        """Print summary of all results."""
        if not self.results:
            print("No results available. Run process_all_activities() first.")
            return

        print("\n" + "="*80)
        print("PROFILE SELECTION SUMMARY - TOPSIS Results")
        print("="*80)
        print(f"\nConfiguration:")
        print(f"  Threshold: {self.threshold}")
        print(f"  Skill Range: [{self.min_threshold}, {self.max_threshold}]")
        print(f"  Proximity Formula: {self.proximity_formula}")
        print(f"  Total Profiles: {len(self.profile_names)}")
        print(f"  Total Activities: {len(self.activity_names)}")
        print(f"  Total Skills: {len(self.profiles_df.columns)}")

        print("\n" + "="*80)
        print("Best Profile for Each Activity")
        print("="*80)
        print(f"{'Activity':<30} {'Best Profile':<30} {'Coefficient':<15}")
        print("-"*80)

        for activity_name, results in self.results.items():
            print(f"{activity_name:<30} {results['best_alternative']:<30} "
                  f"{results['best_coefficient']:<15.6f}")

        print("="*80)


def load_profiles_from_csv(file_path: Path) -> pd.DataFrame:
    """
    Load profiles from CSV file.

    Expected format:
    Profile,Skill1,Skill2,Skill3,...
    Profile1,4,5,3,...
    Profile2,3,4,5,...

    Args:
        file_path: Path to CSV file

    Returns:
        DataFrame with profiles as index
    """
    df = pd.read_csv(file_path, index_col=0)
    return df


def load_activities_from_csv(file_path: Path) -> pd.DataFrame:
    """
    Load activities from CSV file.

    Expected format:
    Activity,Skill1,Skill2,Skill3,...
    Activity1,4,5,3,...
    Activity2,3,4,5,...

    Args:
        file_path: Path to CSV file

    Returns:
        DataFrame with activities as index
    """
    df = pd.read_csv(file_path, index_col=0)
    return df
