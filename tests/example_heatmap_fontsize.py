"""
Example: How to control annotation font size in heatmaps

This script demonstrates how to use the annot_fontsize parameter
in the plot_comparison_heatmap and plot_optimal_assignment_heatmap functions.

Author: Abdel YEZZA (Ph.D)
"""

from pathlib import Path
import pandas as pd
from src.core.profile_processor import ProfileProcessor, load_profiles_from_csv, load_activities_from_csv
from src.visualization.charts import ProfileVisualizer


def example_fontsize_control():
    """Demonstrate font size control in heatmaps."""

    # Load data
    profiles_file = Path('data/input/profiles.csv')
    activities_file = Path('data/input/activities.csv')

    if not profiles_file.exists() or not activities_file.exists():
        print("Error: CSV files not found!")
        return

    profiles_df = load_profiles_from_csv(profiles_file)
    activities_df = load_activities_from_csv(activities_file)

    print("="*80)
    print("HEATMAP ANNOTATION FONT SIZE EXAMPLE")
    print("="*80)

    # Create processor
    processor = ProfileProcessor(
        profiles_df=profiles_df,
        activities_df=activities_df,
        threshold=3.0,
        min_threshold=0.0,
        max_threshold=5.0,
        proximity_formula='variant'
    )

    # Process all activities
    processor.process_all_activities(weight_strategy="uniform", verbose=False)

    # Get full results
    full_results_df = processor.get_full_results_matrix()

    # Create visualizer
    output_dir = Path('data/output_fontsize_demo')
    output_dir.mkdir(parents=True, exist_ok=True)

    visualizer = ProfileVisualizer(output_dir=output_dir, dpi=300)

    # Generate heatmaps with different font sizes
    print("\nGenerating heatmaps with different font sizes...")

    font_sizes = [6, 8, 10, 12]

    for fontsize in font_sizes:
        print(f"\n  Creating heatmap with font size {fontsize}...")

        # Save with custom filename to avoid overwriting
        temp_path = visualizer.plot_comparison_heatmap(
            full_results_df=full_results_df,
            proximity_formula='Variant Formula',
            save=True,
            annot_fontsize=fontsize
        )

        # Rename to include font size in filename
        if temp_path:
            new_path = output_dir / f'heatmap_fontsize_{fontsize}.png'
            temp_path.rename(new_path)
            print(f"  Saved: {new_path}")

    print("\n" + "="*80)
    print("COMPARISON GUIDE:")
    print("="*80)
    print("Font Size | Best Use Case")
    print("-"*80)
    print("  6       | Very large matrices (>20x20), maximum information density")
    print("  8       | Default - good balance for most use cases (10x20 to 20x30)")
    print("  10      | Better readability for medium matrices (5x10 to 10x20)")
    print("  12      | Small matrices (<10x10), presentations, large displays")
    print("-"*80)

    print(f"\nAll heatmaps saved to: {output_dir}")
    print("="*80)


def example_code_usage():
    """Show code examples for using annot_fontsize parameter."""

    print("\n" + "="*80)
    print("CODE EXAMPLES: Using annot_fontsize Parameter")
    print("="*80)

    print("""
# Example 1: Comparison Heatmap with Small Font
visualizer = ProfileVisualizer(output_dir='figures', dpi=300)
visualizer.plot_comparison_heatmap(
    full_results_df=results_df,
    proximity_formula='Variant',
    save=True,
    annot_fontsize=6  # <-- Small font for large matrices
)

# Example 2: Comparison Heatmap with Large Font
visualizer.plot_comparison_heatmap(
    full_results_df=results_df,
    proximity_formula='Standard',
    save=True,
    annot_fontsize=12  # <-- Large font for presentations
)

# Example 3: Optimal Assignment Heatmap with Custom Font
visualizer.plot_optimal_assignment_heatmap(
    full_results_df=results_df,
    assignment_matrix=assignment_matrix,
    assignment_info=assignment_info,
    proximity_formula='Variant',
    save=True,
    annot_fontsize=10  # <-- Medium font size
)

# Example 4: Using Default Font Size (8)
visualizer.plot_comparison_heatmap(
    full_results_df=results_df,
    proximity_formula='Standard',
    save=True
    # annot_fontsize not specified, uses default of 8
)
""")

    print("="*80)
    print("\nTIPS:")
    print("- Start with default (8) and adjust based on your matrix size")
    print("- Smaller fonts (6-7) for large datasets (>15 profiles/activities)")
    print("- Larger fonts (10-12) for presentations or small datasets")
    print("- Test different sizes to find what works best for your data")
    print("="*80)


if __name__ == '__main__':
    print("Choose an option:")
    print("1. Generate heatmaps with different font sizes (requires data)")
    print("2. Show code examples only")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == '1':
        example_fontsize_control()
    else:
        example_code_usage()
