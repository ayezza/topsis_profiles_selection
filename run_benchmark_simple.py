"""
Simple benchmark wrapper to time main.py execution

Author: Abdel YEZZA (Ph.D)
"""

import time
import subprocess
import sys

def run_timed_benchmark(profiles_path, activities_path, use_assignment=True):
    """Run main.py and measure execution time."""

    print("="*80)
    print("TOPSIS PERFORMANCE BENCHMARK - Simple Timer")
    print("="*80)
    print(f"Profiles: {profiles_path}")
    print(f"Activities: {activities_path}")
    print(f"Assignment: {use_assignment}")
    print("="*80)

    # Build command
    cmd = [
        sys.executable, 'main.py',
        '--profiles', profiles_path,
        '--activities', activities_path
    ]

    if use_assignment:
        cmd.extend(['--assignment', '--assignment-method', 'hungarian'])

    print("\nStarting benchmark...")
    print(f"Command: {' '.join(cmd)}\n")

    # Run and time
    start_time = time.time()

    result = subprocess.run(cmd, capture_output=False)

    end_time = time.time()
    elapsed = end_time - start_time

    # Print results
    print("\n" + "="*80)
    print("BENCHMARK RESULTS")
    print("="*80)
    print(f"Total execution time: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
    print(f"Exit code: {result.returncode}")
    print("="*80)

    return elapsed

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Time TOPSIS main.py execution')
    parser.add_argument('--profiles', required=True, help='Profiles CSV path')
    parser.add_argument('--activities', required=True, help='Activities CSV path')
    parser.add_argument('--no-assignment', action='store_true', help='Skip assignment')

    args = parser.parse_args()

    run_timed_benchmark(
        args.profiles,
        args.activities,
        use_assignment=not args.no_assignment
    )
