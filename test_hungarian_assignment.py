"""
Test script for Hungarian Algorithm with equal dimensions (10x10)
Uses profiles_2.csv and activities_2.csv

Author: Abdel YEZZA (Ph.D)
"""

from pathlib import Path
import pandas as pd
from src.core.profile_processor import load_profiles_from_csv, load_activities_from_csv, ProfileProcessor
from src.core.optimal_assignment import OptimalAssignment
from src.visualization.charts import ProfileVisualizer


def main():
    print("="*80)
    print("HUNGARIAN ALGORITHM TEST - Equal Dimensions (10x10)")
    print("="*80)

    # Paths
    profiles_file = Path('data/input/profiles_2.csv')
    activities_file = Path('data/input/activities_2.csv')

    # Check files exist
    if not profiles_file.exists():
        print(f"Error: {profiles_file} not found!")
        return
    if not activities_file.exists():
        print(f"Error: {activities_file} not found!")
        return

    # Load data
    print("\nStep 1: Loading data...")
    profiles_df = load_profiles_from_csv(profiles_file)
    activities_df = load_activities_from_csv(activities_file)

    print(f"  Profiles loaded: {len(profiles_df)}")
    print(f"  Activities loaded: {len(activities_df)}")
    print(f"  Dimensions match: {len(profiles_df) == len(activities_df)} [OK]")

    # Create processor
    print("\nStep 2: Running TOPSIS analysis...")
    processor = ProfileProcessor(
        profiles_df=profiles_df,
        activities_df=activities_df,
        threshold=3.0,
        min_threshold=0.0,
        max_threshold=5.0,
        proximity_formula="variant"
    )

    # Process all activities
    processor.process_all_activities(
        weight_strategy="uniform",
        verbose=False
    )

    print("  TOPSIS analysis complete!")

    # Get full results matrix
    full_results_df = processor.get_full_results_matrix()

    # Display ranking matrix
    print("\nStep 3: Ranking Matrix (Top 3 per activity):")
    print("-" * 80)
    ranking_matrix = processor.get_ranking_matrix(top_n=3)
    print(ranking_matrix.to_string(index=False))

    # Save TOPSIS results
    output_dir = Path('data/output_test')
    output_dir.mkdir(parents=True, exist_ok=True)

    rankings_dir = output_dir / "rankings"
    rankings_dir.mkdir(exist_ok=True)

    full_results_df.to_csv(rankings_dir / 'full_results_matrix_test.csv')
    ranking_matrix.to_csv(rankings_dir / 'ranking_matrix_test.csv', index=False)
    print(f"\nTOPSIS results saved to: {rankings_dir}")

    # Create optimal assignment solver
    print("\n" + "="*80)
    print("Step 4: OPTIMAL ASSIGNMENT - Hungarian Algorithm")
    print("="*80)

    solver = OptimalAssignment(full_results_df)

    # Solve using Hungarian Algorithm
    # Since dimensions match, it will automatically use Hungarian
    assignment_results = solver.solve()

    # Print detailed results
    solver.print_results()

    # Save assignment results
    assignment_csv = rankings_dir / 'optimal_assignment_hungarian.csv'
    solver.save_results(assignment_csv)

    # Get assignment matrices
    assignment_matrix = solver.get_assignment_matrix()
    score_matrix = solver.get_assignment_scores()

    # Create visualization
    print("\n" + "="*80)
    print("Step 5: GENERATING OPTIMAL ASSIGNMENT HEATMAP")
    print("="*80)

    viz_dir = output_dir / 'visualizations'
    visualizer = ProfileVisualizer(output_dir=viz_dir, dpi=300)

    heatmap_path = visualizer.plot_optimal_assignment_heatmap(
        full_results_df=full_results_df,
        assignment_matrix=assignment_matrix,
        assignment_info=assignment_results,
        proximity_formula='TOPSIS Standard',
        save=True
    )

    print(f"\nOptimal assignment heatmap saved to:")
    print(f"  {heatmap_path}")

    # Comparison: Show what changed from greedy rankings
    print("\n" + "="*80)
    print("COMPARISON: Hungarian vs. Simple Top-1 Selection")
    print("="*80)
    print(f"{'Activity':<30} {'Hungarian':<20} {'Top-1 Ranking':<20} {'Status':<10}")
    print("-"*80)

    for activity in full_results_df.index:
        # Hungarian assignment
        hungarian_profile = assignment_results['assignment'][activity]['profile']
        hungarian_score = assignment_results['assignment'][activity]['score']

        # Top-1 from ranking
        top1_profile = full_results_df.loc[activity].idxmax()
        top1_score = full_results_df.loc[activity].max()

        status = "Same" if hungarian_profile == top1_profile else "CHANGED"

        print(f"{activity:<30} {hungarian_profile:<20} {top1_profile:<20} {status:<10}")

    # Final summary
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"Assignment Method: {assignment_results['method'].upper()}")
    print(f"Total Assignments: {assignment_results['n_assignments']}")
    print(f"Total Score: {assignment_results['total_score']:.6f}")
    print(f"Average Score: {assignment_results['average_score']:.6f}")
    print(f"\nFiles created:")
    print(f"  1. Full results: {rankings_dir / 'full_results_matrix_test.csv'}")
    print(f"  2. Ranking matrix: {rankings_dir / 'ranking_matrix_test.csv'}")
    print(f"  3. Assignment CSV: {assignment_csv}")
    print(f"  4. Heatmap: {heatmap_path}")
    print("="*80)


if __name__ == '__main__':
    main()
