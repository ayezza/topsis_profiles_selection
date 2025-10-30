"""
Optimal Assignment Module
Handles optimal 1-to-1 assignment between profiles and activities
using Hungarian Algorithm (when dimensions match) or greedy approach
Author: Abdel YEZZA (Ph.D)
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
from scipy.optimize import linear_sum_assignment


class OptimalAssignment:
    """
    Handles optimal assignment between profiles and activities.
    """

    def __init__(self, full_results_df: pd.DataFrame):
        """
        Initialize optimal assignment solver.

        Args:
            full_results_df: DataFrame with activities as rows, profiles as columns
                           containing TOPSIS proximity coefficients
        """
        self.full_results_df = full_results_df.copy()
        self.activities = full_results_df.index.tolist()
        self.profiles = full_results_df.columns.tolist()
        self.n_activities = len(self.activities)
        self.n_profiles = len(self.profiles)

        self.assignment = None
        self.assignment_method = None
        self.total_score = None

    def check_dimensions(self) -> Tuple[bool, str]:
        """
        Check if dimensions allow for Hungarian Algorithm.

        Returns:
            Tuple of (can_use_hungarian, message)
        """
        if self.n_activities == self.n_profiles:
            return True, f"Dimensions match: {self.n_activities} activities = {self.n_profiles} profiles. Hungarian Algorithm can be applied."
        else:
            return False, f"Dimensions mismatch: {self.n_activities} activities ≠ {self.n_profiles} profiles. Hungarian Algorithm cannot be applied. Using greedy approach instead."

    def solve_hungarian(self) -> Dict:
        """
        Solve optimal assignment using Hungarian Algorithm.
        Maximizes total TOPSIS score.

        Returns:
            Dictionary with assignment results
        """
        # Convert DataFrame to numpy array
        cost_matrix = self.full_results_df.values

        # Hungarian algorithm minimizes, so we negate for maximization
        # We use negative values because linear_sum_assignment minimizes
        row_ind, col_ind = linear_sum_assignment(-cost_matrix)

        # Build assignment dictionary
        assignment = {}
        total_score = 0.0

        for activity_idx, profile_idx in zip(row_ind, col_ind):
            activity = self.activities[activity_idx]
            profile = self.profiles[profile_idx]
            score = cost_matrix[activity_idx, profile_idx]

            assignment[activity] = {
                'profile': profile,
                'score': score,
                'activity_idx': activity_idx,
                'profile_idx': profile_idx
            }
            total_score += score

        self.assignment = assignment
        self.assignment_method = 'hungarian'
        self.total_score = total_score

        return {
            'method': 'hungarian',
            'assignment': assignment,
            'total_score': total_score,
            'average_score': total_score / len(assignment),
            'n_assignments': len(assignment)
        }

    def solve_greedy(self) -> Dict:
        """
        Solve assignment using greedy approach.
        Iteratively assigns each activity to its best available (unassigned) profile.

        Returns:
            Dictionary with assignment results
        """
        assignment = {}
        assigned_profiles = set()
        total_score = 0.0

        # Create a sorted list of (activity, profile, score) tuples
        candidates = []
        for activity in self.activities:
            for profile in self.profiles:
                score = self.full_results_df.loc[activity, profile]
                candidates.append((activity, profile, score))

        # Sort by score in descending order
        candidates.sort(key=lambda x: x[2], reverse=True)

        # Greedy assignment
        assigned_activities = set()
        for activity, profile, score in candidates:
            if activity not in assigned_activities and profile not in assigned_profiles:
                assignment[activity] = {
                    'profile': profile,
                    'score': score,
                    'activity_idx': self.activities.index(activity),
                    'profile_idx': self.profiles.index(profile)
                }
                assigned_activities.add(activity)
                assigned_profiles.add(profile)
                total_score += score

                # Stop when all activities are assigned
                if len(assigned_activities) == self.n_activities:
                    break

        self.assignment = assignment
        self.assignment_method = 'greedy'
        self.total_score = total_score

        return {
            'method': 'greedy',
            'assignment': assignment,
            'total_score': total_score,
            'average_score': total_score / len(assignment) if assignment else 0,
            'n_assignments': len(assignment),
            'unassigned_profiles': list(set(self.profiles) - assigned_profiles)
        }

    def solve(self, force_method: Optional[str] = None) -> Dict:
        """
        Solve optimal assignment problem automatically.
        Uses Hungarian if dimensions match, otherwise greedy.

        Args:
            force_method: If specified, force use of 'hungarian' or 'greedy'

        Returns:
            Dictionary with assignment results
        """
        can_use_hungarian, msg = self.check_dimensions()

        print(f"\n{'='*80}")
        print("OPTIMAL ASSIGNMENT SOLVER")
        print(f"{'='*80}")
        print(f"Activities: {self.n_activities}")
        print(f"Profiles: {self.n_profiles}")
        # Replace special characters for console compatibility
        msg_safe = msg.replace('≠', '!=')
        print(f"\n{msg_safe}")

        if force_method == 'hungarian':
            if not can_use_hungarian:
                raise ValueError("Cannot use Hungarian Algorithm with mismatched dimensions!")
            print("\nUsing Hungarian Algorithm (forced)...")
            return self.solve_hungarian()
        elif force_method == 'greedy':
            print("\nUsing Greedy Approach (forced)...")
            return self.solve_greedy()
        else:
            # Auto-select method
            if can_use_hungarian:
                print("\nUsing Hungarian Algorithm for optimal 1-to-1 assignment...")
                return self.solve_hungarian()
            else:
                print("\nUsing Greedy Approach for best-effort assignment...")
                return self.solve_greedy()

    def get_assignment_matrix(self) -> pd.DataFrame:
        """
        Create a binary matrix showing the optimal assignment.

        Returns:
            DataFrame with 1 for assigned pairs, 0 otherwise
        """
        if self.assignment is None:
            raise ValueError("No assignment computed yet. Run solve() first.")

        # Create zero matrix
        assignment_matrix = pd.DataFrame(
            0,
            index=self.activities,
            columns=self.profiles
        )

        # Fill in assignments
        for activity, info in self.assignment.items():
            profile = info['profile']
            assignment_matrix.loc[activity, profile] = 1

        return assignment_matrix

    def get_assignment_scores(self) -> pd.DataFrame:
        """
        Create a matrix showing scores for assigned pairs (0 for unassigned).

        Returns:
            DataFrame with scores for assigned pairs
        """
        if self.assignment is None:
            raise ValueError("No assignment computed yet. Run solve() first.")

        # Create zero matrix
        score_matrix = pd.DataFrame(
            0.0,
            index=self.activities,
            columns=self.profiles
        )

        # Fill in scores for assigned pairs
        for activity, info in self.assignment.items():
            profile = info['profile']
            score = info['score']
            score_matrix.loc[activity, profile] = score

        return score_matrix

    def print_results(self):
        """
        Print detailed assignment results.
        """
        if self.assignment is None:
            print("No assignment computed yet. Run solve() first.")
            return

        print(f"\n{'='*80}")
        print(f"OPTIMAL ASSIGNMENT RESULTS - Method: {self.assignment_method.upper()}")
        print(f"{'='*80}")
        print(f"Number of Assignments: {len(self.assignment)}")
        print(f"Sum of Proximity Values (All Assigned Pairs): {self.total_score:.6f}")
        print(f"  -> This is the sum of scores for all red-squared cells")
        print(f"Average Proximity per Assignment: {self.total_score / len(self.assignment):.6f}")
        print(f"\n{'Activity':<30} {'Profile':<30} {'Score':<15}")
        print(f"{'-'*80}")

        # Sort by activity name
        sorted_assignment = sorted(self.assignment.items(), key=lambda x: x[0])

        for activity, info in sorted_assignment:
            profile = info['profile']
            score = info['score']
            print(f"{activity:<30} {profile:<30} {score:<15.6f}")

        print(f"{'='*80}")

        # If greedy method, show unassigned profiles
        if self.assignment_method == 'greedy':
            assigned_profiles = {info['profile'] for info in self.assignment.values()}
            unassigned = set(self.profiles) - assigned_profiles
            if unassigned:
                print(f"\nUnassigned Profiles ({len(unassigned)}): {', '.join(sorted(unassigned))}")
                print(f"{'='*80}")

    def save_results(self, output_path: str):
        """
        Save assignment results to CSV.

        Args:
            output_path: Path to save CSV file
        """
        if self.assignment is None:
            raise ValueError("No assignment computed yet. Run solve() first.")

        # Create DataFrame
        results_data = []
        for activity, info in self.assignment.items():
            results_data.append({
                'Activity': activity,
                'Assigned_Profile': info['profile'],
                'Score': info['score']
            })

        df = pd.DataFrame(results_data)
        df = df.sort_values('Activity')

        # Add summary statistics at the end
        summary_rows = [
            {'Activity': '', 'Assigned_Profile': '', 'Score': ''},
            {'Activity': 'SUMMARY', 'Assigned_Profile': '', 'Score': ''},
            {'Activity': 'Method', 'Assigned_Profile': self.assignment_method.upper(), 'Score': ''},
            {'Activity': 'Total Assignments', 'Assigned_Profile': str(len(self.assignment)), 'Score': ''},
            {'Activity': 'Sum of Proximity Values', 'Assigned_Profile': '(All Assigned Pairs)', 'Score': f'{self.total_score:.6f}'},
            {'Activity': 'Average Proximity', 'Assigned_Profile': '(Per Assignment)', 'Score': f'{self.total_score / len(self.assignment):.6f}'}
        ]

        summary_df = pd.DataFrame(summary_rows)
        df_with_summary = pd.concat([df, summary_df], ignore_index=True)

        df_with_summary.to_csv(output_path, index=False)

        print(f"\nAssignment results saved to: {output_path}")
        print(f"  -> Includes summary: Total Score = {self.total_score:.6f}")
