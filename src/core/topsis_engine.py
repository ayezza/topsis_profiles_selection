"""
TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) Engine
Adapted for profile selection based on skill levels
Author: Combined from topsis_algorithm project
"""

import numpy as np
from typing import List, Dict, Tuple, Optional


class TopsisEngine:
    """
    TOPSIS algorithm implementation for multi-criteria decision making.
    Used to rank profiles based on multiple skill criteria.
    """

    def __init__(
        self,
        decision_matrix: np.ndarray,
        weights: np.ndarray,
        criteria_types: np.ndarray,
        alternative_names: Optional[List[str]] = None,
        criteria_names: Optional[List[str]] = None,
        proximity_formula: str = "standard"
    ):
        """
        Initialize TOPSIS engine.

        Args:
            decision_matrix: 2D array (alternatives x criteria)
            weights: 1D array of criterion weights
            criteria_types: 1D array (1=beneficial/max, 0=non-beneficial/min)
            alternative_names: Names of alternatives (e.g., profile names)
            criteria_names: Names of criteria (e.g., skill names)
            proximity_formula: "standard" or "variant"
        """
        self.decision_matrix = np.array(decision_matrix, dtype=float)
        self.weights = np.array(weights, dtype=float)
        self.criteria_types = np.array(criteria_types, dtype=int)
        self.alternative_names = alternative_names or [f"Alt_{i+1}" for i in range(len(decision_matrix))]
        self.criteria_names = criteria_names or [f"Criterion_{i+1}" for i in range(len(weights))]
        self.proximity_formula = proximity_formula

        # Validate inputs
        self._validate_inputs()

        # Normalize weights
        self.weights = self.weights / np.sum(self.weights)

        # Results storage
        self.normalized_matrix = None
        self.weighted_matrix = None
        self.ideal_best = None
        self.ideal_worst = None
        self.distance_to_best = None
        self.distance_to_worst = None
        self.proximity_coefficients = None
        self.ranking = None

    def _validate_inputs(self):
        """Validate input dimensions and values."""
        n_alternatives, n_criteria = self.decision_matrix.shape

        if len(self.weights) != n_criteria:
            raise ValueError(f"Weights length ({len(self.weights)}) must match number of criteria ({n_criteria})")

        if len(self.criteria_types) != n_criteria:
            raise ValueError(f"Criteria types length ({len(self.criteria_types)}) must match number of criteria ({n_criteria})")

        if len(self.alternative_names) != n_alternatives:
            raise ValueError(f"Alternative names length ({len(self.alternative_names)}) must match number of alternatives ({n_alternatives})")

        if not all(ct in [0, 1] for ct in self.criteria_types):
            raise ValueError("Criteria types must be 0 (non-beneficial) or 1 (beneficial)")

        if np.any(self.weights < 0):
            raise ValueError("Weights must be non-negative")

        if np.sum(self.weights) == 0:
            raise ValueError("Sum of weights cannot be zero")

    def normalize_matrix(self) -> np.ndarray:
        """
        Step 1: Normalize decision matrix using Euclidean distance normalization.
        r_ij = x_ij / sqrt(sum(x_ij^2))

        Returns:
            Normalized matrix
        """
        # Calculate the Euclidean norm for each criterion (column)
        column_norms = np.sqrt(np.sum(self.decision_matrix ** 2, axis=0))

        # Avoid division by zero
        column_norms[column_norms == 0] = 1

        # Normalize
        self.normalized_matrix = self.decision_matrix / column_norms

        return self.normalized_matrix

    def apply_weights(self) -> np.ndarray:
        """
        Step 2: Apply weights to normalized matrix.
        t_ij = w_j * r_ij

        Returns:
            Weighted normalized matrix
        """
        if self.normalized_matrix is None:
            self.normalize_matrix()

        self.weighted_matrix = self.normalized_matrix * self.weights

        return self.weighted_matrix

    def determine_ideal_solutions(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Step 3: Determine ideal best (A+) and ideal worst (A-) solutions.

        For beneficial criteria (type=1): A+ = max, A- = min
        For non-beneficial criteria (type=0): A+ = min, A- = max

        Returns:
            Tuple of (ideal_best, ideal_worst)
        """
        if self.weighted_matrix is None:
            self.apply_weights()

        self.ideal_best = np.zeros(self.weighted_matrix.shape[1])
        self.ideal_worst = np.zeros(self.weighted_matrix.shape[1])

        for j in range(self.weighted_matrix.shape[1]):
            if self.criteria_types[j] == 1:  # Beneficial (maximize)
                self.ideal_best[j] = np.max(self.weighted_matrix[:, j])
                self.ideal_worst[j] = np.min(self.weighted_matrix[:, j])
            else:  # Non-beneficial (minimize)
                self.ideal_best[j] = np.min(self.weighted_matrix[:, j])
                self.ideal_worst[j] = np.max(self.weighted_matrix[:, j])

        return self.ideal_best, self.ideal_worst

    def calculate_distances(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Step 4: Calculate Euclidean distances from ideal solutions.

        E+[i] = sqrt(sum((t[i,j] - A+[j])^2))
        E-[i] = sqrt(sum((t[i,j] - A-[j])^2))

        Returns:
            Tuple of (distance_to_best, distance_to_worst)
        """
        if self.ideal_best is None or self.ideal_worst is None:
            self.determine_ideal_solutions()

        # Distance to ideal best
        diff_best = self.weighted_matrix - self.ideal_best
        self.distance_to_best = np.sqrt(np.sum(diff_best ** 2, axis=1))

        # Distance to ideal worst
        diff_worst = self.weighted_matrix - self.ideal_worst
        self.distance_to_worst = np.sqrt(np.sum(diff_worst ** 2, axis=1))

        return self.distance_to_best, self.distance_to_worst

    def calculate_proximity(self) -> np.ndarray:
        """
        Step 5: Calculate proximity coefficients (S*).

        Standard formula: S*[i] = E-[i] / (E+[i] + E-[i])
        Variant formula: S*[i] = E-[i] / E+[i] (then normalized to [0,1])

        Returns:
            Proximity coefficients (higher is better)
        """
        if self.distance_to_best is None or self.distance_to_worst is None:
            self.calculate_distances()

        if self.proximity_formula == "standard":
            # Standard TOPSIS formula
            denominator = self.distance_to_best + self.distance_to_worst
            # Avoid division by zero by adding a small epsilon
            denominator[denominator == 0] = 1e-10
            self.proximity_coefficients = self.distance_to_worst / denominator

        elif self.proximity_formula == "variant":
            # Variant formula: S* = E- / E+ for E+ != 0, else S* = E- / max(E+)
            raw_proximity = np.zeros_like(self.distance_to_worst)
            max_distance_to_best = np.max(self.distance_to_best)

            for i in range(len(self.distance_to_best)):
                if self.distance_to_best[i] != 0:
                    raw_proximity[i] = self.distance_to_worst[i] / self.distance_to_best[i]
                else:
                    # When E+ = 0, use max(E+) as denominator
                    if max_distance_to_best != 0:
                        raw_proximity[i] = self.distance_to_worst[i] / max_distance_to_best
                    else:
                        # Edge case: all distances to best are 0
                        raw_proximity[i] = 1.0

            # Normalize proximity coefficients to [0, 1] range
            max_prox = np.max(raw_proximity)
            if max_prox != 0:
                self.proximity_coefficients = raw_proximity / max_prox

        else:
            raise ValueError(f"Unknown proximity formula: {self.proximity_formula}")

        return self.proximity_coefficients

    def get_ranking(self) -> np.ndarray:
        """
        Get ranking of alternatives (indices sorted by proximity, best to worst).

        Returns:
            Array of indices in ranked order
        """
        if self.proximity_coefficients is None:
            self.calculate_proximity()

        self.ranking = np.argsort(self.proximity_coefficients)[::-1]

        return self.ranking

    def calculate(self, verbose: bool = False) -> np.ndarray:
        """
        Execute complete TOPSIS algorithm.

        Args:
            verbose: If True, print intermediate results

        Returns:
            Proximity coefficients
        """
        if verbose:
            print("="*80)
            print("TOPSIS Algorithm - Profile Selection")
            print("="*80)
            print(f"\nAlternatives: {len(self.alternative_names)}")
            print(f"Criteria: {len(self.criteria_names)}")
            print(f"Proximity Formula: {self.proximity_formula}")

        # Step 1: Normalize
        self.normalize_matrix()
        if verbose:
            print("\nStep 1: Normalized Matrix")
            print(self.normalized_matrix)

        # Step 2: Apply weights
        self.apply_weights()
        if verbose:
            print("\nStep 2: Weighted Normalized Matrix")
            print(self.weighted_matrix)

        # Step 3: Ideal solutions
        self.determine_ideal_solutions()
        if verbose:
            print("\nStep 3: Ideal Solutions")
            print(f"Ideal Best (A+): {self.ideal_best}")
            print(f"Ideal Worst (A-): {self.ideal_worst}")

        # Step 4: Calculate distances
        self.calculate_distances()
        if verbose:
            print("\nStep 4: Euclidean Distances")
            print(f"Distance to Best (E+): {self.distance_to_best}")
            print(f"Distance to Worst (E-): {self.distance_to_worst}")

        # Step 5: Proximity coefficients
        self.calculate_proximity()
        if verbose:
            print("\nStep 5: Proximity Coefficients")
            print(f"Coefficients: {self.proximity_coefficients}")

        # Get ranking
        self.get_ranking()
        if verbose:
            print("\n" + "="*80)
            print("RESULTS - Ranked Alternatives")
            print("="*80)
            for i, idx in enumerate(self.ranking):
                print(f"{i+1}. {self.alternative_names[idx]}: {self.proximity_coefficients[idx]:.6f} ({self.proximity_coefficients[idx]*100:.2f}%)")

        return self.proximity_coefficients

    def get_results_dict(self) -> Dict:
        """
        Get complete results as a dictionary.

        Returns:
            Dictionary with all results
        """
        if self.proximity_coefficients is None:
            self.calculate()

        results = []
        for i, idx in enumerate(self.ranking):
            results.append({
                'rank': i + 1,
                'alternative': self.alternative_names[idx],
                'coefficient': float(self.proximity_coefficients[idx]),
                'percentage': float(self.proximity_coefficients[idx] * 100),
                'distance_to_best': float(self.distance_to_best[idx]),
                'distance_to_worst': float(self.distance_to_worst[idx])
            })

        return {
            'ranked_results': results,
            'best_alternative': self.alternative_names[self.ranking[0]],
            'best_coefficient': float(self.proximity_coefficients[self.ranking[0]]),
            'metadata': {
                'n_alternatives': len(self.alternative_names),
                'n_criteria': len(self.criteria_names),
                'proximity_formula': self.proximity_formula,
                'criteria_names': self.criteria_names,
                'weights': self.weights.tolist(),
                'criteria_types': self.criteria_types.tolist()
            }
        }
