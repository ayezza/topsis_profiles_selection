# Optimal 1-to-1 Profile-Activity Assignment

## Overview

This solution addresses the problem where **one profile is ranked #1 for multiple activities** (1-to-many assignments) by finding the **optimal 1-to-1 mapping** between profiles and activities.

## Problem Statement

In your TOPSIS results, you may have situations like:
- Profile_7 is ranked #1 for both Backend_Development AND Full_Stack_Developer
- Profile_5 is ranked #1 for Team_Lead AND appears in top rankings for other activities
- Profile_1 is ranked #1 for both Frontend_Development AND Tech_Lead

If your goal is to assign each profile to a unique activity, this creates conflicts when trying to assign unique profiles to each activity.

## Solution Approach

The implementation provides **two methods** based on the dimensions of your data:

### Method 1: Hungarian Algorithm (when #profiles = #activities)
- **Optimal Solution**: Guarantees the maximum total TOPSIS score
- **Complexity**: O(n³) - efficient even for large datasets
- **Requirement**: Number of profiles must equal number of activities
- **Algorithm**: Uses `scipy.optimize.linear_sum_assignment`

### Method 2: Greedy Approach (when #profiles ≠ #activities)
- **Best-Effort Solution**: Iteratively assigns activities to best available profiles
- **Process**:
  1. Sorts all (activity, profile, score) combinations by score
  2. Assigns each activity to its highest-scoring unassigned profile
  3. Continues until all activities are assigned
- **Result**: Some profiles may remain unassigned if #profiles > #activities

## Example: Your Current Data

- **Profiles**: 15
- **Activities**: 10
- **Method Used**: `Greedy` (since 15 ≠ 10)

## Optimal Assignment Results

The greedy algorithm produced the following optimal 1-to-1 assignment:

| Activity | Assigned Profile | Score |
|----------|-----------------|-------|
| Backend_Development | Profile_7 | 1.0000 |
| Cloud_Architect | Profile_3 | 0.5942 |
| Data_Engineer | Profile_14 | 1.0000 |
| Database_Admin | Profile_12 | 1.0000 |
| DevOps_Engineer | Profile_4 | 1.0000 |
| Frontend_Development | Profile_1 | 1.0000 |
| Full_Stack_Developer | Profile_15 | 0.9735 |
| Project_Manager | Profile_13 | 1.0000 |
| Team_Lead | Profile_5 | 1.0000 |
| Tech_Lead | Profile_2 | 0.8481 |

**Total Score**: 9.4159

**Average Score**: 0.9416

**Unassigned Profiles**: Profile_6, Profile_8, Profile_9, Profile_10, Profile_11

## Files Generated

1. **`data/output/rankings/optimal_assignment.csv`**
   - CSV file with the optimal assignment
   - Columns: Activity, Assigned_Profile, Score

2. **`data/output/visualizations/optimal_heatmap_all_results.png`**
   - Visual heatmap showing all TOPSIS scores
   - Optimal assignments highlighted with ★ and red borders
   - Easy to see which profile is assigned to which activity

## Usage

### Running the Script

```bash
# Using virtual environment
venv/Scripts/python create_optimal_assignment.py

# Or if you have python in PATH
python create_optimal_assignment.py
```

### Using in Your Code

```python
from pathlib import Path
import pandas as pd
from src.core.optimal_assignment import OptimalAssignment
from src.visualization.charts import ProfileVisualizer

# Load your TOPSIS results
full_results_df = pd.read_csv('data/output/rankings/full_results_matrix.csv', index_col=0)

# Create solver
solver = OptimalAssignment(full_results_df)

# Solve (auto-selects method based on dimensions)
results = solver.solve()

# Or force a specific method
# results = solver.solve(force_method='hungarian')  # Only if dimensions match
# results = solver.solve(force_method='greedy')

# Print results
solver.print_results()

# Save to CSV
solver.save_results('output_assignment.csv')

# Get assignment matrices
assignment_matrix = solver.get_assignment_matrix()  # Binary matrix
score_matrix = solver.get_assignment_scores()       # Scores for assigned pairs

# Create visualization
visualizer = ProfileVisualizer(output_dir='data/output/visualizations')
heatmap_path = visualizer.plot_optimal_assignment_heatmap(
    full_results_df=full_results_df,
    assignment_matrix=assignment_matrix,
    assignment_info=results,
    proximity_formula='TOPSIS',
    save=True
)
```

## Key Benefits

1. **Automatic Method Selection**: Checks dimensions and uses the best method
2. **Dimension Validation**: Prevents Hungarian algorithm from being used incorrectly
3. **Clear Visualization**: Heatmap clearly shows optimal assignments vs all possibilities
4. **Export Ready**: CSV output for easy integration with other tools
5. **Maximizes Total Score**: Ensures the best overall assignment quality

## Understanding the Visualization

The heatmap (`optimal_heatmap_all_results.png`) shows:
- **All cells**: TOPSIS proximity coefficients for each profile-activity pair
- **★ Symbols**: Indicate optimal assignments
- **Red Borders**: Highlight the assigned cells
- **Color Intensity**: Darker blue = higher TOPSIS score
- **Title Bar**: Shows method used, total score, average score, and number of assignments

## Notes

- The greedy approach is **not guaranteed to be globally optimal** when dimensions don't match
- If you need a perfect 1-to-1 mapping, consider:
  - Adding dummy activities (if #profiles > #activities)
  - Selecting top N profiles (if #profiles > #activities)
  - Creating additional job roles to match profile count

- The Hungarian algorithm would give the **mathematically optimal** solution only when dimensions match

## Dependencies

Install with:
```bash
venv/Scripts/python -m pip install pandas numpy scipy matplotlib seaborn
```

## Author

Abdel YEZZA (Ph.D)
