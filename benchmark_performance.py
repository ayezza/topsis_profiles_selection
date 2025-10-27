"""
Performance Benchmark Script for TOPSIS Profile Selection System

This script generates large random datasets, runs TOPSIS analysis, and measures
execution time and memory usage for performance evaluation.

Author: Abdel YEZZA (Ph.D)
"""

import time
import psutil
import os
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.profile_processor import ProfileProcessor
from src.core.optimal_assignment import OptimalAssignment
from generate_large_dataset import generate_dataset_pair


class PerformanceBenchmark:
    """Performance benchmark tool for TOPSIS system."""

    def __init__(self):
        self.results = []
        self.process = psutil.Process(os.getpid())

    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        return self.process.memory_info().rss / 1024 / 1024

    def benchmark_topsis(
        self,
        n_profiles: int,
        n_activities: int,
        n_skills: int,
        proximity_formula: str = 'variant',
        use_assignment: bool = False
    ) -> dict:
        """
        Run TOPSIS benchmark with given dimensions.

        Args:
            n_profiles: Number of profiles
            n_activities: Number of activities
            n_skills: Number of skills
            proximity_formula: TOPSIS proximity formula
            use_assignment: Whether to run optimal assignment

        Returns:
            Dictionary with benchmark results
        """
        print("\n" + "="*80)
        print(f"BENCHMARK: {n_profiles} profiles × {n_activities} activities × {n_skills} skills")
        print("="*80)

        result = {
            'n_profiles': n_profiles,
            'n_activities': n_activities,
            'n_skills': n_skills,
            'total_cells': (n_profiles + n_activities) * n_skills,
            'proximity_formula': proximity_formula,
            'use_assignment': use_assignment
        }

        # Generate data
        print("\n[1/4] Generating random dataset...")
        start_time = time.time()
        start_memory = self.get_memory_usage()

        output_dir = Path('data/benchmark')
        profiles_df, activities_df = generate_dataset_pair(
            n_profiles=n_profiles,
            n_activities=n_activities,
            n_skills=n_skills,
            output_dir=output_dir,
            prefix=f'bench_{n_profiles}x{n_activities}',
            seed=42
        )

        result['data_generation_time'] = time.time() - start_time
        result['data_generation_memory'] = self.get_memory_usage() - start_memory

        print(f"  Time: {result['data_generation_time']:.2f}s")
        print(f"  Memory: {result['data_generation_memory']:.1f} MB")

        # Initialize processor
        print("\n[2/4] Initializing TOPSIS processor...")
        start_time = time.time()
        start_memory = self.get_memory_usage()

        processor = ProfileProcessor(
            profiles_df=profiles_df,
            activities_df=activities_df,
            threshold=3.0,
            min_threshold=0.0,
            max_threshold=5.0,
            proximity_formula=proximity_formula
        )

        result['init_time'] = time.time() - start_time
        result['init_memory'] = self.get_memory_usage() - start_memory

        print(f"  Time: {result['init_time']:.2f}s")
        print(f"  Memory: {result['init_memory']:.1f} MB")

        # Run TOPSIS analysis
        print("\n[3/4] Running TOPSIS analysis...")
        start_time = time.time()
        start_memory = self.get_memory_usage()

        processor.process_all_activities(
            weight_strategy='uniform',
            verbose=False
        )

        result['topsis_time'] = time.time() - start_time
        result['topsis_memory'] = self.get_memory_usage() - start_memory

        print(f"  Time: {result['topsis_time']:.2f}s")
        print(f"  Memory: {result['topsis_memory']:.1f} MB")
        print(f"  Time per activity: {result['topsis_time'] / n_activities * 1000:.1f} ms")

        # Optional: Run assignment
        if use_assignment and n_profiles == n_activities:
            print("\n[4/4] Running optimal assignment (Hungarian)...")
            start_time = time.time()
            start_memory = self.get_memory_usage()

            full_results_df = processor.get_full_results_matrix()
            solver = OptimalAssignment(full_results_df)
            assignment_results = solver.solve(force_method='hungarian')

            result['assignment_time'] = time.time() - start_time
            result['assignment_memory'] = self.get_memory_usage() - start_memory

            print(f"  Time: {result['assignment_time']:.2f}s")
            print(f"  Memory: {result['assignment_memory']:.1f} MB")
        else:
            result['assignment_time'] = None
            result['assignment_memory'] = None
            print("\n[4/4] Skipping assignment (dimensions don't match or not requested)")

        # Calculate totals
        result['total_time'] = (
            result['data_generation_time'] +
            result['init_time'] +
            result['topsis_time'] +
            (result['assignment_time'] or 0)
        )

        result['peak_memory'] = self.get_memory_usage()

        # Print summary
        print("\n" + "="*80)
        print("BENCHMARK RESULTS SUMMARY")
        print("="*80)
        print(f"Dataset: {n_profiles} profiles × {n_activities} activities × {n_skills} skills")
        print(f"Total data points: {result['total_cells']:,}")
        print(f"\nTiming Breakdown:")
        print(f"  Data generation: {result['data_generation_time']:.2f}s")
        print(f"  Initialization:  {result['init_time']:.2f}s")
        print(f"  TOPSIS analysis: {result['topsis_time']:.2f}s")
        if result['assignment_time']:
            print(f"  Assignment:      {result['assignment_time']:.2f}s")
        print(f"  TOTAL:           {result['total_time']:.2f}s")
        print(f"\nMemory Usage:")
        print(f"  Peak memory: {result['peak_memory']:.1f} MB")
        print(f"\nPerformance Metrics:")
        print(f"  Time per activity: {result['topsis_time'] / n_activities * 1000:.1f} ms")
        print(f"  Throughput: {n_activities / result['topsis_time']:.1f} activities/second")
        print("="*80)

        self.results.append(result)
        return result

    def run_multiple_benchmarks(self, test_sizes: list, proximity_formula: str = 'variant'):
        """
        Run benchmarks for multiple dataset sizes.

        Args:
            test_sizes: List of (n_profiles, n_activities, n_skills) tuples
            proximity_formula: TOPSIS proximity formula
        """
        print("\n" + "="*80)
        print("RUNNING MULTIPLE BENCHMARKS")
        print("="*80)
        print(f"Test configurations: {len(test_sizes)}")
        print(f"Proximity formula: {proximity_formula}")
        print("="*80)

        for i, (n_profiles, n_activities, n_skills) in enumerate(test_sizes, 1):
            print(f"\n>>> Test {i}/{len(test_sizes)}")
            use_assignment = (n_profiles == n_activities)
            self.benchmark_topsis(
                n_profiles=n_profiles,
                n_activities=n_activities,
                n_skills=n_skills,
                proximity_formula=proximity_formula,
                use_assignment=use_assignment
            )

        # Generate comparison report
        self.print_comparison_report()

    def print_comparison_report(self):
        """Print comparison report for all benchmarks."""
        if not self.results:
            print("No benchmark results available.")
            return

        print("\n" + "="*80)
        print("BENCHMARK COMPARISON REPORT")
        print("="*80)

        # Create DataFrame for easy comparison
        df = pd.DataFrame(self.results)

        # Sort by total cells
        df = df.sort_values('total_cells')

        print(f"\n{'Dataset':<20} {'TOPSIS Time':<15} {'Total Time':<15} {'Peak Memory':<15} {'Throughput':<15}")
        print("-"*80)

        for _, row in df.iterrows():
            dataset_str = f"{row['n_profiles']}×{row['n_activities']}×{row['n_skills']}"
            topsis_time = f"{row['topsis_time']:.2f}s"
            total_time = f"{row['total_time']:.2f}s"
            memory = f"{row['peak_memory']:.1f} MB"
            throughput = f"{row['n_activities'] / row['topsis_time']:.1f} act/s"

            print(f"{dataset_str:<20} {topsis_time:<15} {total_time:<15} {memory:<15} {throughput:<15}")

        print("-"*80)

        # Save to CSV
        output_path = Path('data/benchmark/benchmark_results.csv')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\nDetailed results saved to: {output_path}")
        print("="*80)

    def save_report(self, output_path: Path):
        """Save detailed benchmark report."""
        if not self.results:
            print("No benchmark results to save.")
            return

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("TOPSIS PROFILE SELECTION SYSTEM - PERFORMANCE BENCHMARK REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total benchmarks: {len(self.results)}\n")
            f.write("="*80 + "\n\n")

            for i, result in enumerate(self.results, 1):
                f.write(f"Benchmark {i}\n")
                f.write("-"*80 + "\n")
                f.write(f"Dataset: {result['n_profiles']} profiles × {result['n_activities']} activities × {result['n_skills']} skills\n")
                f.write(f"Total data points: {result['total_cells']:,}\n")
                f.write(f"Proximity formula: {result['proximity_formula']}\n")
                f.write(f"\nTiming:\n")
                f.write(f"  Data generation: {result['data_generation_time']:.2f}s\n")
                f.write(f"  Initialization:  {result['init_time']:.2f}s\n")
                f.write(f"  TOPSIS analysis: {result['topsis_time']:.2f}s\n")
                if result['assignment_time']:
                    f.write(f"  Assignment:      {result['assignment_time']:.2f}s\n")
                f.write(f"  TOTAL:           {result['total_time']:.2f}s\n")
                f.write(f"\nMemory:\n")
                f.write(f"  Peak memory: {result['peak_memory']:.1f} MB\n")
                f.write(f"\nPerformance:\n")
                f.write(f"  Time per activity: {result['topsis_time'] / result['n_activities'] * 1000:.1f} ms\n")
                f.write(f"  Throughput: {result['n_activities'] / result['topsis_time']:.1f} activities/second\n")
                f.write("\n" + "="*80 + "\n\n")

        print(f"\nDetailed report saved to: {output_path}")


def main():
    """Main benchmark execution."""
    print("="*80)
    print("TOPSIS PERFORMANCE BENCHMARK SUITE")
    print("="*80)
    start_time = datetime.now()
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System: Python {sys.version.split()[0]}")
    print(f"Available memory: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.1f} GB")
    print("="*80)

    benchmark = PerformanceBenchmark()

    # Define test configurations
    # Format: (n_profiles, n_activities, n_skills)
    test_sizes = [
        (100, 100, 20),      # Small: 100×100 with 20 skills
        (500, 500, 30),      # Medium: 500×500 with 30 skills
        (1000, 1000, 50),    # Large: 1000×1000 with 50 skills (YOUR REQUEST!)
        # (2000, 2000, 50),  # Very large: 2000×2000 (uncomment if you have time/memory)
    ]

    print("\nPlanned benchmarks:")
    for i, (p, a, s) in enumerate(test_sizes, 1):
        total_cells = (p + a) * s
        print(f"  {i}. {p}×{a}×{s} ({total_cells:,} data points)")

    response = input("\nProceed with benchmarks? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return

    # Run benchmarks
    benchmark.run_multiple_benchmarks(test_sizes, proximity_formula='variant')

    # Save detailed report
    report_path = Path('data/benchmark/benchmark_report.txt')
    benchmark.save_report(report_path)

    print("\n" + "="*80)
    print("BENCHMARK SUITE COMPLETED")
    print("="*80)
    end_time = datetime.now()
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration: {end_time - start_time}")
    print("\nResults saved to:")
    print(f"  - CSV: data/benchmark/benchmark_results.csv")
    print(f"  - Report: data/benchmark/benchmark_report.txt")
    print("="*80)


if __name__ == '__main__':
    main()
