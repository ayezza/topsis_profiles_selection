"""
Generate Large Random Datasets for TOPSIS Performance Testing

This script generates random profiles and activities datasets with configurable dimensions
for stress-testing the TOPSIS Profile Selection System.

Author: Abdel YEZZA (Ph.D)
"""

import numpy as np
import pandas as pd
from pathlib import Path
import argparse
from datetime import datetime


def generate_random_profiles(n_profiles: int, n_skills: int, output_path: Path, seed: int = 42) -> pd.DataFrame:
    """
    Generate random profiles dataset.

    Args:
        n_profiles: Number of profiles to generate
        n_skills: Number of skills per profile
        output_path: Path to save the CSV file
        seed: Random seed for reproducibility

    Returns:
        DataFrame with random profiles
    """
    np.random.seed(seed)

    print(f"\nGenerating {n_profiles} profiles with {n_skills} skills...")

    # Generate profile names
    profile_names = [f"Profile_{i+1}" for i in range(n_profiles)]

    # Generate skill names
    skill_names = [f"Skill_{i+1}" for i in range(n_skills)]

    # Generate random skill levels (0.0 to 5.0)
    # Using normal distribution centered at 2.5 to get realistic spread
    data = np.random.normal(loc=2.5, scale=1.0, size=(n_profiles, n_skills))

    # Clip values to [0, 5] range
    data = np.clip(data, 0.0, 5.0)

    # Round to 1 decimal place
    data = np.round(data, 1)

    # Create DataFrame
    df = pd.DataFrame(data, columns=skill_names, index=profile_names)
    df.index.name = 'Profile'

    # Save to CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path)

    print(f"  [OK] Profiles saved to: {output_path}")
    print(f"  Shape: {df.shape}")
    print(f"  Skill range: [{df.min().min():.1f}, {df.max().max():.1f}]")
    print(f"  Mean skill level: {df.mean().mean():.2f}")

    return df


def generate_random_activities(n_activities: int, n_skills: int, output_path: Path, seed: int = 42) -> pd.DataFrame:
    """
    Generate random activities dataset.

    Args:
        n_activities: Number of activities to generate
        n_skills: Number of skill requirements per activity
        output_path: Path to save the CSV file
        seed: Random seed for reproducibility

    Returns:
        DataFrame with random activities
    """
    np.random.seed(seed + 1)  # Different seed than profiles

    print(f"\nGenerating {n_activities} activities with {n_skills} skill requirements...")

    # Generate activity names
    activity_names = [f"Activity_{i+1}" for i in range(n_activities)]

    # Generate skill names (same as profiles)
    skill_names = [f"Skill_{i+1}" for i in range(n_skills)]

    # Generate random skill requirements (0.0 to 5.0)
    # Activities tend to have higher requirements, so center at 3.0
    data = np.random.normal(loc=3.0, scale=1.2, size=(n_activities, n_skills))

    # Clip values to [0, 5] range
    data = np.clip(data, 0.0, 5.0)

    # Round to 1 decimal place
    data = np.round(data, 1)

    # Create DataFrame
    df = pd.DataFrame(data, columns=skill_names, index=activity_names)
    df.index.name = 'Activity'

    # Save to CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path)

    print(f"  [OK] Activities saved to: {output_path}")
    print(f"  Shape: {df.shape}")
    print(f"  Requirement range: [{df.min().min():.1f}, {df.max().max():.1f}]")
    print(f"  Mean requirement level: {df.mean().mean():.2f}")

    return df


def generate_dataset_pair(
    n_profiles: int,
    n_activities: int,
    n_skills: int,
    output_dir: Path,
    prefix: str = "large",
    seed: int = 42
):
    """
    Generate a pair of matching profiles and activities datasets.

    Args:
        n_profiles: Number of profiles
        n_activities: Number of activities
        n_skills: Number of skills
        output_dir: Output directory
        prefix: Filename prefix
        seed: Random seed
    """
    print("="*80)
    print(f"GENERATING LARGE RANDOM DATASET: {prefix}")
    print("="*80)
    print(f"Configuration:")
    print(f"  Profiles: {n_profiles}")
    print(f"  Activities: {n_activities}")
    print(f"  Skills: {n_skills}")
    print(f"  Total data points: {(n_profiles + n_activities) * n_skills:,}")
    print(f"  Random seed: {seed}")

    # Generate profiles
    profiles_path = output_dir / f"{prefix}_profiles.csv"
    profiles_df = generate_random_profiles(n_profiles, n_skills, profiles_path, seed)

    # Generate activities
    activities_path = output_dir / f"{prefix}_activities.csv"
    activities_df = generate_random_activities(n_activities, n_skills, activities_path, seed)

    # Print statistics
    print("\n" + "="*80)
    print("DATASET GENERATION COMPLETE")
    print("="*80)
    print(f"Files created:")
    print(f"  1. {profiles_path}")
    print(f"  2. {activities_path}")
    print(f"\nDataset info:")
    print(f"  Profiles shape: {profiles_df.shape}")
    print(f"  Activities shape: {activities_df.shape}")
    print(f"  Files size: ~{(profiles_path.stat().st_size + activities_path.stat().st_size) / 1024:.1f} KB")
    print("="*80)

    return profiles_df, activities_df


def main():
    """Main function with CLI interface."""
    parser = argparse.ArgumentParser(
        description="Generate large random datasets for TOPSIS performance testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 1000x1000 dataset (1000 profiles, 1000 activities, 50 skills)
  python generate_large_dataset.py --profiles 1000 --activities 1000 --skills 50

  # Generate 100x100 small test dataset
  python generate_large_dataset.py -p 100 -a 100 -s 10

  # Generate multiple datasets with different sizes
  python generate_large_dataset.py --profiles 500 --activities 500 --skills 30 --prefix test_500
  python generate_large_dataset.py --profiles 1000 --activities 1000 --skills 50 --prefix test_1000
  python generate_large_dataset.py --profiles 2000 --activities 2000 --skills 50 --prefix test_2000

  # Equal dimensions for Hungarian algorithm testing
  python generate_large_dataset.py -p 100 -a 100 -s 20 --prefix hungarian_100
        """
    )

    parser.add_argument(
        '-p', '--profiles',
        type=int,
        default=1000,
        help='Number of profiles to generate (default: 1000)'
    )

    parser.add_argument(
        '-a', '--activities',
        type=int,
        default=1000,
        help='Number of activities to generate (default: 1000)'
    )

    parser.add_argument(
        '-s', '--skills',
        type=int,
        default=50,
        help='Number of skills per profile/activity (default: 50)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='data/input',
        help='Output directory (default: data/input)'
    )

    parser.add_argument(
        '--prefix',
        type=str,
        default='large',
        help='Filename prefix (default: large)'
    )

    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )

    args = parser.parse_args()

    # Validate inputs
    if args.profiles < 1 or args.activities < 1 or args.skills < 1:
        print("Error: All dimensions must be positive integers!")
        return

    # Warning for very large datasets
    total_cells = (args.profiles + args.activities) * args.skills
    if total_cells > 10_000_000:  # > 10 million cells
        print(f"\n⚠️  WARNING: Large dataset detected ({total_cells:,} total data points)")
        print("    This may take significant time and memory.")
        response = input("    Continue? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

    # Generate datasets
    output_dir = Path(args.output)
    generate_dataset_pair(
        n_profiles=args.profiles,
        n_activities=args.activities,
        n_skills=args.skills,
        output_dir=output_dir,
        prefix=args.prefix,
        seed=args.seed
    )

    print(f"\n[SUCCESS] Dataset generation completed successfully!")
    print(f"\nTo test with TOPSIS, run:")
    print(f"  python main.py --profiles {output_dir / f'{args.prefix}_profiles.csv'} \\")
    print(f"                 --activities {output_dir / f'{args.prefix}_activities.csv'}")


if __name__ == '__main__':
    main()
