"""
Test script to demonstrate the impact of different threshold values
Compares results with threshold = 2.0, 3.0, 4.0

Author: Abdel YEZZA (Ph.D)
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.profile_processor import ProfileProcessor, load_profiles_from_csv, load_activities_from_csv


def test_threshold_impact():
    """Test and compare results with different thresholds."""

    print("="*80)
    print("THRESHOLD COMPARISON TEST")
    print("="*80)
    print("\nThis test demonstrates how different threshold values affect profile rankings.")
    print("We'll test with thresholds: 2.0 (lenient), 3.0 (balanced), 4.0 (strict)")
    print("\n" + "="*80 + "\n")

    # Load data
    profiles_df = load_profiles_from_csv('data/input/profiles.csv')
    activities_df = load_activities_from_csv('data/input/activities.csv')

    # Test activity
    test_activity = "Backend_Development"

    thresholds = [2.0, 3.0, 4.0]
    results_summary = {}

    for threshold in thresholds:
        print(f"\n{'='*80}")
        print(f"THRESHOLD = {threshold}")
        print(f"{'='*80}\n")

        # Create processor with this threshold
        processor = ProfileProcessor(
            profiles_df=profiles_df,
            activities_df=activities_df,
            threshold=threshold,
            min_threshold=0.0,
            max_threshold=5.0,
            proximity_formula='standard'
        )

        # Process the test activity
        result = processor.process_activity(
            activity_name=test_activity,
            weight_strategy='uniform',
            verbose=False
        )

        # Store results
        results_summary[threshold] = result

        # Print criteria classification
        required_skills = activities_df.loc[test_activity].values
        criteria_types = processor.skill_transformer.determine_criteria_types(required_skills)
        n_beneficial = sum(criteria_types == 1)
        n_non_beneficial = sum(criteria_types == 0)

        print(f"Criteria Classification:")
        print(f"  Beneficial skills: {n_beneficial} ({n_beneficial/len(criteria_types)*100:.1f}%)")
        print(f"  Non-beneficial skills: {n_non_beneficial} ({n_non_beneficial/len(criteria_types)*100:.1f}%)")

        # Print top 5
        print(f"\nTop 5 Profiles:")
        print("-" * 60)
        print(f"{'Rank':<6} {'Profile':<15} {'Coefficient':<15} {'Percentage'}")
        print("-" * 60)
        for i, res in enumerate(result['ranked_results'][:5]):
            print(f"{res['rank']:<6} {res['alternative']:<15} "
                  f"{res['coefficient']:<15.6f} {res['percentage']:.2f}%")

    # Comparison summary
    print("\n" + "="*80)
    print("COMPARISON SUMMARY")
    print("="*80)
    print(f"\nActivity: {test_activity}")
    print("\nBest Profile by Threshold:")
    print("-" * 60)
    print(f"{'Threshold':<15} {'Best Profile':<15} {'Coefficient':<15} {'Change'}")
    print("-" * 60)

    prev_coef = None
    for threshold in thresholds:
        result = results_summary[threshold]
        best = result['best_alternative']
        coef = result['best_coefficient']

        change_str = ""
        if prev_coef is not None:
            change = coef - prev_coef
            change_str = f"{change:+.4f}"

        print(f"{threshold:<15.1f} {best:<15} {coef:<15.6f} {change_str}")
        prev_coef = coef

    # Ranking changes
    print("\n" + "="*80)
    print("RANKING STABILITY ANALYSIS")
    print("="*80)

    print("\nProfiles that appear in Top 5 for ALL thresholds:")

    top5_sets = []
    for threshold in thresholds:
        result = results_summary[threshold]
        top5 = set([r['alternative'] for r in result['ranked_results'][:5]])
        top5_sets.append(top5)

    stable_top5 = top5_sets[0].intersection(*top5_sets[1:])
    if stable_top5:
        print("  " + ", ".join(sorted(stable_top5)))
    else:
        print("  None - rankings are highly sensitive to threshold!")

    print("\nProfiles that change positions significantly:")
    for threshold_idx in range(len(thresholds) - 1):
        t1 = thresholds[threshold_idx]
        t2 = thresholds[threshold_idx + 1]

        # Get rankings
        rank1 = {r['alternative']: r['rank'] for r in results_summary[t1]['ranked_results']}
        rank2 = {r['alternative']: r['rank'] for r in results_summary[t2]['ranked_results']}

        print(f"\n  From threshold {t1} to {t2}:")

        # Find biggest movers
        changes = []
        for profile in rank1.keys():
            change = rank1[profile] - rank2[profile]
            if abs(change) >= 3:  # Significant change
                changes.append((profile, rank1[profile], rank2[profile], change))

        if changes:
            changes.sort(key=lambda x: abs(x[3]), reverse=True)
            for profile, r1, r2, change in changes[:3]:
                direction = "UP" if change > 0 else "DOWN"
                print(f"    {profile}: Rank {r1} -> {r2} ({direction} {abs(change)} positions)")
        else:
            print("    No significant changes (< 3 positions)")

    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    print("\nThe threshold parameter significantly impacts profile rankings by changing")
    print("how skills are evaluated (beneficial vs non-beneficial).")
    print("\nRecommendation: Choose threshold based on your evaluation philosophy:")
    print("  - Lower threshold (2.0-2.5): Lenient, few 'must-have' skills")
    print("  - Medium threshold (3.0-3.5): Balanced approach")
    print("  - Higher threshold (4.0+): Strict, many 'must-have' skills")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_threshold_impact()
