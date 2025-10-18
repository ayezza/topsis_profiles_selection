# TOPSIS Profile Selection System

A comprehensive system for profile evaluation and ranking using the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) algorithm with configurable skill-level thresholds.

**Author:** Abdel YEZZA (Ph.D)

## Overview

This project combines two powerful concepts:
1. **Profile-Activity Matching** - Matching profiles to activities based on competencies
2. **TOPSIS Algorithm** - Multi-criteria decision analysis for ranking

### Key Innovation: Dynamic Threshold System

The system uses a **configurable threshold** to determine how skills are evaluated:

- **Skills >= Threshold**: Treated as **Beneficial** criteria (higher is better)
- **Skills < Threshold**: Treated as **Non-Beneficial** criteria (lower is acceptable)

This approach allows flexible evaluation where some skills are critical (must be maximized) while others are optional (don't penalize lack of proficiency).

## Features

- **Configurable Threshold System** (min_threshold to max_threshold)
- **Multiple Weight Strategies** (uniform, requirement-based, custom)
- **Two TOPSIS Proximity Formulas** (standard and variant)
- **Comprehensive Visualizations** (heatmaps, bar charts, radar plots, distance analysis)
- **Flexible Input Formats** (CSV files with profiles and activities)
- **Command-Line Interface** with extensive options
- **Detailed Results Export** (rankings, matrices, analysis reports)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
cd D:\PythonProjects\topsis_profiles_selection
pip install -r requirements.txt
```

## Quick Start

### 1. Basic Usage (Default Configuration)

```bash
python main.py
```

This will:
- Load profiles and activities from `data/input/`
- Use threshold = 3.0 (configurable between 0-5)
- Apply uniform weights to all skills
- Generate rankings for all activities
- Save results to `data/output/`

### 2. Custom Threshold

```bash
python main.py --threshold 3.5
```

### 3. Single Activity Processing

```bash
python main.py --activity "Backend_Development"
```

### 4. Verbose Mode with Visualizations

```bash
python main.py -v --viz
```

### 5. Custom Weight Strategy

```bash
python main.py --weight-strategy requirement_based
```

### 6. Custom Input Files

```bash
python main.py --profiles data/input/profiles.csv --activities data/input/activities.csv
```

## Configuration

Edit `config.json` to customize:

```json
{
  "threshold_settings": {
    "threshold": 3.0,
    "min_threshold": 0.0,
    "max_threshold": 5.0
  },
  "topsis_settings": {
    "proximity_formula": "standard"
  },
  "weight_settings": {
    "strategy": "uniform"
  }
}
```

## Input Data Format

### Profiles CSV (`data/input/profiles.csv`)

```csv
Profile,Python,Java,SQL,Communication,Leadership
Dev1,5,3,4,4,2
Dev2,4,5,3,5,4
Dev3,3,2,5,3,3
```

- **First column**: Profile names/IDs
- **Other columns**: Skill levels (0-5 scale)

### Activities CSV (`data/input/activities.csv`)

```csv
Activity,Python,Java,SQL,Communication,Leadership
Backend_Development,5,4,5,3,2
Frontend_Development,3,5,2,4,2
Team_Lead,3,3,3,5,5
```

- **First column**: Activity names
- **Other columns**: Required skill levels (same skills as profiles)
- **Important**: Skill columns must match between profiles and activities

## How It Works

### 1. Skill Transformation

For each activity, required skill levels are analyzed:

```
Example: Backend Development requires Python=5, Leadership=2

Python (5 >= 3): Beneficial criterion → Higher Python skills preferred
Leadership (2 < 3): Non-beneficial criterion → Lower Leadership acceptable
```

### 2. TOPSIS Algorithm

The system applies TOPSIS in 5 steps:

1. **Normalize** the decision matrix (profiles × skills)
2. **Apply weights** to normalized values
3. **Determine ideal solutions** (best and worst)
4. **Calculate distances** from each profile to ideal solutions
5. **Calculate proximity coefficients** (higher = better match)

### 3. Ranking

Profiles are ranked by proximity coefficient (0 to 1):
- **1.0** = Perfect match with ideal solution
- **0.0** = Closest to worst solution

## Output

### Directory Structure

```
data/output/
├── rankings/
│   ├── ranking_matrix.csv              # Top 3 profiles per activity
│   ├── full_results_matrix.csv         # All proximity coefficients
│   ├── ranking_Backend_Development.txt # Detailed ranking per activity
│   └── ...
└── figures/
    ├── heatmap_all_results.png         # Overview heatmap
    ├── ranking_bar_*.png               # Bar charts per activity
    ├── radar_*.png                     # Skill comparison radar charts
    ├── distances_*.png                 # Distance analysis
    └── criteria_distribution.png       # Threshold analysis
```

### Sample Output

```
================================================================================
PROFILE SELECTION SUMMARY - TOPSIS Results
================================================================================

Best Profile for Each Activity
--------------------------------------------------------------------------------
Activity                       Best Profile                   Coefficient
--------------------------------------------------------------------------------
Backend_Development            Dev10                          0.876543
Frontend_Development           Dev2                           0.854321
Team_Lead                      Dev14                          0.891234
...
```

## Command-Line Options

```bash
usage: main.py [-h] [-c CONFIG] [--profiles PROFILES] [--activities ACTIVITIES]
               [--threshold THRESHOLD] [--min-threshold MIN_THRESHOLD]
               [--max-threshold MAX_THRESHOLD] [--activity ACTIVITY]
               [--weight-strategy {uniform,requirement_based}]
               [--proximity-formula {standard,variant}] [-v] [--viz] [-o OUTPUT]

Options:
  -h, --help            Show help message
  -c, --config          Configuration file path
  --profiles            Profiles CSV file path
  --activities          Activities CSV file path
  --threshold           Skill level threshold (default: 3.0)
  --min-threshold       Minimum skill level (default: 0.0)
  --max-threshold       Maximum skill level (default: 5.0)
  --activity            Process only specific activity
  --weight-strategy     Weight generation strategy
  --proximity-formula   TOPSIS proximity formula
  -v, --verbose         Enable verbose output
  --viz, --visualize    Generate visualizations
  -o, --output          Output directory
```

## Weight Strategies

### 1. Uniform Weights (Default)

All skills have equal importance:
```
weights = [0.1, 0.1, 0.1, ..., 0.1]
```

### 2. Requirement-Based Weights

Skills with higher required levels get higher weights:
```
weights proportional to required_levels
```

### 3. Custom Weights

Define specific weights in config.json:
```json
{
  "weight_settings": {
    "strategy": "custom",
    "custom_weights": [0.3, 0.2, 0.2, 0.1, 0.1, 0.1]
  }
}
```

## TOPSIS Formulas

### Standard Formula (Default)

```
S*[i] = E-[i] / (E+[i] + E-[i])
```
- Values between 0 and 1
- Easier to interpret
- Smaller differences between alternatives

### Variant Formula

```
        ⎧  E-
        ⎪ ───    for E+ ≠ 0
S*[i] = ⎨  E+
        ⎪  E-
        ⎪ ─────  for E+ = 0
        ⎩ max(E+)
```

Where:
- **E-** = Distance to worst ideal solution
- **E+** = Distance to best ideal solution
- **max(E+)** = Maximum distance to best across all alternatives

Characteristics:
- Better discrimination between alternatives
- Handles edge cases when distance to best is zero
- No normalization required
- Higher values indicate better match

## Examples

### Example 1: Find Best Backend Developer

```bash
python main.py --activity "Backend_Development" -v
```

This will show detailed analysis of which profiles best match the backend development requirements.

### Example 2: Adjust Threshold for Different Standards

```bash
# Strict evaluation (threshold = 4.0)
python main.py --threshold 4.0

# Lenient evaluation (threshold = 2.5)
python main.py --threshold 2.5
```

Higher thresholds mean more skills are treated as "must have" (beneficial).

### Example 3: Generate Complete Report with Visualizations

```bash
python main.py -v --viz --output reports/analysis_2024
```

## Project Structure

```
topsis_profiles_selection/
├── main.py                          # Main CLI entry point
├── config.json                      # Configuration file
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── src/
│   ├── core/
│   │   ├── topsis_engine.py        # TOPSIS algorithm implementation
│   │   ├── skill_transformer.py    # Threshold-based transformation
│   │   └── profile_processor.py    # Main processing logic
│   └── visualization/
│       └── charts.py                # Visualization generation
└── data/
    ├── input/
    │   ├── profiles.csv            # Sample profiles data
    │   └── activities.csv          # Sample activities data
    └── output/
        ├── rankings/               # Results and rankings
        └── figures/                # Generated visualizations
```

## API Usage (Python)

```python
from pathlib import Path
import sys
sys.path.insert(0, 'src')

from core.profile_processor import ProfileProcessor, load_profiles_from_csv, load_activities_from_csv

# Load data
profiles_df = load_profiles_from_csv('data/input/profiles.csv')
activities_df = load_activities_from_csv('data/input/activities.csv')

# Create processor
processor = ProfileProcessor(
    profiles_df=profiles_df,
    activities_df=activities_df,
    threshold=3.0,
    min_threshold=0.0,
    max_threshold=5.0,
    proximity_formula='standard'
)

# Process all activities
results = processor.process_all_activities(
    weight_strategy='uniform',
    verbose=True
)

# Get specific activity results
backend_results = processor.results['Backend_Development']
best_profile = backend_results['best_alternative']
print(f"Best profile for Backend Development: {best_profile}")

# Save results
processor.save_results(Path('data/output'))
```

## Advanced Features

### 1. Skill Transformer Analysis

```python
from core.skill_transformer import SkillTransformer
import numpy as np

transformer = SkillTransformer(threshold=3.0)
required_skills = np.array([5, 4, 3, 2, 1])
skill_names = ['Python', 'Java', 'SQL', 'Docs', 'Testing']

transformer.print_criteria_analysis(skill_names, required_skills)
```

### 2. Custom Weights Generation

```python
from core.skill_transformer import WeightGenerator
import numpy as np

# Uniform weights
weights = WeightGenerator.uniform_weights(n_criteria=5)

# Requirement-based weights
required_levels = np.array([5, 4, 3, 2, 1])
weights = WeightGenerator.requirement_based_weights(required_levels, threshold=3.0)

# Hybrid weights
importance_scores = [0.4, 0.3, 0.2, 0.05, 0.05]
weights = WeightGenerator.hybrid_weights(required_levels, importance_scores, alpha=0.5)
```

### 3. Visualization Customization

```python
from visualization.charts import ProfileVisualizer
from pathlib import Path

visualizer = ProfileVisualizer(
    output_dir=Path('data/output/figures'),
    dpi=300
)

# Generate all visualizations
saved_files = visualizer.generate_all_visualizations(
    processor=processor,
    top_n=10
)
```

## References

### TOPSIS Algorithm

- Hwang, C.L., & Yoon, K. (1981). Multiple Attribute Decision Making: Methods and Applications. Springer-Verlag.
- Yoon, K.P., & Hwang, C.L. (1995). Multiple Attribute Decision Making: An Introduction. SAGE Publications.

### Multi-Criteria Decision Analysis

- Triantaphyllou, E. (2000). Multi-criteria Decision Making Methods: A Comparative Study. Kluwer Academic Publishers.

## License

This project combines concepts from:
- Profile Assignment System (MCAP) - Abdel YEZZA (Ph.D)
- TOPSIS Algorithm Implementation - Abdel YEZZA (Ph.D)

## Contributing

For issues, suggestions, or contributions, please contact the author.

## Author

**Abdel YEZZA, Ph.D**

Combined System: TOPSIS Profile Selection
- Profile Matching + TOPSIS Algorithm
- Dynamic Threshold System
- Multi-Criteria Decision Analysis

---

**Version:** 1.0.0
**Last Updated:** 2024
