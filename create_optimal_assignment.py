"""
Script to create optimal 1-to-1 assignment between profiles and activities
with visualization heatmap.

Author: Abdel YEZZA (Ph.D)
"""

from pathlib import Path
import pandas as pd
from src.core.optimal_assignment import OptimalAssignment
from src.visualization.charts import ProfileVisualizer


def main():
    """
    Main function to solve optimal assignment and create visualization.
    """
    print("="*80)
    print("OPTIMAL PROFILE-ACTIVITY ASSIGNMENT")
    print("="*80)

    # Path to full results matrix
    results_file = Path('data/output/rankings/full_results_matrix.csv')

    if not results_file.exists():
        print(f"\nError: Results file not found at {results_file}")
        print("Please run the TOPSIS analysis first to generate results.")
        return

    # Load results
    print(f"\nLoading results from: {results_file}")
    full_results_df = pd.read_csv(results_file, index_col=0)

    print(f"\nData loaded:")
    print(f"  - Activities: {len(full_results_df)}")
    print(f"  - Profiles: {len(full_results_df.columns)}")

    # Create optimal assignment solver
    print("\n" + "="*80)
    solver = OptimalAssignment(full_results_df)

    # Solve optimal assignment
    # This will automatically use Hungarian if dimensions match,
    # otherwise use greedy approach
    assignment_results = solver.solve()

    # Print results
    solver.print_results()

    # Save assignment results to CSV
    output_dir = Path('data/output/rankings')
    output_dir.mkdir(parents=True, exist_ok=True)

    assignment_csv = output_dir / 'optimal_assignment.csv'
    solver.save_results(assignment_csv)

    # Get assignment matrices
    assignment_matrix = solver.get_assignment_matrix()

    # Create visualization
    print("\n" + "="*80)
    print("GENERATING OPTIMAL ASSIGNMENT HEATMAP")
    print("="*80)

    viz_output_dir = Path('data/output/visualizations')
    visualizer = ProfileVisualizer(output_dir=viz_output_dir, dpi=300)

    # Plot optimal assignment heatmap
    heatmap_path = visualizer.plot_optimal_assignment_heatmap(
        full_results_df=full_results_df,
        assignment_matrix=assignment_matrix,
        assignment_info=assignment_results,
        proximity_formula='TOPSIS',  # Update this based on your method
        save=True
    )

    if heatmap_path:
        print(f"\nSuccess! Optimal assignment heatmap created at:")
        print(f"  {heatmap_path}")

    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Assignment method: {assignment_results['method'].upper()}")
    print(f"Total assignments: {assignment_results['n_assignments']}")
    print(f"Total score: {assignment_results['total_score']:.6f}")
    print(f"Average score: {assignment_results['average_score']:.6f}")

    if assignment_results['method'] == 'greedy' and 'unassigned_profiles' in assignment_results:
        unassigned = assignment_results['unassigned_profiles']
        if unassigned:
            print(f"\nUnassigned profiles ({len(unassigned)}): {', '.join(unassigned)}")

    print("\nFiles created:")
    print(f"  1. Assignment CSV: {assignment_csv}")
    print(f"  2. Heatmap visualization: {heatmap_path}")
    print("="*80)


if __name__ == '__main__':
    main()
