"""
Visualization Module
Generate charts and graphs for TOPSIS profile selection results
Author: Abdel YEZZA (Ph.D)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import seaborn as sns


class ProfileVisualizer:
    """
    Create visualizations for TOPSIS profile selection results.
    """

    def __init__(self, output_dir: Path, dpi: int = 300, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize visualizer.

        Args:
            output_dir: Directory to save figures
            dpi: Resolution for saved figures
            style: Matplotlib style
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = dpi

        # Set style
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

        # Set color palette
        self.colors = sns.color_palette("husl", 15)

    def plot_ranking_bar_chart(
        self,
        results: Dict,
        activity_name: str,
        top_n: int = 10,
        save: bool = True
    ) -> Optional[Path]:
        """
        Create bar chart showing ranking for a single activity.

        Args:
            results: Results dictionary from ProfileProcessor
            activity_name: Name of the activity
            top_n: Number of top profiles to display
            save: If True, save figure

        Returns:
            Path to saved figure if save=True, else None
        """
        ranked_results = results['ranked_results'][:top_n]

        profiles = [r['alternative'] for r in ranked_results]
        coefficients = [r['coefficient'] for r in ranked_results]

        fig, ax = plt.subplots(figsize=(12, 6))

        bars = ax.barh(profiles, coefficients, color=self.colors[:len(profiles)])

        ax.set_xlabel('Proximity Coefficient', fontsize=12, fontweight='bold')
        ax.set_ylabel('Profile', fontsize=12, fontweight='bold')
        ax.set_title(f'TOPSIS Ranking: {activity_name}\nTop {top_n} Profiles',
                    fontsize=14, fontweight='bold')

        # Add value labels on bars
        for i, (bar, coef) in enumerate(zip(bars, coefficients)):
            ax.text(coef + 0.01, bar.get_y() + bar.get_height()/2,
                   f'{coef:.4f}',
                   va='center', fontsize=9)

        ax.set_xlim(0, 1.0)
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()

        if save:
            safe_name = activity_name.replace(' ', '_').replace('/', '_')
            filename = self.output_dir / f'ranking_bar_{safe_name}.png'
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            return filename
        else:
            plt.show()
            return None

    def plot_comparison_heatmap(
        self,
        full_results_df: pd.DataFrame,
        save: bool = True
    ) -> Optional[Path]:
        """
        Create heatmap showing all profiles vs all activities.

        Args:
            full_results_df: DataFrame with activities as index, profiles as columns
            save: If True, save figure

        Returns:
            Path to saved figure if save=True, else None
        """

        # Add ranking annotations
        full_results_df_ranked = full_results_df.rank(ascending=False, axis=1, method='min').astype(int)
        annot_df = full_results_df.round(3).astype(str) + '\n(#' + full_results_df_ranked.astype(str) + ')'

        fig, ax = plt.subplots(figsize=(16, 10))

        sns.heatmap(
            full_results_df,
            annot=annot_df,
            fmt='',
            cmap='YlGnBu',
            cbar_kws={'label': 'Proximity Coefficient'},
            ax=ax,
            linewidths=0.5
        )

        ax.set_title('TOPSIS Results Heatmap\nProfiles vs Activities',
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Profile', fontsize=12, fontweight='bold')
        ax.set_ylabel('Activity', fontsize=12, fontweight='bold')

        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()

        if save:
            filename = self.output_dir / 'heatmap_all_results.png'
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            return filename
        else:
            plt.show()
            return None

    def plot_radar_chart(
        self,
        profiles_df: pd.DataFrame,
        profile_names: List[str],
        activity_name: str,
        save: bool = True
    ) -> Optional[Path]:
        """
        Create radar chart comparing skill levels of top profiles.

        Args:
            profiles_df: DataFrame with profile skills
            profile_names: List of profile names to compare
            activity_name: Name of the activity
            save: If True, save figure

        Returns:
            Path to saved figure if save=True, else None
        """
        # Get data for selected profiles
        selected_profiles = profiles_df.loc[profile_names]

        # Skill names
        skills = list(profiles_df.columns)
        n_skills = len(skills)

        # Compute angle for each skill
        angles = np.linspace(0, 2 * np.pi, n_skills, endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

        for i, profile_name in enumerate(profile_names):
            values = selected_profiles.loc[profile_name].tolist()
            values += values[:1]  # Complete the circle

            ax.plot(angles, values, 'o-', linewidth=2,
                   label=profile_name, color=self.colors[i])
            ax.fill(angles, values, alpha=0.15, color=self.colors[i])

        # Set labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(skills, fontsize=9)
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=8)
        ax.grid(True)

        ax.set_title(f'Skill Comparison - {activity_name}\nTop Profiles',
                    fontsize=14, fontweight='bold', pad=20)

        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.tight_layout()

        if save:
            safe_name = activity_name.replace(' ', '_').replace('/', '_')
            filename = self.output_dir / f'radar_{safe_name}.png'
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            return filename
        else:
            plt.show()
            return None

    def plot_distance_comparison(
        self,
        results: Dict,
        activity_name: str,
        top_n: int = 10,
        save: bool = True
    ) -> Optional[Path]:
        """
        Plot comparison of distances to ideal best and worst solutions.

        Args:
            results: Results dictionary from ProfileProcessor
            activity_name: Name of the activity
            top_n: Number of top profiles to display
            save: If True, save figure

        Returns:
            Path to saved figure if save=True, else None
        """
        ranked_results = results['ranked_results'][:top_n]

        profiles = [r['alternative'] for r in ranked_results]
        dist_best = [r['distance_to_best'] for r in ranked_results]
        dist_worst = [r['distance_to_worst'] for r in ranked_results]

        x = np.arange(len(profiles))
        width = 0.35

        fig, ax = plt.subplots(figsize=(14, 6))

        bars1 = ax.bar(x - width/2, dist_best, width, label='Distance to Best (E+)',
                      color='coral', alpha=0.8)
        bars2 = ax.bar(x + width/2, dist_worst, width, label='Distance to Worst (E-)',
                      color='skyblue', alpha=0.8)

        ax.set_xlabel('Profile', fontsize=12, fontweight='bold')
        ax.set_ylabel('Euclidean Distance', fontsize=12, fontweight='bold')
        ax.set_title(f'Distance Analysis: {activity_name}\nTop {top_n} Profiles',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(profiles, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        if save:
            safe_name = activity_name.replace(' ', '_').replace('/', '_')
            filename = self.output_dir / f'distances_{safe_name}.png'
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            return filename
        else:
            plt.show()
            return None

    def plot_criteria_distribution(
        self,
        activities_df: pd.DataFrame,
        threshold: float,
        save: bool = True
    ) -> Optional[Path]:
        """
        Plot distribution of beneficial vs non-beneficial criteria across activities.

        Args:
            activities_df: DataFrame with activity requirements
            threshold: Skill threshold
            save: If True, save figure

        Returns:
            Path to saved figure if save=True, else None
        """
        beneficial_counts = []
        non_beneficial_counts = []

        for activity_name in activities_df.index:
            required_skills = activities_df.loc[activity_name].values
            n_beneficial = np.sum(required_skills >= threshold)
            n_non_beneficial = np.sum(required_skills < threshold)

            beneficial_counts.append(n_beneficial)
            non_beneficial_counts.append(n_non_beneficial)

        activities = activities_df.index.tolist()
        x = np.arange(len(activities))
        width = 0.35

        fig, ax = plt.subplots(figsize=(14, 6))

        bars1 = ax.bar(x - width/2, beneficial_counts, width,
                      label=f'Beneficial (>= {threshold})',
                      color='green', alpha=0.7)
        bars2 = ax.bar(x + width/2, non_beneficial_counts, width,
                      label=f'Non-Beneficial (< {threshold})',
                      color='orange', alpha=0.7)

        ax.set_xlabel('Activity', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Skills', fontsize=12, fontweight='bold')
        ax.set_title(f'Criteria Type Distribution by Activity\nThreshold = {threshold}',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(activities, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        if save:
            filename = self.output_dir / 'criteria_distribution.png'
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            return filename
        else:
            plt.show()
            return None

    def plot_ranking_overview(
        self,
        ranking_matrix_df: pd.DataFrame,
        save: bool = True
    ) -> Optional[Path]:
        """
        Create overview visualization of ranking matrix.

        Args:
            ranking_matrix_df: DataFrame with ranking matrix
            save: If True, save figure

        Returns:
            Path to saved figure if save=True, else None
        """
        fig, ax = plt.subplots(figsize=(14, 8))

        # Extract data for visualization
        activities = ranking_matrix_df['Activity'].tolist()
        n_activities = len(activities)
        n_ranks = len([col for col in ranking_matrix_df.columns if col.startswith('Rank')])

        # Create text table
        ax.axis('tight')
        ax.axis('off')

        table_data = []
        for _, row in ranking_matrix_df.iterrows():
            row_data = [row['Activity']]
            for i in range(1, n_ranks + 1):
                rank_col = f'Rank {i}'
                if rank_col in row:
                    row_data.append(row[rank_col])
                else:
                    row_data.append('')
            table_data.append(row_data)

        headers = ['Activity'] + [f'Rank {i}' for i in range(1, n_ranks + 1)]

        table = ax.table(
            cellText=table_data,
            colLabels=headers,
            cellLoc='left',
            loc='center',
            colWidths=[0.2] + [0.27] * n_ranks
        )

        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)

        # Style header
        for i in range(len(headers)):
            cell = table[(0, i)]
            cell.set_facecolor('#4CAF50')
            cell.set_text_props(weight='bold', color='white')

        # Alternate row colors
        for i in range(1, len(table_data) + 1):
            for j in range(len(headers)):
                cell = table[(i, j)]
                if i % 2 == 0:
                    cell.set_facecolor('#f0f0f0')
                else:
                    cell.set_facecolor('white')

        ax.set_title('TOPSIS Profile Selection - Ranking Overview\nTop Profiles per Activity',
                    fontsize=16, fontweight='bold', pad=20)

        plt.tight_layout()

        if save:
            filename = self.output_dir / 'ranking_overview.png'
            plt.savefig(filename, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            return filename
        else:
            plt.show()
            return None

    def generate_all_visualizations(
        self,
        processor,
        top_n: int = 10
    ) -> List[Path]:
        """
        Generate all visualizations for the processed results.

        Args:
            processor: ProfileProcessor instance with results
            top_n: Number of top profiles for individual charts

        Returns:
            List of paths to generated figures
        """
        saved_files = []

        print("\n  Generating visualizations...")

        # 1. Heatmap of all results
        print("    - Creating heatmap...")
        full_results = processor.get_full_results_matrix()
        file_path = self.plot_comparison_heatmap(full_results, save=True)
        if file_path:
            saved_files.append(file_path)

        # 2. Ranking overview
        print("    - Creating ranking overview...")
        ranking_matrix = processor.get_ranking_matrix(top_n=3)
        file_path = self.plot_ranking_overview(ranking_matrix, save=True)
        if file_path:
            saved_files.append(file_path)

        # 3. Criteria distribution
        print("    - Creating criteria distribution...")
        file_path = self.plot_criteria_distribution(
            processor.activities_df,
            processor.threshold,
            save=True
        )
        if file_path:
            saved_files.append(file_path)

        # 4. Individual activity charts (bar, distance, radar)
        for i, (activity_name, results) in enumerate(processor.results.items()):
            print(f"    - Creating charts for activity {i+1}/{len(processor.results)}: {activity_name}")

            # Bar chart
            file_path = self.plot_ranking_bar_chart(results, activity_name, top_n=top_n, save=True)
            if file_path:
                saved_files.append(file_path)

            # Distance comparison
            file_path = self.plot_distance_comparison(results, activity_name, top_n=top_n, save=True)
            if file_path:
                saved_files.append(file_path)

            # Radar chart for top 5
            top_profiles = [r['alternative'] for r in results['ranked_results'][:5]]
            file_path = self.plot_radar_chart(
                processor.profiles_df,
                top_profiles,
                activity_name,
                save=True
            )
            if file_path:
                saved_files.append(file_path)

        print(f"\n  Generated {len(saved_files)} visualization files")

        return saved_files
