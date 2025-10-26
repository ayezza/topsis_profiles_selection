# Performance Testing Guide for TOPSIS Profile Selection System

**Author:** Abdel YEZZA (Ph.D)
**Date:** October 2025

---

## Overview

This guide explains how to generate large random datasets and benchmark the performance of the TOPSIS Profile Selection System.

## Tools Created

### 1. **Data Generator** (`generate_large_dataset.py`)

Generates random profiles and activities datasets for stress testing.

#### Features:
- Configurable dimensions (profiles × activities × skills)
- Realistic data distribution (normal distribution with configurable parameters)
- Random seed support for reproducibility
- Generates CSV files compatible with main.py

#### Usage:

```bash
# Generate 1000×1000 dataset with 50 skills
python generate_large_dataset.py --profiles 1000 --activities 1000 --skills 50

# Short form
python generate_large_dataset.py -p 500 -a 500 -s 30

# Custom output directory and prefix
python generate_large_dataset.py -p 100 -a 100 -s 20 --output data/test --prefix test_100
```

#### Parameters:

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `--profiles` | `-p` | 1000 | Number of profiles to generate |
| `--activities` | `-a` | 1000 | Number of activities to generate |
| `--skills` | `-s` | 50 | Number of skills per profile/activity |
| `--output` | `-o` | `data/input` | Output directory |
| `--prefix` | | `large` | Filename prefix |
| `--seed` | | 42 | Random seed for reproducibility |

#### Output:

- `{prefix}_profiles.csv` - Profiles with random skill levels (0.0-5.0)
- `{prefix}_activities.csv` - Activities with random requirements (0.0-5.0)

---

### 2. **Simple Benchmark Tool** (`run_benchmark_simple.py`)

Times the execution of main.py with large datasets.

#### Usage:

```bash
# Benchmark with assignment (Hungarian algorithm)
python run_benchmark_simple.py \
    --profiles data/input/large_1000_profiles.csv \
    --activities data/input/large_1000_activities.csv

# Without assignment
python run_benchmark_simple.py \
    --profiles data/input/large_1000_profiles.csv \
    --activities data/input/large_1000_activities.csv \
    --no-assignment
```

#### Output:

```
================================================================================
BENCHMARK RESULTS
================================================================================
Total execution time: 245.67 seconds (4.09 minutes)
Exit code: 0
================================================================================
```

---

### 3. **Advanced Benchmark Suite** (`benchmark_performance.py`)

Comprehensive performance testing with memory usage tracking and multiple test configurations.

#### Features:
- Multiple dataset sizes in one run
- Memory usage tracking (peak RAM)
- Detailed timing breakdown (data generation, initialization, TOPSIS, assignment)
- Comparison report generation
- CSV export of results

#### Usage:

```bash
# Run predefined benchmark suite
python benchmark_performance.py
```

The script will prompt you before running tests.

#### Predefined Test Sizes:

1. **Small**: 100×100 with 20 skills (~2,000 data points)
2. **Medium**: 500×500 with 30 skills (~30,000 data points)
3. **Large**: 1000×1000 with 50 skills (~100,000 data points)

#### Output Files:

- `data/benchmark/benchmark_results.csv` - Detailed results in CSV format
- `data/benchmark/benchmark_report.txt` - Human-readable report

---

## Quick Start: 1000×1000 Test

### Step 1: Generate Data

```bash
python generate_large_dataset.py --profiles 1000 --activities 1000 --skills 50 --prefix large_1000
```

**Output:**
- `data/input/large_1000_profiles.csv` (1000 profiles × 50 skills)
- `data/input/large_1000_activities.csv` (1000 activities × 50 skills)
- Total: ~100,000 data points

### Step 2: Run Benchmark

```bash
python run_benchmark_simple.py \
    --profiles data/input/large_1000_profiles.csv \
    --activities data/input/large_1000_activities.csv
```

### Step 3: View Results

The system will:
1. Load the 1000×1000 dataset
2. Run TOPSIS analysis on all 1000 activities
3. Execute Hungarian algorithm for optimal assignment
4. Save results to `data/output/`
5. Display total execution time

---

## Performance Expectations

Based on typical hardware (modern CPU, 8GB+ RAM):

| Dataset Size | Activities | Profiles | Skills | TOPSIS Time | Assignment Time | Total Time |
|--------------|------------|----------|--------|-------------|-----------------|------------|
| **Small** | 100 | 100 | 20 | ~2-5s | ~0.1s | ~3-6s |
| **Medium** | 500 | 500 | 30 | ~30-60s | ~2-5s | ~35-70s |
| **Large** | 1000 | 1000 | 50 | ~120-250s | ~10-30s | ~150-300s |
| **Very Large** | 2000 | 2000 | 50 | ~600-1200s | ~60-180s | ~700-1400s |

**Note:** Times vary based on:
- CPU speed and number of cores
- Available RAM
- Proximity formula (variant vs standard)
- Whether assignment is enabled

---

## Performance Metrics Explained

### 1. **TOPSIS Time**
Time to compute proximity coefficients for all activities.
- Formula: Total time / Number of activities = Time per activity

### 2. **Assignment Time**
Time for Hungarian algorithm to find optimal 1-to-1 assignment.
- Only applicable when #profiles = #activities
- Complexity: O(n³)

### 3. **Throughput**
Number of activities processed per second.
- Formula: Activities / TOPSIS Time

### 4. **Peak Memory**
Maximum RAM usage during execution.
- Important for large datasets (1000+ profiles/activities)

---

## Tips for Large Datasets

### Memory Considerations

For very large datasets (>2000×2000):
- Ensure sufficient RAM (minimum 8GB, recommended 16GB+)
- Close other applications
- Consider using the greedy assignment method instead of Hungarian

### Speed Optimization

1. **Disable visualizations** (they're memory-intensive):
   ```bash
   # Visualizations are disabled by default if libraries not installed
   ```

2. **Use standard proximity formula** (slightly faster):
   ```bash
   python main.py --proximity-formula standard ...
   ```

3. **Skip assignment for unequal dimensions**:
   ```bash
   # Assignment is automatically skipped if dimensions don't match
   ```

---

## Interpreting Results

### Good Performance Indicators:
- ✅ Time per activity < 500ms
- ✅ Throughput > 5 activities/second
- ✅ Peak memory < 2GB for 1000×1000

### Potential Issues:
- ⚠️ Time per activity > 1000ms → CPU bottleneck
- ⚠️ Peak memory > 4GB for 1000×1000 → Memory inefficiency
- ⚠️ Assignment time > 60s for 1000×1000 → Consider greedy method

---

## Example: Complete Workflow

```bash
# 1. Generate multiple test datasets
python generate_large_dataset.py -p 100 -a 100 -s 20 --prefix test_100
python generate_large_dataset.py -p 500 -a 500 -s 30 --prefix test_500
python generate_large_dataset.py -p 1000 -a 1000 -s 50 --prefix test_1000

# 2. Run benchmarks
python run_benchmark_simple.py --profiles data/input/test_100_profiles.csv --activities data/input/test_100_activities.csv
python run_benchmark_simple.py --profiles data/input/test_500_profiles.csv --activities data/input/test_500_activities.csv
python run_benchmark_simple.py --profiles data/input/test_1000_profiles.csv --activities data/input/test_1000_activities.csv

# 3. Or run comprehensive suite
python benchmark_performance.py
```

---

## Comparison: Formula Performance

Test both proximity formulas to see which is faster for your use case:

```bash
# Standard formula
python main.py --profiles data/input/large_1000_profiles.csv \
               --activities data/input/large_1000_activities.csv \
               --proximity-formula standard

# Variant formula
python main.py --profiles data/input/large_1000_profiles.csv \
               --activities data/input/large_1000_activities.csv \
               --proximity-formula variant
```

**Generally:**
- **Standard**: Slightly faster, more conservative results
- **Variant**: Better discrimination, slightly slower

---

## Troubleshooting

### Out of Memory Error

**Solution:** Reduce dataset size or increase RAM.

```bash
# Try with fewer skills
python generate_large_dataset.py -p 1000 -a 1000 -s 30  # instead of 50
```

### Too Slow

**Solutions:**
1. Use standard formula instead of variant
2. Skip assignment for large datasets
3. Use greedy assignment instead of Hungarian

```bash
python main.py --profiles large.csv --activities large.csv \
               --proximity-formula standard --assignment-method greedy
```

### Process Hangs

- Check system resources (Task Manager / Activity Monitor)
- Kill and retry with smaller dataset
- Ensure no other memory-intensive programs are running

---

## Advanced: Custom Test Sizes

Modify `benchmark_performance.py` to test custom sizes:

```python
test_sizes = [
    (100, 100, 20),      # Your custom size
    (250, 250, 25),      # Another test
    (500, 1000, 30),     # Unequal dimensions (no Hungarian)
]
```

---

## Files Generated

After running benchmarks, you'll find:

```
data/
├── input/
│   ├── large_1000_profiles.csv
│   ├── large_1000_activities.csv
│   └── ... (other generated datasets)
├── output/
│   ├── rankings/
│   │   ├── full_results_matrix.csv
│   │   ├── ranking_matrix.csv
│   │   └── optimal_assignment_hungarian.csv
│   └── figures/ (if visualization libraries installed)
└── benchmark/
    ├── benchmark_results.csv
    ├── benchmark_report.txt
    └── ... (generated test files)
```

---

## Summary

The TOPSIS Profile Selection System can handle:
- ✅ **Small datasets** (100×100): Very fast (~3-6 seconds)
- ✅ **Medium datasets** (500×500): Fast (~30-70 seconds)
- ✅ **Large datasets** (1000×1000): Reasonable (~2-5 minutes)
- ⚠️ **Very large datasets** (2000×2000+): Possible but slow (~10-20 minutes)

For production use with very large datasets, consider:
1. Incremental processing
2. Database integration
3. Parallel processing
4. Caching mechanisms

---

**Questions or issues?** Check the main README.md or contact the author.
