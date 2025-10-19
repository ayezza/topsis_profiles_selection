# Quick Start Guide - Optimal Assignment

## Choose Your Scenario

### Scenario 1: Equal Dimensions (e.g., 10 profiles, 10 activities)
**Method Used**: Hungarian Algorithm (Optimal)

```bash
# Use profiles_2.csv and activities_2.csv (or any equal-dimension files)
venv/Scripts/python test_hungarian_assignment.py
```

**Result**:
- ✓ Mathematically optimal 1-to-1 assignment
- ✓ Maximum total TOPSIS score
- ✓ No unassigned profiles

---

### Scenario 2: Unequal Dimensions (e.g., 15 profiles, 10 activities)
**Method Used**: Greedy Approach (Best-effort)

```bash
# Use profiles_1.csv and activities_1.csv (or any unequal-dimension files)
venv/Scripts/python create_optimal_assignment.py
```

**Result**:
- ✓ Best-effort assignment
- ✓ All activities assigned
- ✓ Some profiles may remain unassigned

---

## Output Files (Both Scenarios)

### 1. Assignment CSV
**Location**: `data/output[_test]/rankings/optimal_assignment[_hungarian].csv`

```csv
Activity,Assigned_Profile,Score
Backend_Development,Profile_7,0.7185
Frontend_Development,Profile_2,0.6236
...
```

### 2. Visual Heatmap
**Location**: `data/output[_test]/visualizations/optimal_heatmap_all_results.png`

Shows:
- All TOPSIS scores (color-coded)
- ★ Optimal assignments marked
- Red borders around assigned cells

---

## Using in Your Own Code

```python
from pathlib import Path
import pandas as pd
from src.core.optimal_assignment import OptimalAssignment
from src.visualization.charts import ProfileVisualizer

# Load your TOPSIS results
results_df = pd.read_csv('path/to/full_results_matrix.csv', index_col=0)

# Create solver and solve automatically
solver = OptimalAssignment(results_df)
results = solver.solve()  # Auto-selects Hungarian or Greedy

# Print and save
solver.print_results()
solver.save_results('assignment.csv')

# Create visualization
visualizer = ProfileVisualizer(output_dir='output')
visualizer.plot_optimal_assignment_heatmap(
    full_results_df=results_df,
    assignment_matrix=solver.get_assignment_matrix(),
    assignment_info=results,
    save=True
)
```

---

## Decision Tree

```
Do #profiles = #activities?
│
├─ YES → Hungarian Algorithm
│         ├─ Optimal solution
│         └─ No unassigned profiles
│
└─ NO → Greedy Approach
        ├─ Best-effort solution
        └─ Some profiles may be unassigned
```

---

## Common Use Cases

### Use Case 1: Job Assignment
**Scenario**: 10 employees, 10 projects
**Use**: `test_hungarian_assignment.py` (Hungarian)
**Result**: Each employee assigned to exactly one project (optimal)

### Use Case 2: Talent Pool
**Scenario**: 15 candidates, 10 positions
**Use**: `create_optimal_assignment.py` (Greedy)
**Result**: Best 10 candidates assigned, 5 remain in reserve

---

## Troubleshooting

### Issue: "Dimensions mismatch" error
**Solution**: This is expected when profiles ≠ activities. The system will automatically use Greedy approach.

### Issue: "ModuleNotFoundError: seaborn"
**Solution**:
```bash
venv/Scripts/python -m pip install seaborn scipy
```

### Issue: Star symbols (★) not showing in heatmap
**Solution**: This is just a font warning. The heatmap still works correctly!

---

## Files Overview

| File | Purpose |
|------|---------|
| `create_optimal_assignment.py` | Main script (any dimensions) |
| `test_hungarian_assignment.py` | Test with equal dimensions |
| `src/core/optimal_assignment.py` | Core solver logic |
| `src/visualization/charts.py` | Heatmap visualization |
| `OPTIMAL_ASSIGNMENT_README.md` | Full documentation |
| `HUNGARIAN_TEST_RESULTS.md` | Test results analysis |

---

## Key Takeaways

1. **Equal dimensions** = Hungarian Algorithm = **Optimal**
2. **Unequal dimensions** = Greedy Approach = **Best-effort**
3. System **auto-detects** and selects the best method
4. Both methods produce:
   - Assignment CSV file
   - Visual heatmap with highlighted assignments
   - Detailed console output

---

## Need Help?

- Read: `OPTIMAL_ASSIGNMENT_README.md` for detailed explanation
- See: `HUNGARIAN_TEST_RESULTS.md` for example results
- Check: CSV and PNG outputs in `data/output[_test]/` folders
