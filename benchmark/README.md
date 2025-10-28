# Benchmark Directory

This directory contains performance benchmarking tools for the TOPSIS Profile Selection System.

## Benchmark Scripts

### 1. **benchmark_performance.py**
Comprehensive performance benchmark suite with detailed metrics and memory tracking.

**Features:**
- Tests multiple dataset sizes (100×100, 500×500, 1000×1000)
- Tracks memory usage (RAM)
- Measures timing for each phase (data generation, TOPSIS, assignment)
- Generates comparison reports
- Exports results to CSV

**Usage:**
```bash
# From project root
python benchmark/benchmark_performance.py

# Or from benchmark directory
cd benchmark
python benchmark_performance.py
```

**Output Files:**
- `data/benchmark/benchmark_results.csv` - Detailed metrics in CSV format
- `data/benchmark/benchmark_report.txt` - Human-readable report

**Metrics Tracked:**
- Data generation time
- Initialization time
- TOPSIS analysis time
- Assignment time (Hungarian/Greedy)
- Peak memory usage
- Throughput (activities/second)

---

### 2. **run_benchmark_simple.py**
Simple timing wrapper for `main.py` execution.

**Usage:**
```bash
# From project root
python benchmark/run_benchmark_simple.py \
    --profiles data/input/large_1000_profiles.csv \
    --activities data/input/large_1000_activities.csv

# Without assignment
python benchmark/run_benchmark_simple.py \
    --profiles data/input/large_1000_profiles.csv \
    --activities data/input/large_1000_activities.csv \
    --no-assignment

# Or from benchmark directory
cd benchmark
python run_benchmark_simple.py \
    --profiles ../data/input/large_1000_profiles.csv \
    --activities ../data/input/large_1000_activities.csv
```

**Output:**
```
================================================================================
BENCHMARK RESULTS
================================================================================
Total execution time: 245.67 seconds (4.09 minutes)
Exit code: 0
================================================================================
```

---

## Quick Start: Benchmark 1000×1000

### Step 1: Generate Large Dataset

```bash
# From project root
python generate_large_dataset.py \
    --profiles 1000 \
    --activities 1000 \
    --skills 50 \
    --prefix large_1000
```

### Step 2: Run Simple Benchmark

```bash
python benchmark/run_benchmark_simple.py \
    --profiles data/input/large_1000_profiles.csv \
    --activities data/input/large_1000_activities.csv
```

### Step 3: Or Run Comprehensive Suite

```bash
python benchmark/benchmark_performance.py
```

---

## Performance Expectations

Based on typical hardware (modern CPU, 8GB+ RAM):

| Dataset | TOPSIS Time | Assignment Time | Total Time | Memory |
|---------|-------------|-----------------|------------|--------|
| 100×100×20 | ~2-5s | ~0.1s | ~3-6s | ~100 MB |
| 500×500×30 | ~30-60s | ~2-5s | ~35-70s | ~300 MB |
| 1000×1000×50 | ~120-250s | ~10-30s | ~150-300s | ~800 MB |
| 2000×2000×50 | ~600-1200s | ~60-180s | ~700-1400s | ~2 GB |

**Note:** Times vary based on CPU speed, RAM, and system load.

---

## Benchmark Metrics Explained

### 1. **TOPSIS Time**
Time to compute proximity coefficients for all activities.
- **Formula:** Total time ÷ Number of activities = Time per activity
- **Good:** < 500ms per activity
- **Acceptable:** 500-1000ms per activity
- **Slow:** > 1000ms per activity

### 2. **Assignment Time**
Time for optimal assignment algorithm (Hungarian or Greedy).
- **Hungarian:** O(n³) - only for equal dimensions
- **Greedy:** O(n² log n) - works with any dimensions
- **Good:** < 30s for 1000×1000

### 3. **Throughput**
Number of activities processed per second.
- **Formula:** Activities ÷ TOPSIS Time
- **Good:** > 5 activities/second
- **Acceptable:** 2-5 activities/second
- **Slow:** < 2 activities/second

### 4. **Peak Memory**
Maximum RAM usage during execution.
- **Important for:** Large datasets (>1000×1000)
- **Recommended:** < 2GB for 1000×1000

---

## Configuration Options

### Modify Test Sizes

Edit `benchmark_performance.py` to customize test configurations:

```python
test_sizes = [
    (100, 100, 20),      # Small
    (500, 500, 30),      # Medium
    (1000, 1000, 50),    # Large
    (2000, 2000, 50),    # Very large (uncomment if needed)
]
```

### Change Proximity Formula

```python
benchmark.run_multiple_benchmarks(test_sizes, proximity_formula='standard')
# or
benchmark.run_multiple_benchmarks(test_sizes, proximity_formula='variant')
```

---

## Requirements

### System Requirements
- **Python:** 3.8+
- **RAM:** Minimum 4GB (8GB+ recommended for large datasets)
- **CPU:** Multi-core recommended

### Python Packages
```bash
pip install numpy pandas scipy psutil
```

**Optional:**
```bash
pip install matplotlib seaborn  # For visualizations
```

---

## Interpreting Results

### Good Performance Indicators
- ✅ Time per activity < 500ms
- ✅ Throughput > 5 activities/second
- ✅ Peak memory < 2GB for 1000×1000
- ✅ Linear scaling with dataset size

### Potential Issues
- ⚠️ Time per activity > 1000ms → CPU bottleneck
- ⚠️ Peak memory > 4GB for 1000×1000 → Memory inefficiency
- ⚠️ Assignment time > 60s for 1000×1000 → Consider greedy method
- ⚠️ Non-linear scaling → Algorithm complexity issue

---

## Optimization Tips

### For Speed
1. Use standard proximity formula (slightly faster)
2. Disable visualizations
3. Use greedy assignment for large datasets
4. Close other applications

### For Memory
1. Reduce number of skills
2. Process activities in batches
3. Use greedy instead of Hungarian for unequal dimensions
4. Increase available RAM

---

## Troubleshooting

### Out of Memory Error
**Solution:** Reduce dataset size or increase RAM
```bash
# Generate with fewer skills
python generate_large_dataset.py -p 1000 -a 1000 -s 30
```

### Too Slow
**Solutions:**
```bash
# Use standard formula
python main.py --proximity-formula standard ...

# Skip assignment
python main.py --no-assignment ...

# Use greedy assignment
python main.py --assignment-method greedy ...
```

### Process Hangs
- Check Task Manager / Activity Monitor for resources
- Kill process and try with smaller dataset
- Ensure no other memory-intensive programs are running

---

## Advanced Usage

### Custom Benchmark

Create your own benchmark script based on `benchmark_performance.py`:

```python
from benchmark.benchmark_performance import PerformanceBenchmark

benchmark = PerformanceBenchmark()

# Custom test
result = benchmark.benchmark_topsis(
    n_profiles=1500,
    n_activities=1500,
    n_skills=40,
    proximity_formula='variant',
    use_assignment=True
)

print(f"Total time: {result['total_time']:.2f}s")
```

---

## Continuous Integration

For CI/CD pipelines, use the simple benchmark:

```yaml
# .github/workflows/benchmark.yml
- name: Run performance benchmark
  run: |
    python generate_large_dataset.py -p 100 -a 100 -s 10
    python benchmark/run_benchmark_simple.py \
      --profiles data/input/large_profiles.csv \
      --activities data/input/large_activities.csv
```

---

## Output Files

After running benchmarks:

```
data/
└── benchmark/
    ├── benchmark_results.csv      # Detailed metrics
    ├── benchmark_report.txt       # Human-readable report
    ├── bench_100x100_profiles.csv
    ├── bench_100x100_activities.csv
    ├── bench_500x500_profiles.csv
    ├── bench_500x500_activities.csv
    └── ...
```

---

## See Also

- [PERFORMANCE_TESTING_GUIDE.md](../PERFORMANCE_TESTING_GUIDE.md) - Comprehensive performance testing guide
- [generate_large_dataset.py](../generate_large_dataset.py) - Data generator script
- [config.json](../config.json) - System configuration

---

Author: Abdel YEZZA (Ph.D)
