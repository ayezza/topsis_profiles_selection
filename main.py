"""
TOPSIS Profile Selection System
Main entry point for profile evaluation and ranking using TOPSIS algorithm

Author: Abdel YEZZA (Ph.D)
Combined System: Profile Assignment + TOPSIS Algorithm
"""

import argparse
import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.profile_processor import ProfileProcessor, load_profiles_from_csv, load_activities_from_csv
from src.core.skill_transformer import SkillTransformer
from src.core.optimal_assignment import OptimalAssignment

# Try to import visualization module (optional)
try:
    from src.visualization.charts import ProfileVisualizer
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Note: Visualization libraries not available. Install matplotlib and seaborn for visualizations.")


def load_config(config_path: Path) -> dict:
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


def print_header():
    """Print application header."""
    print("\n" + "="*80)
    print(" " * 20 + "TOPSIS PROFILE SELECTION SYSTEM")
    print(" " * 15 + "Profile Evaluation using TOPSIS Algorithm")
    print(" " * 25 + "Author: Abdel YEZZA (Ph.D)")
    print("="*80)


def print_config_summary(config: dict):
    """Print configuration summary."""
    print("\nConfiguration Summary:")
    print("-" * 80)
    print(f"  Profiles File: {config['data']['profiles_file']}")
    print(f"  Activities File: {config['data']['activities_file']}")
    print(f"  Output Directory: {config['data']['output_dir']}")
    print(f"\nThreshold Settings:")
    print(f"  Threshold: {config['threshold_settings']['threshold']}")
    print(f"  Range: [{config['threshold_settings']['min_threshold']}, {config['threshold_settings']['max_threshold']}]")
    print(f"  Description: {config['threshold_settings']['description']}")
    print(f"\nTOPSIS Settings:")
    print(f"  Proximity Formula: {config['topsis_settings']['proximity_formula']}")
    print(f"\nWeight Strategy:")
    print(f"  Strategy: {config['weight_settings']['strategy']}")
    print(f"  Description: {config['weight_settings']['strategy_descriptions'][config['weight_settings']['strategy']]}")
    print(f"\nOptimal Assignment:")
    print(f"  Enabled: {config['assignment_settings']['enable_optimal_assignment']}")
    if config['assignment_settings']['enable_optimal_assignment']:
        print(f"  Method: {config['assignment_settings']['assignment_method']}")
        print(f"  Description: {config['assignment_settings']['assignment_method_descriptions'][config['assignment_settings']['assignment_method']]}")
    print("-" * 80)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="TOPSIS Profile Selection System - Rank profiles based on skill requirements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default configuration
  python main.py

  # Use custom configuration
  python main.py -c my_config.json

  # Override threshold
  python main.py --threshold 3.5

  # Process single activity
  python main.py --activity "Backend_Development"

  # Use custom input files
  python main.py --profiles data/my_profiles.csv --activities data/my_activities.csv

  # Verbose mode with visualizations
  python main.py -v --viz

  # Use different weight strategy
  python main.py --weight-strategy requirement_based

  # Enable optimal assignment with Hungarian/Greedy algorithm
  python main.py --assignment

  # Force Hungarian algorithm (requires equal dimensions)
  python main.py --assignment --assignment-method hungarian

  # Use greedy assignment approach
  python main.py --assignment --assignment-method greedy
        """
    )

    parser.add_argument(
        '-c', '--config',
        type=str,
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )

    parser.add_argument(
        '--profiles',
        type=str,
        help='Path to profiles CSV file (overrides config)'
    )

    parser.add_argument(
        '--activities',
        type=str,
        help='Path to activities CSV file (overrides config)'
    )

    parser.add_argument(
        '--threshold',
        type=float,
        help='Skill level threshold (overrides config)'
    )

    parser.add_argument(
        '--min-threshold',
        type=float,
        help='Minimum skill level (overrides config)'
    )

    parser.add_argument(
        '--max-threshold',
        type=float,
        help='Maximum skill level (overrides config)'
    )

    parser.add_argument(
        '--activity',
        type=str,
        help='Process only this specific activity'
    )

    parser.add_argument(
        '--weight-strategy',
        type=str,
        choices=['uniform', 'requirement_based'],
        help='Weight generation strategy (overrides config)'
    )

    parser.add_argument(
        '--proximity-formula',
        type=str,
        choices=['standard', 'variant'],
        help='TOPSIS proximity formula (overrides config)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--viz', '--visualize',
        action='store_true',
        dest='visualize',
        help='Generate visualizations'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output directory (overrides config)'
    )

    parser.add_argument(
        '--assignment',
        action='store_true',
        help='Enable optimal assignment (Hungarian/Greedy)'
    )

    parser.add_argument(
        '--assignment-method',
        type=str,
        choices=['auto', 'hungarian', 'greedy'],
        help='Assignment method (overrides config)'
    )

    args = parser.parse_args()

    # Print header
    print_header()

    # Load configuration
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"\nError: Configuration file not found: {config_path}")
        print("Creating default configuration file...")
        # Here you could create a default config
        sys.exit(1)

    config = load_config(config_path)

    # Override config with command-line arguments
    if args.profiles:
        config['data']['profiles_file'] = args.profiles
    if args.activities:
        config['data']['activities_file'] = args.activities
    if args.threshold is not None:
        config['threshold_settings']['threshold'] = args.threshold
    if args.min_threshold is not None:
        config['threshold_settings']['min_threshold'] = args.min_threshold
    if args.max_threshold is not None:
        config['threshold_settings']['max_threshold'] = args.max_threshold
    if args.weight_strategy:
        config['weight_settings']['strategy'] = args.weight_strategy
    if args.proximity_formula:
        config['topsis_settings']['proximity_formula'] = args.proximity_formula
    if args.verbose:
        config['output_settings']['verbose'] = True
    if args.visualize:
        config['output_settings']['generate_visualizations'] = True
    if args.output:
        config['data']['output_dir'] = args.output
    if args.assignment:
        config['assignment_settings']['enable_optimal_assignment'] = True
    if args.assignment_method:
        config['assignment_settings']['assignment_method'] = args.assignment_method

    # Print configuration
    print_config_summary(config)

    # Load data
    print("\nLoading data...")
    try:
        profiles_path = Path(config['data']['profiles_file'])
        activities_path = Path(config['data']['activities_file'])

        if not profiles_path.exists():
            print(f"Error: Profiles file not found: {profiles_path}")
            sys.exit(1)

        if not activities_path.exists():
            print(f"Error: Activities file not found: {activities_path}")
            sys.exit(1)

        profiles_df = load_profiles_from_csv(profiles_path)
        activities_df = load_activities_from_csv(activities_path)

        print(f"  Loaded {len(profiles_df)} profiles")
        print(f"  Loaded {len(activities_df)} activities")
        print(f"  Skills: {len(profiles_df.columns)}")

    except Exception as e:
        print(f"\nError loading data: {e}")
        sys.exit(1)

    # Create processor
    print("\nInitializing TOPSIS processor...")
    try:
        processor = ProfileProcessor(
            profiles_df=profiles_df,
            activities_df=activities_df,
            threshold=config['threshold_settings']['threshold'],
            min_threshold=config['threshold_settings']['min_threshold'],
            max_threshold=config['threshold_settings']['max_threshold'],
            proximity_formula=config['topsis_settings']['proximity_formula']
        )
        print("  Processor initialized successfully")

    except Exception as e:
        print(f"\nError initializing processor: {e}")
        sys.exit(1)

    # Process activities
    print("\n" + "="*80)
    print("PROCESSING ACTIVITIES")
    print("="*80)

    try:
        if args.activity:
            # Process single activity
            print(f"\nProcessing single activity: {args.activity}")
            results = processor.process_activity(
                activity_name=args.activity,
                weight_strategy=config['weight_settings']['strategy'],
                verbose=config['output_settings']['verbose']
            )

            # Print results
            print("\n" + "="*80)
            print(f"RESULTS: {args.activity}")
            print("="*80)
            print(f"\nBest Profile: {results['best_alternative']}")
            print(f"Coefficient: {results['best_coefficient']:.6f} ({results['best_coefficient']*100:.2f}%)")
            print(f"\nTop 5 Profiles:")
            print("-" * 80)
            print(f"{'Rank':<6} {'Profile':<30} {'Coefficient':<15} {'Percentage'}")
            print("-" * 80)
            for i, result in enumerate(results['ranked_results'][:5]):
                print(f"{result['rank']:<6} {result['alternative']:<30} "
                      f"{result['coefficient']:<15.6f} {result['percentage']:.2f}%")

        else:
            # Process all activities
            print("\nProcessing all activities...")
            all_results = processor.process_all_activities(
                weight_strategy=config['weight_settings']['strategy'],
                verbose=config['output_settings']['verbose']
            )

            # Print summary
            processor.print_summary()

            # Print ranking matrix
            print("\n" + "="*80)
            print("RANKING MATRIX - Top 3 Profiles per Activity")
            print("="*80)
            ranking_matrix = processor.get_ranking_matrix(
                top_n=config['output_settings']['top_n_profiles']
            )
            print("\n" + ranking_matrix.to_string(index=False))

    except Exception as e:
        print(f"\nError during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Save results
    print("\n" + "="*80)
    print("SAVING RESULTS")
    print("="*80)

    try:
        output_dir = Path(config['data']['output_dir'])
        processor.save_results(output_dir)

    except Exception as e:
        print(f"\nError saving results: {e}")
        sys.exit(1)

    # Optimal Assignment (only for all activities mode)
    if config['assignment_settings']['enable_optimal_assignment'] and not args.activity:
        print("\n" + "="*80)
        print("OPTIMAL ASSIGNMENT")
        print("="*80)

        try:
            # Get full results matrix
            full_results_df = processor.get_full_results_matrix()

            # Create optimal assignment solver
            solver = OptimalAssignment(full_results_df)

            # Determine assignment method
            assignment_method = config['assignment_settings']['assignment_method']
            force_method = None if assignment_method == 'auto' else assignment_method

            # Solve assignment
            assignment_results = solver.solve(force_method=force_method)

            # Print results
            solver.print_results()

            # Save assignment results
            rankings_dir = output_dir / "rankings"
            rankings_dir.mkdir(parents=True, exist_ok=True)

            assignment_csv = rankings_dir / f'optimal_assignment_{assignment_results["method"]}.csv'
            solver.save_results(assignment_csv)

            # Generate assignment heatmap if visualization is enabled
            if config['assignment_settings']['generate_assignment_heatmap'] and VISUALIZATION_AVAILABLE:
                try:
                    viz_dir = output_dir / "figures"
                    visualizer = ProfileVisualizer(
                        output_dir=viz_dir,
                        dpi=config['visualization_settings']['figure_dpi']
                    )

                    assignment_matrix = solver.get_assignment_matrix()

                    heatmap_path = visualizer.plot_optimal_assignment_heatmap(
                        full_results_df=full_results_df,
                        assignment_matrix=assignment_matrix,
                        assignment_info=assignment_results,
                        proximity_formula=config['topsis_settings']['proximity_formula'],
                        save=True
                    )

                    print(f"\nOptimal assignment heatmap saved to: {heatmap_path}")

                except Exception as e:
                    print(f"\n  Warning: Could not generate assignment heatmap: {e}")

            # Comparison with top-1 rankings
            print("\n" + "="*80)
            print("COMPARISON: Optimal Assignment vs. Top-1 Rankings")
            print("="*80)
            print(f"{'Activity':<30} {'Optimal':<20} {'Top-1':<20} {'Status':<10}")
            print("-"*80)

            for activity in full_results_df.index:
                # Optimal assignment
                optimal_profile = assignment_results['assignment'][activity]['profile']

                # Top-1 from ranking
                top1_profile = full_results_df.loc[activity].idxmax()

                status = "Same" if optimal_profile == top1_profile else "CHANGED"
                print(f"{activity:<30} {optimal_profile:<20} {top1_profile:<20} {status:<10}")

            print("\n" + "="*80)
            print(f"Assignment Method: {assignment_results['method'].upper()}")
            print(f"Total Score: {assignment_results['total_score']:.6f}")
            print(f"Average Score: {assignment_results['average_score']:.6f}")
            print("="*80)

        except Exception as e:
            print(f"\n  Warning: Could not perform optimal assignment: {e}")
            import traceback
            traceback.print_exc()

    # Generate visualizations
    if config['output_settings']['generate_visualizations']:
        print("\n" + "="*80)
        print("GENERATING VISUALIZATIONS")
        print("="*80)

        if not VISUALIZATION_AVAILABLE:
            print("\n  Visualization libraries not installed.")
            print("  Install matplotlib and seaborn:")
            print("    pip install matplotlib seaborn")
        else:
            try:
                if not args.activity:
                    # Generate all visualizations for all activities
                    figures_dir = output_dir / "figures"
                    visualizer = ProfileVisualizer(
                        output_dir=figures_dir,
                        dpi=config['visualization_settings']['figure_dpi']
                    )

                    saved_files = visualizer.generate_all_visualizations(
                        processor=processor,
                        top_n=10
                    )

                    print(f"\n  Successfully generated {len(saved_files)} visualization files")
                    print(f"  Saved to: {figures_dir}")
                else:
                    print("\n  Visualization for single activity mode coming soon...")

            except Exception as e:
                print(f"\n  Warning: Could not generate visualizations: {e}")
                print("  Results are still available in the output directory.")

    print("\n" + "="*80)
    print("PROCESS COMPLETED SUCCESSFULLY")
    print("="*80)
    print(f"\nAll results saved to: {output_dir}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
