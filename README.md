# High-Performance Computing — Data Pipeline for Healthcare

## Objective
Compare different data technologies (Pandas, Dask) on a public health dataset (BRFSS 2024) through a benchmark of common operations, then use the results in an interactive dashboard.

## Dataset
BRFSS 2024: U.S. public health survey, approximately 457,670 respondents and 301 variables.

## Project Structure
```text
.
├── data/
│   └── parquet/           Converted dataset, at different sizes
├── results/
│   ├── profil_colonnes.csv    Column profile (types, missing values, cardinality)
│   ├── timings.csv             Raw benchmark results
│   └── INTERPRETATION.md       Summary document (methodology, results, analysis)
└── src/
    ├── prepare_data.py         Conversion of the XPT file to Parquet
    ├── generate_sizes.py       Generation of the different data sizes
    ├── check_columns.py        Script to inspect and check column profiles
    ├── inspect_data.py         Quick data inspection and exploration script
    ├── operations.py           Benchmark operations (Pandas)
    ├── operations_dask.py      Benchmark operations (Dask)
    ├── benchmark.py            Measurement harness; generates results/timings.csv
    ├── app.py                  Interactive dashboard (Streamlit)
    ├── test_operations.py      Unit tests for Pandas operations
    └── test_operations_dask.py Unit tests for Dask operations
```

## Usage
All commands should be run from the project root.

### 1. Prepare the data
Only necessary if `data/parquet/brfss_full.parquet` does not already exist (otherwise, proceed directly to step 2 using the files already provided).
```
python src/prepare_data.py
```
Converts `data/raw/LLCP2024.XPT` to `data/parquet/brfss_full.parquet`. LLCP2024.XPT is too large to compress and has therefore been removed from the folder.

### 2. Generate the different data sizes
```
python src/generate_sizes.py
```
Produces the following files in `data/parquet/`: `brfss_10.parquet`, `brfss_25.parquet`, `brfss_50.parquet`, `brfss_100.parquet`, `brfss_x2.parquet`, `brfss_x3.parquet` (10%, 25%, 50%, and 100% of the dataset, followed by ×2 and ×3 duplications).

### 3. Run the benchmark
```
python src/benchmark.py
```
Runs the 5 operations (selection, filtering, groupby, new variable, descriptive statistics) with Pandas and Dask on each data size, and records the measured times in `results/timings.csv`.

### 4. Run the dashboard
```
streamlit run src/app.py
```
Opens a web interface allowing users to choose a data size, an operation, and one or more technologies, then display the result and the measured execution time.

### 5. Review the analysis
The `notebook/explorations.ipynb` notebook contains the initial exploration of the dataset. The `results/INTERPRETATION.md` document presents the methodology, benchmark results, and recommendations.

## Reda LAHLOU KASSI
