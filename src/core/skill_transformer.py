"""
Skill Transformer Module
Transforms skill levels into TOPSIS criteria types based on configurable threshold
Author: Abdel YEZZA (Ph.D) - Combined System
"""

import numpy as np
from typing import Dict, List, Tuple


class SkillTransformer:
    """
    Transforms skill requirement levels into TOPSIS criteria types.

    Rules:
    - If required skill level >= threshold: Beneficial criterion (higher is better)
    - If required skill level < threshold: Non-beneficial criterion (lower is acceptable)
    """

    def __init__(
        self,
        threshold: float = 3.0,
        min_threshold: float = 0.0,
        max_threshold: float = 5.0
    ):
        """
        Initialize skill transformer.

        Args:
            threshold: Skill level threshold for determining criterion type
            min_threshold: Minimum possible skill level
            max_threshold: Maximum possible skill level
        """
        self.threshold = threshold
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

        # Validate threshold
        self._validate_threshold()

    def _validate_threshold(self):
        """Validate threshold is within valid range."""
        if not (self.min_threshold <= self.threshold <= self.max_threshold):
            raise ValueError(
                f"Threshold {self.threshold} must be between "
                f"min_threshold {self.min_threshold} and max_threshold {self.max_threshold}"
            )

    def determine_criteria_types(
        self,
        required_skill_levels: np.ndarray
    ) -> np.ndarray:
        """
        Determine TOPSIS criteria types based on required skill levels.

        Args:
            required_skill_levels: Array of required skill levels for an activity

        Returns:
            Array of criteria types (1=beneficial, 0=non-beneficial)
        """
        criteria_types = np.zeros(len(required_skill_levels), dtype=int)

        for i, skill_level in enumerate(required_skill_levels):
            if skill_level >= self.threshold:
                criteria_types[i] = 1  # Beneficial (maximize)
            else:
                criteria_types[i] = 0  # Non-beneficial (minimize)

        return criteria_types

    def get_criteria_info(
        self,
        skill_names: List[str],
        required_skill_levels: np.ndarray
    ) -> List[Dict]:
        """
        Get detailed information about each criterion.

        Args:
            skill_names: List of skill names
            required_skill_levels: Array of required skill levels

        Returns:
            List of dictionaries with criterion information
        """
        criteria_types = self.determine_criteria_types(required_skill_levels)
        criteria_info = []

        for i, (name, level, ctype) in enumerate(zip(skill_names, required_skill_levels, criteria_types)):
            criteria_info.append({
                'skill_name': name,
                'required_level': float(level),
                'criterion_type': int(ctype),
                'criterion_type_label': 'Beneficial (Maximize)' if ctype == 1 else 'Non-Beneficial (Minimize)',
                'reasoning': self._get_reasoning(level, ctype)
            })

        return criteria_info

    def _get_reasoning(self, skill_level: float, criterion_type: int) -> str:
        """
        Get human-readable reasoning for criterion type assignment.

        Args:
            skill_level: Required skill level
            criterion_type: Assigned criterion type

        Returns:
            Reasoning string
        """
        if criterion_type == 1:
            return (f"Required level {skill_level} >= threshold {self.threshold}: "
                   f"Higher skill levels are preferred")
        else:
            return (f"Required level {skill_level} < threshold {self.threshold}: "
                   f"Lower skill levels are acceptable")

    def validate_skill_levels(
        self,
        skill_matrix: np.ndarray
    ) -> Tuple[bool, str]:
        """
        Validate that skill levels are within acceptable range.

        Args:
            skill_matrix: Matrix of skill levels

        Returns:
            Tuple of (is_valid, message)
        """
        min_val = np.min(skill_matrix)
        max_val = np.max(skill_matrix)

        if min_val < self.min_threshold:
            return False, (f"Minimum skill level {min_val} is below "
                          f"min_threshold {self.min_threshold}")

        if max_val > self.max_threshold:
            return False, (f"Maximum skill level {max_val} exceeds "
                          f"max_threshold {self.max_threshold}")

        return True, "All skill levels are within valid range"

    def get_threshold_info(self) -> Dict:
        """
        Get information about current threshold configuration.

        Returns:
            Dictionary with threshold information
        """
        return {
            'threshold': self.threshold,
            'min_threshold': self.min_threshold,
            'max_threshold': self.max_threshold,
            'beneficial_range': f'>= {self.threshold}',
            'non_beneficial_range': f'< {self.threshold}'
        }

    def set_threshold(self, new_threshold: float):
        """
        Update the threshold value.

        Args:
            new_threshold: New threshold value
        """
        self.threshold = new_threshold
        self._validate_threshold()

    def analyze_activity_requirements(
        self,
        skill_names: List[str],
        required_skill_levels: np.ndarray
    ) -> Dict:
        """
        Analyze activity requirements and provide summary statistics.

        Args:
            skill_names: List of skill names
            required_skill_levels: Array of required skill levels

        Returns:
            Dictionary with analysis results
        """
        criteria_types = self.determine_criteria_types(required_skill_levels)
        n_beneficial = np.sum(criteria_types == 1)
        n_non_beneficial = np.sum(criteria_types == 0)

        beneficial_skills = [skill_names[i] for i in range(len(skill_names))
                            if criteria_types[i] == 1]
        non_beneficial_skills = [skill_names[i] for i in range(len(skill_names))
                                if criteria_types[i] == 0]

        return {
            'total_skills': len(skill_names),
            'n_beneficial': n_beneficial,
            'n_non_beneficial': n_non_beneficial,
            'percentage_beneficial': (n_beneficial / len(skill_names)) * 100,
            'percentage_non_beneficial': (n_non_beneficial / len(skill_names)) * 100,
            'beneficial_skills': beneficial_skills,
            'non_beneficial_skills': non_beneficial_skills,
            'avg_required_level': float(np.mean(required_skill_levels)),
            'max_required_level': float(np.max(required_skill_levels)),
            'min_required_level': float(np.min(required_skill_levels)),
            'threshold_used': self.threshold
        }

    def print_criteria_analysis(
        self,
        skill_names: List[str],
        required_skill_levels: np.ndarray
    ):
        """
        Print detailed analysis of criteria types for an activity.

        Args:
            skill_names: List of skill names
            required_skill_levels: Array of required skill levels
        """
        print("\n" + "="*80)
        print("SKILL CRITERIA ANALYSIS")
        print("="*80)
        print(f"\nThreshold Configuration:")
        print(f"  Current Threshold: {self.threshold}")
        print(f"  Range: [{self.min_threshold}, {self.max_threshold}]")
        print(f"  Beneficial (Maximize): >= {self.threshold}")
        print(f"  Non-Beneficial (Minimize): < {self.threshold}")

        criteria_info = self.get_criteria_info(skill_names, required_skill_levels)

        print(f"\nSkill Requirements & Criteria Types:")
        print("-" * 80)
        print(f"{'Skill':<20} {'Required Level':<15} {'Type':<25} {'Reasoning'}")
        print("-" * 80)

        for info in criteria_info:
            print(f"{info['skill_name']:<20} {info['required_level']:<15.1f} "
                  f"{info['criterion_type_label']:<25} {info['reasoning']}")

        analysis = self.analyze_activity_requirements(skill_names, required_skill_levels)
        print(f"\nSummary Statistics:")
        print("-" * 80)
        print(f"  Total Skills: {analysis['total_skills']}")
        print(f"  Beneficial Skills: {analysis['n_beneficial']} ({analysis['percentage_beneficial']:.1f}%)")
        print(f"  Non-Beneficial Skills: {analysis['n_non_beneficial']} ({analysis['percentage_non_beneficial']:.1f}%)")
        print(f"  Average Required Level: {analysis['avg_required_level']:.2f}")
        print(f"  Range: [{analysis['min_required_level']:.1f}, {analysis['max_required_level']:.1f}]")
        print("="*80)


class WeightGenerator:
    """
    Generate weights for skills based on various strategies.
    """

    @staticmethod
    def uniform_weights(n_criteria: int) -> np.ndarray:
        """
        Generate uniform weights (all equal).

        Args:
            n_criteria: Number of criteria

        Returns:
            Array of uniform weights
        """
        return np.ones(n_criteria) / n_criteria

    @staticmethod
    def importance_based_weights(
        importance_scores: List[float]
    ) -> np.ndarray:
        """
        Generate weights based on importance scores.

        Args:
            importance_scores: List of importance scores for each criterion

        Returns:
            Normalized weights
        """
        weights = np.array(importance_scores, dtype=float)
        return weights / np.sum(weights)

    @staticmethod
    def requirement_based_weights(
        required_levels: np.ndarray,
        threshold: float
    ) -> np.ndarray:
        """
        Generate weights based on required skill levels.
        Higher required levels get higher weights.

        Args:
            required_levels: Array of required skill levels
            threshold: Threshold value

        Returns:
            Normalized weights
        """
        # Weight proportional to required level
        weights = required_levels.copy()
        weights = np.maximum(weights, 0.1)  # Minimum weight of 0.1
        return weights / np.sum(weights)

    @staticmethod
    def hybrid_weights(
        required_levels: np.ndarray,
        importance_scores: List[float],
        alpha: float = 0.5
    ) -> np.ndarray:
        """
        Generate hybrid weights combining requirement levels and importance.

        Args:
            required_levels: Array of required skill levels
            importance_scores: List of importance scores
            alpha: Balance factor (0=all importance, 1=all requirement)

        Returns:
            Normalized weights
        """
        req_weights = required_levels / np.sum(required_levels)
        imp_weights = np.array(importance_scores) / np.sum(importance_scores)

        hybrid = alpha * req_weights + (1 - alpha) * imp_weights
        return hybrid / np.sum(hybrid)
