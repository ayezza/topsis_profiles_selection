"""
Test to demonstrate that different proximity formulas can lead to different
optimal assignments when using the Hungarian algorithm.

Author: Abdel YEZZA (Ph.D)
"""

import numpy as np
import pandas as pd
from pathlib import Path
from src.core.profile_processor import ProfileProcessor, load_profiles_from_csv, load_activities_from_csv
from src.core.optimal_assignment import OptimalAssignment


def compare_formulas():
    """Compare standard vs variant proximity formulas for assignment."""

    # Use the equal-dimension dataset (10x10)
    profiles_file = Path('data/input/profiles_2.csv')
    activities_file = Path('data/input/activities_2.csv')

    if not profiles_file.exists() or not activities_file.exists():
        print("Error: profiles_2.csv and activities_2.csv not found!")
        print("This test requires equal-dimension datasets.")
        return

    print("="*80)
    print("COMPARING PROXIMITY FORMULAS: STANDARD vs VARIANT")
    print("="*80)

    # Load data once
    profiles_df = load_profiles_from_csv(profiles_file)
    activities_df = load_activities_from_csv(activities_file)

    print(f"\nDataset: {len(profiles_df)} profiles × {len(activities_df)} activities")
    print(f"Skills: {len(profiles_df.columns)}")

    results = {}

    # Test both formulas
    for formula in ['standard', 'variant']:
        print(f"\n{'='*80}")
        print(f"TESTING: {formula.upper()} PROXIMITY FORMULA")
        print(f"{'='*80}")

        # Create processor with specific formula
        processor = ProfileProcessor(
            profiles_df=profiles_df,
            activities_df=activities_df,
            threshold=3.0,
            min_threshold=0.0,
            max_threshold=5.0,
            proximity_formula=formula
        )

        # Process all activities
        processor.process_all_activities(weight_strategy="uniform", verbose=False)

        # Get full results matrix
        full_results_df = processor.get_full_results_matrix()

        # Create optimal assignment solver
        solver = OptimalAssignment(full_results_df)

        # Solve using Hungarian
        assignment_results = solver.solve(force_method='hungarian')

        # Store results
        results[formula] = {
            'full_results': full_results_df.copy(),
            'assignment': assignment_results['assignment'],
            'total_score': assignment_results['total_score'],
            'average_score': assignment_results['average_score']
        }

        print(f"\nTotal Score: {assignment_results['total_score']:.6f}")
        print(f"Average Score: {assignment_results['average_score']:.6f}")

    # Compare results
    print("\n" + "="*80)
    print("COMPARISON: STANDARD vs VARIANT")
    print("="*80)

    # Compare score matrices
    print("\n1. SCORE COMPARISON:")
    print("-"*80)

    standard_matrix = results['standard']['full_results']
    variant_matrix = results['variant']['full_results']

    print(f"\nStandard formula score range: [{standard_matrix.min().min():.6f}, {standard_matrix.max().max():.6f}]")
    print(f"Variant formula score range:  [{variant_matrix.min().min():.6f}, {variant_matrix.max().max():.6f}]")

    # Compare assignments
    print("\n2. ASSIGNMENT COMPARISON:")
    print("-"*80)
    print(f"{'Activity':<30} {'Standard':<20} {'Variant':<20} {'Same?':<10}")
    print("-"*80)

    differences = 0
    for activity in standard_matrix.index:
        standard_profile = results['standard']['assignment'][activity]['profile']
        variant_profile = results['variant']['assignment'][activity]['profile']
        same = "YES" if standard_profile == variant_profile else "NO"
        if same == "NO":
            differences += 1
        print(f"{activity:<30} {standard_profile:<20} {variant_profile:<20} {same:<10}")

    print("-"*80)
    print(f"\nDifferences: {differences} out of {len(standard_matrix.index)} assignments ({differences/len(standard_matrix.index)*100:.1f}%)")

    # Compare total scores
    print("\n3. OPTIMIZATION SCORE COMPARISON:")
    print("-"*80)
    print(f"Standard formula total score: {results['standard']['total_score']:.6f}")
    print(f"Variant formula total score:  {results['variant']['total_score']:.6f}")
    print(f"Difference: {abs(results['standard']['total_score'] - results['variant']['total_score']):.6f}")

    # Detailed score comparison for activities with different assignments
    if differences > 0:
        print("\n4. DETAILED ANALYSIS OF CHANGED ASSIGNMENTS:")
        print("-"*80)
        for activity in standard_matrix.index:
            standard_profile = results['standard']['assignment'][activity]['profile']
            variant_profile = results['variant']['assignment'][activity]['profile']

            if standard_profile != variant_profile:
                print(f"\n{activity}:")
                print(f"  Standard assigned: {standard_profile} (score: {standard_matrix.loc[activity, standard_profile]:.6f})")
                print(f"  Variant assigned:  {variant_profile} (score: {variant_matrix.loc[activity, variant_profile]:.6f})")

                # Show what the other formula scored these profiles
                print(f"  In standard formula, {variant_profile} scored: {standard_matrix.loc[activity, variant_profile]:.6f}")
                print(f"  In variant formula, {standard_profile} scored: {variant_matrix.loc[activity, standard_profile]:.6f}")

    # Conclusion
    print("\n" + "="*80)
    print("CONCLUSION:")
    print("="*80)

    if differences == 0:
        print("[OK] Both formulas produced IDENTICAL assignments!")
        print("  The Hungarian algorithm found the same optimal matching.")
    else:
        print(f"[DIFFERENT] The formulas produced DIFFERENT assignments ({differences} differences)!")
        print("  This demonstrates that the proximity formula DOES affect")
        print("  the optimal assignment when using the Hungarian algorithm.")
        print("\n  Why? The variant formula creates different score distributions,")
        print("  which changes the cost matrix that the Hungarian algorithm optimizes.")

    print("="*80)


if __name__ == '__main__':
    compare_formulas()
