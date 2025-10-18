# TOPSIS Profile Selection - Quick Start Guide

## What You've Built

A powerful system that combines:
- **Profile-Activity Matching** from your profiles_assignment project
- **TOPSIS Algorithm** from your topsis_algorithm project
- **Dynamic Threshold System** - The key innovation!

## Key Innovation: Configurable Threshold

The system uses a **threshold** (default: 3.0, range: 0-5) to intelligently classify skills:

- **Skill Level >= Threshold**: Beneficial criterion → Higher is better
- **Skill Level < Threshold**: Non-beneficial criterion → Lower is acceptable

This means:
- Critical skills (high requirement) favor candidates with strong abilities
- Optional skills (low requirement) don't penalize candidates who lack them

## Quick Test Examples

### 1. Basic Run (Default Settings)
```bash
cd D:\PythonProjects\topsis_profiles_selection
python main.py
```

### 2. Adjust Threshold (Strict Evaluation)
```bash
# With threshold=4.0, more skills become "critical"
python main.py --threshold 4.0
```

### 3. Lenient Evaluation
```bash
# With threshold=2.5, fewer skills are critical
python main.py --threshold 2.5
```

### 4. Single Activity Analysis (Verbose)
```bash
python main.py --activity "Backend_Development" -v
```

### 5. Use Requirement-Based Weights
```bash
# Weights proportional to skill importance
python main.py --weight-strategy requirement_based
```

## Real-World Example: Backend Development

**Activity Requirements:**
- Python: 5 (>= 3.0 threshold) → Beneficial (maximize)
- Leadership: 2 (< 3.0 threshold) → Non-beneficial (minimize)

**Result:**
- Profiles with Python=5 score higher
- Profiles with Leadership=2 are NOT penalized (it's acceptable)

## Output Files

After running, check:
```
data/output/
├── rankings/
│   ├── ranking_matrix.csv              # Top 3 profiles per activity
│   ├── full_results_matrix.csv         # All coefficients
│   └── ranking_Backend_Development.txt # Detailed rankings
└── figures/                            # Visualizations (if libraries installed)
```

## Configuration

Edit [config.json](config.json) to customize:

```json
{
  "threshold_settings": {
    "threshold": 3.0,        // Adjust this!
    "min_threshold": 0.0,
    "max_threshold": 5.0
  },
  "weight_settings": {
    "strategy": "uniform"    // or "requirement_based"
  }
}
```

## Understanding Results

**Proximity Coefficient (0 to 1):**
- **1.0** = Perfect match with ideal solution
- **0.5** = Moderate match
- **0.0** = Worst possible match

Example output:
```
Backend_Development: Dev10 (0.8115) - 81.15% match
```

Dev10 is 81% close to the ideal profile for backend development!

## Sample Data

The system includes sample data:
- **15 Profiles** (Dev1-Dev15)
- **10 Activities** (Backend_Development, Team_Lead, etc.)
- **10 Skills** (Python, Java, SQL, Communication, etc.)

Each skill rated 0-5.

## Threshold Impact Examples

### Threshold = 3.0 (Default)
For Backend_Development (Python=5, Leadership=2):
- 8 skills are Beneficial (80%)
- 2 skills are Non-beneficial (20%)

### Threshold = 4.0 (Strict)
For Team_Lead (Communication=5, Leadership=5):
- 5 skills are Beneficial (50%)
- 5 skills are Non-beneficial (50%)

## Command-Line Options

```bash
python main.py [OPTIONS]

Key Options:
  --threshold FLOAT         Skill level threshold (0-5)
  --activity NAME          Process single activity
  --weight-strategy TYPE    uniform | requirement_based
  -v, --verbose            Show detailed analysis
  --viz                    Generate visualizations*
  -o DIR                   Output directory

*Requires: pip install matplotlib seaborn
```

## Next Steps

1. **Customize Input Data:**
   - Edit `data/input/profiles.csv` with your profiles
   - Edit `data/input/activities.csv` with your activities

2. **Experiment with Thresholds:**
   ```bash
   python main.py --threshold 2.0
   python main.py --threshold 3.5
   python main.py --threshold 4.5
   ```

3. **Compare Weight Strategies:**
   ```bash
   python main.py --weight-strategy uniform
   python main.py --weight-strategy requirement_based
   ```

4. **Install Visualization Libraries:**
   ```bash
   pip install matplotlib seaborn
   python main.py --viz
   ```

## Architecture

```
Input: Profiles + Activities + Threshold
   ↓
SkillTransformer: Classify skills (beneficial/non-beneficial)
   ↓
TOPSIS Engine: Calculate proximity coefficients
   ↓
Ranking: Sort profiles by coefficient
   ↓
Output: Rankings + Visualizations
```

## Key Files

- [main.py](main.py) - Main CLI interface
- [config.json](config.json) - Configuration
- [src/core/topsis_engine.py](src/core/topsis_engine.py) - TOPSIS algorithm
- [src/core/skill_transformer.py](src/core/skill_transformer.py) - Threshold logic
- [src/core/profile_processor.py](src/core/profile_processor.py) - Main processor
- [README.md](README.md) - Full documentation

## Troubleshooting

**Q: Visualization error?**
A: Install libraries: `pip install matplotlib seaborn`

**Q: ModuleNotFoundError?**
A: Make sure you're in the project directory

**Q: Want different skill scale?**
A: Adjust min_threshold and max_threshold in config.json

## Success Indicators

You know it's working when you see:
```
Best Profile for Each Activity
Dev10: 0.811529 (81.15%)
```

And output files in `data/output/rankings/`

## Support

For questions or issues, refer to the full [README.md](README.md)

---

**Author:** Abdel YEZZA (Ph.D)
**Version:** 1.0.0
**Project:** Combined TOPSIS Profile Selection System
