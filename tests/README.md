# Tests Directory

This directory contains test scripts for validating the TOPSIS Profile Selection System functionality.

## Test Scripts

### 1. **test_formula_comparison.py**
Compares the standard vs variant proximity formulas to demonstrate how they produce different assignment results.

**Usage:**
```bash
# From project root
python tests/test_formula_comparison.py

# Or from tests directory
cd tests
python test_formula_comparison.py
```

**Requirements:**
- Equal-dimension datasets: `data/input/profiles_2.csv` and `data/input/activities_2.csv`

**Output:**
- Comparison report showing differences in assignments between formulas
- Statistics on score ranges and assignment changes

---

### 2. **test_hungarian_assignment.py**
Tests the Hungarian algorithm with equal-dimension datasets (10×10).

**Usage:**
```bash
# From project root
python tests/test_hungarian_assignment.py

# Or from tests directory
cd tests
python test_hungarian_assignment.py
```

**Requirements:**
- Equal-dimension datasets: `data/input/profiles_2.csv` and `data/input/activities_2.csv`

**Output:**
- TOPSIS rankings
- Optimal assignment results
- Comparison with top-1 rankings
- Saved results in `data/output_test/`
- Heatmap visualization (if matplotlib/seaborn installed)

---

### 3. **test_threshold_comparison.py**
Compares results using different threshold values.

**Usage:**
```bash
# From project root
python tests/test_threshold_comparison.py

# Or from tests directory
cd tests
python test_threshold_comparison.py
```

---

### 4. **example_heatmap_fontsize.py**
Demonstrates how to control annotation font sizes in heatmaps.

**Usage:**
```bash
# From project root
python tests/example_heatmap_fontsize.py

# Or from tests directory
cd tests
python example_heatmap_fontsize.py
```

**Interactive Options:**
1. Generate heatmaps with different font sizes (requires data)
2. Show code examples only

---

## Running All Tests

To run all tests sequentially:

```bash
# From project root
python tests/test_formula_comparison.py
python tests/test_hungarian_assignment.py
python tests/test_threshold_comparison.py
```

---

## Requirements

All test scripts require:
- Python 3.8+
- numpy, pandas
- scipy (for Hungarian algorithm)
- matplotlib, seaborn (optional, for visualizations)

Install dependencies:
```bash
pip install numpy pandas scipy matplotlib seaborn
```

---

## Test Data

Tests use datasets from `data/input/`:
- `profiles_2.csv` - 10 profiles with 10 skills
- `activities_2.csv` - 10 activities with 10 skill requirements

These datasets have equal dimensions (10×10) specifically for testing the Hungarian algorithm.

---

## Output Locations

Test outputs are saved to:
- `data/output_test/` - Test-specific results
- `data/output_fontsize_demo/` - Font size example outputs

---

## Notes

- All tests are self-contained and can be run independently
- Tests automatically handle path resolution (work from any directory)
- Tests use `sys.path` manipulation to import from `src/` directory
- No installation required - tests work directly from the repository

---

Author: Abdel YEZZA (Ph.D)
