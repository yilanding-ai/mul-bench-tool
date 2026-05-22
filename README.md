# Mul-Bench

Benchmark 14 DNA methylation alignment algorithms for whole genome bisulfite/converted sequencing.

Based on the paper: *"Benchmarking DNA methylation analysis of 14 alignment algorithms for whole genome bisulfite sequencing in mammals"* (Gong et al., 2022, CSBJ).

## Features

- **14 alignment tools**: Bwa-meth, BSBolt, BSMAP, Walt, Abismal, Batmeth2, HISAT-3n, HISAT-3n (repeat), Bismark-bwt2-e2e, Bismark-his2, BSseeker2-bwt, BSseeker2-soap2, BSseeker2-bwt2-e2e, BSseeker2-bwt2-local
- **12 conversion types**: C>T, T>C, A>G, G>A, A>C, C>A, G>T, T>G, A>T, T>A, C>G, G>C
- **Single-end & Paired-end**: Both modes supported
- **Simulated data**: Built-in simulator with known ground truth (no input files needed)
- **Real data support**: Extract subsets from real FASTQ files
- **Built-in mock aligners**: 4 accuracy levels, run the full pipeline without installing any external tools
- **Comprehensive evaluation**: Precision, recall, F1 score, accuracy, methylation level correlation
- **Multi-sample batch analysis**: Compare aligner performance across multiple samples and conditions
- **QC analysis**: Per-base quality, GC content, sequence length distribution, overrepresented sequences, adapter detection
- **Adapter trimming**: Built-in trimmer with auto-detection, bisulfite-aware, cutadapt integration
- **UMI processing**: Header/inline extraction, cluster/consensus deduplication, auto-detect
- **Rich reports**: HTML, JSON, CSV, plots (matplotlib/seaborn)
- **Web UI**: Interactive Streamlit interface with Plotly charts
- **Docker**: Multi-stage containerization, docker-compose support

## Installation

### Option 1: pip (from source)

```bash
# Unzip the package
unzip mul-bench-1.0.0.zip
cd mul-bench-1.0.0

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install .

# Verify installation
mul-bench --help
```

### Option 2: Docker

```bash
# Build and run with docker-compose
docker-compose up --build

# Or build manually
docker build -t mul-bench .
docker run --rm -v $(pwd)/results:/app/results mul-bench run --simulate -o /app/results
```

## Quick Start

### Demo (no external tools required)

```bash
# Run a quick demo with built-in mock aligners
mul-bench run --simulate -o ./results

# Demo with A-to-G conversion
mul-bench run --simulate --conversion ag -o ./results

# Demo with G-to-T conversion
mul-bench run --simulate --conversion gt -o ./results
```

This generates simulated data, runs 4 mock aligners (perfect/good/medium/poor), evaluates accuracy, and produces a ranked HTML report.

### Multi-sample batch demo

```bash
mul-bench batch-demo
```

Runs 4 samples (high/low methylation x 2 conversion types) and generates a comparison report.

### Web UI

```bash
mul-bench web
```

Opens a Streamlit web interface with interactive Plotly charts.

## Usage

### All commands

```text
mul-bench [OPTIONS] COMMAND [ARGS]...

Commands:
  run              Run the full benchmarking pipeline
  simulate         Generate simulated bisulfite/converted sequencing data
  extract          Extract a subset of reads from FASTQ files
  trim             Trim adapters from FASTQ files
  umi              Detect and process UMIs
  qc               Run quality control analysis on FASTQ file(s)
  report           Generate report from completed benchmark results
  batch            Multi-sample batch analysis commands
  batch-demo       Run a multi-sample demo (no external tools required)
  list-aligners    List all supported aligners with descriptions
  list-adapters    List known adapter sequences
  list-umi-patterns List known UMI patterns
  web              Launch the interactive web interface (Streamlit)
```

### `run` — Full benchmarking pipeline

```bash
mul-bench run [OPTIONS]

Options:
  -1, --read1 FILE          Read 1 FASTQ file
  -2, --read2 FILE          Read 2 FASTQ file (paired-end)
  -r, --reference FILE      Reference genome FASTA
  -o, --output DIR          Output directory (default: ./mul_bench_results)
  -c, --config FILE         Config file path
  --conversion CHOICE       Conversion type (default: ct)
                            One of: ct, tc, ag, ga, ac, ca, gt, tg, at, ta, cg, gc
  --simulate                Generate simulated data instead of using real input
  --sim-reads INT           Number of simulated reads (default: 50000)
  --num-reads INT           Number of reads to extract from real data (default: 100000)
  --threads INT             Threads to use (default: 8)
  --aligners STR            Comma-separated list of aligners to run
  --dry-run                 Check tool availability without running
  --enable-qc               Enable QC analysis phase
  --enable-trim             Enable adapter trimming
  --enable-umi              Enable UMI processing
  --help                    Show this message
```

#### Examples

```bash
# Simulated data, C-to-T (default), single-end
mul-bench run --simulate --conversion ct --sim-reads 100000 -o ./results

# Real data, paired-end, A-to-G conversion
mul-bench run -1 sample_R1.fastq.gz -2 sample_R2.fastq.gz \
  -r reference.fa --conversion ag -o ./results --threads 16

# Run a subset of aligners only
mul-bench run --simulate --aligners bwameth,bsbolt,bsmap -o ./results

# Enable QC + adapter trimming + UMI
mul-bench run -1 sample_R1.fastq.gz -r reference.fa \
  --enable-qc --enable-trim --enable-umi -o ./results

# All 12 conversion types
mul-bench run --simulate --conversion tc -o ./results_tc
mul-bench run --simulate --conversion ac -o ./results_ac
mul-bench run --simulate --conversion cg -o ./results_cg
```

### `simulate` — Generate simulated data only

```bash
mul-bench simulate --genome-length 1000000 --num-reads 50000 \
  --read-length 100 --conversion ct --mode pe -o ./sim_data

Options:
  --genome-length INT    Reference genome length (default: 1000000)
  --num-reads INT        Number of reads (default: 50000)
  --read-length INT      Read length (default: 100)
  --fragment-mean INT    Mean fragment size for paired-end (default: 300)
  --fragment-sd INT      Fragment size SD (default: 50)
  --methylation-rate FLOAT  Methylation rate (default: 0.7)
  --error-rate FLOAT     Sequencing error rate (default: 0.01)
  --conversion CHOICE    Conversion type (default: ct)
  --mode [se|pe]         Sequencing mode (default: pe)
  --seed INT             Random seed (default: 42)
  -o, --output DIR       Output directory (default: ./simulated_data)
```

### `extract` — Subset reads from FASTQ files

```bash
mul-bench extract -1 input_R1.fastq.gz -2 input_R2.fastq.gz \
  --num-reads 100000 -o ./subset

Options:
  -1, --read1 FILE   Read 1 FASTQ (required)
  -2, --read2 FILE   Read 2 FASTQ (paired-end)
  --num-reads INT    Number of reads to extract (default: 100000)
  --seed INT         Random seed for sampling (default: 42)
  -o, --output DIR   Output directory
```

### `trim` — Adapter trimming

```bash
mul-bench trim -1 input_R1.fastq.gz -2 input_R2.fastq.gz \
  --conversion ct -o ./trimmed

Options:
  -1, --read1 FILE      Read 1 FASTQ (required)
  -2, --read2 FILE      Read 2 FASTQ (paired-end)
  --conversion CHOICE   Conversion type for bisulfite-aware trimming (default: ct)
  --auto-detect         Auto-detect adapter sequences
  --r1-3prime STR       R1 3' adapter sequence
  --r2-3prime STR       R2 3' adapter sequence
  --use-cutadapt        Use cutadapt if available (default: true)
  -o, --output DIR      Output directory
```

### `umi` — UMI processing

```bash
mul-bench umi -1 input_R1.fastq.gz --location header --strategy cluster -o ./umi

Options:
  -1, --read1 FILE       Read 1 FASTQ (required)
  -2, --read2 FILE       Read 2 FASTQ (paired-end)
  --location [header|inline_5prime|inline_3prime]  UMI location (default: header)
  --length INT           UMI length (0 = auto-detect)
  --pattern STR          Custom regex pattern
  --strategy [cluster|consensus]  Deduplication strategy (default: cluster)
  -o, --output DIR       Output directory
```

### `qc` — Quality control

```bash
mul-bench qc -1 input_R1.fastq.gz -2 input_R2.fastq.gz \
  --max-reads 50000 -o ./qc_report

Options:
  -1, --read1 FILE   Read 1 FASTQ (required)
  -2, --read2 FILE   Read 2 FASTQ (paired-end)
  --max-reads INT    Maximum reads to analyze (default: 50000)
  -o, --output DIR   Output directory (default: ./qc_report)
```

### `batch` — Multi-sample batch analysis

```bash
# Run batch analysis from config file
mul-bench batch run -c batch_config.yaml -o ./batch_results

# Generate a sample batch config
mul-bench batch generate -o batch_config.yaml
```

Example `batch_config.yaml`:

```yaml
max_workers: 4
use_mock: true
samples:
  - name: sample1
    conversion: ct
    mode: pe
    group: group_a
    sim_reads: 30000
  - name: sample2
    conversion: ag
    mode: pe
    group: group_a
    sim_reads: 30000
  - name: sample3
    conversion: ct
    mode: se
    group: group_b
    sim_reads: 30000
```

### `batch-demo` — Quick multi-sample demo

```bash
mul-bench batch-demo
```

Runs 4 simulated samples (ct/ag x high/low methylation) with mock aligners and generates a comparison HTML report.

### `web` — Streamlit web interface

```bash
mul-bench web
```

Launches a browser-based UI with 5 pages:

- **Pipeline**: Run the benchmarking pipeline
- **Quality Control**: View QC metrics
- **Results**: Browse benchmark results
- **Multi-Sample**: Compare multiple samples
- **About**: Package information

## Output Structure

```
results/
├── comparison_results.json       # Full results in JSON
├── comparison_results.csv        # Results in CSV
├── report/
│   ├── report.html               # Interactive HTML report
│   ├── summary.txt               # Text summary
│   ├── f1_score.png              # F1 score bar chart
│   ├── precision.png             # Precision bar chart
│   ├── recall.png                # Recall bar chart
│   ├── accuracy.png              # Accuracy bar chart
│   └── heatmap.png               # Performance heatmap
├── qc/                           # QC reports (if enabled)
│   ├── qc_report.html
│   └── qc_metrics.json
└── work/
    ├── simulated/                # Simulated data (if --simulate)
    │   ├── reference.fa
    │   ├── ground_truth.bed
    │   └── simulated_R*.fastq
    └── bwameth/                  # Per-aligner results
        └── ...
```

## Conversion Types

All 12 possible single-base substitutions are supported:

| Tag | Conversion | Description |
|-----|-----------|-------------|
| ct | C -> T | Bisulfite conversion (WGBS) |
| tc | T -> C | Reverse bisulfite |
| ag | A -> G | A-to-G conversion |
| ga | G -> A | G-to-A conversion |
| ac | A -> C | A-to-C conversion |
| ca | C -> A | C-to-A conversion |
| gt | G -> T | G-to-T conversion |
| tg | T -> G | T-to-G conversion |
| at | A -> T | A-to-T conversion |
| ta | T -> A | T-to-A conversion |
| cg | C -> G | C-to-G conversion |
| gc | G -> C | G-to-C conversion |

## Supported Aligners

| Aligner | Description |
|---------|-------------|
| bwameth | Bwa-meth: BWA-based aligner for bisulfite reads |
| bsbolt | BSBolt: Bisulfite sequence aligner |
| bsmap | BSMAP: Bisulfite mapping program |
| walt | Walt: Fast bisulfite read aligner |
| abismal | Abismal: Bisulfite read aligner |
| batmeth2 | Batmeth2: Bisulfite aligner |
| hisat3n | HISAT-3n: Hierarchical indexing for spliced alignment |
| hisat3n_repeat | HISAT-3n (repeat): Repeat-aware alignment |
| bismark_bwt2_e2e | Bismark-bwt2-e2e: End-to-end bowtie2 mode |
| bismark_his2 | Bismark-his2: HISAT2 mode |
| bsseeker2_bwt | BSseeker2-bwt: BWA-backtrack mode |
| bsseeker2_soap2 | BSseeker2-soap2: SOAP2 mode |
| bsseeker2_bwt2_e2e | BSseeker2-bwt2-e2e: End-to-end bowtie2 mode |
| bsseeker2_bwt2_local | BSseeker2-bwt2-local: Local bowtie2 mode |
| mock_* | Built-in mock aligners (no external tools needed) |

## Mock Aligners

When no external tools are installed, Mul-Bench automatically falls back to 4 built-in mock aligners with controlled accuracy levels:

- **mock_perfect**: Accuracy ~ 0.98 (simulates near-perfect alignment)
- **mock_good**: Accuracy ~ 0.88
- **mock_medium**: Accuracy ~ 0.75
- **mock_poor**: Accuracy ~ 0.55

This allows the full pipeline to run end-to-end without any external dependencies.

## Configuration

All pipeline settings can be configured via YAML config file:

```bash
mul-bench run -c config.yaml
```

See `config.yaml` for all available options.

## Docker

```bash
# Build and run
docker build -t mul-bench .

# Run simulation benchmark
docker run --rm -v $(pwd)/results:/app/results mul-bench run --simulate -o /app/results

# Run with real data
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/results:/app/results \
  mul-bench run -1 /app/data/sample_R1.fastq.gz -r /app/data/reference.fa -o /app/results

# Docker Compose (with web UI)
docker-compose up
# Then open http://localhost:8501

# Run QC service
docker-compose run qc -1 /data/sample_R1.fastq.gz -o /data/qc_report
```

## Install External Aligners

```bash
# Via conda (recommended)
conda install -c bioconda bwameth bsbolt bsmap walt abismal batmeth2 \
  hisat-3n bismark bs-seeker2 samtools bedtools

# Or use the install script
bash scripts/install_tools.sh
```

## License

MIT
