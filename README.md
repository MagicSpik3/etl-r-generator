# ETL R Generator

![Status](https://img.shields.io/badge/status-phase--1-blue) ![Target](https://img.shields.io/badge/target-R_%2F_Tidyverse-blue)

> **The Backend Compiler: Turning Logic into Code.**

This is the final stage of the ETL Compiler pipeline. It consumes the **Optimized Logical IR** (produced by `etl-optimizer`) and synthesizes idiomatic, human-readable R scripts.

## 🎯 Design Philosophy

We do not generate "Machine Code." We generate **Maintenance Code**.
The output is designed to look as if a Senior R Data Engineer wrote it by hand.

### Key Features
1.  **Vectorization:** Converts loops and linear computes into vectorized `dplyr::mutate` chains.
2.  **Idiomatic Tidyverse:** Uses pipes (`%>%`) and standard verbs (`filter`, `select`, `group_by`).
3.  **Type Safety:** explicit type casting where the IR dictates (e.g., String to Numeric).
4.  **No Vendor Lock-in:** The generated code runs on open-source R; it requires no proprietary runtime from this project.

## 🏗 Architecture

```mermaid
graph LR
    A[Optimized IR (YAML)] -->|Ingest| B(Pipeline Model)
    B -->|Visitor| C{Node Type?}
    C -->|Batch Compute| D[Mutate Generator]
    C -->|Filter| E[Filter Generator]
    C -->|Join| F[Join Generator]
    D -->|Expression Transpiler| G[R Syntax Builder]
    E -->|Expression Transpiler| G
    G -->|Emit| H[final_script.R]

```

## 🛠 Usage

```bash
# Generate R script from optimized YAML
python cli.py input_optimized.yaml --output pipeline.R

```

### Example Output

**Input IR:**

```yaml
type: batch_compute
parameters:
  computes:
    - target: age
      expression: (current_date - dob) / 365

```

**Output R:**

```r
df <- df %>%
  mutate(
    age = (current_date - dob) / 365
  )

```

## 📦 Requirements

* Python 3.12+
* R 4.x (Only required to run the generated code, not to generate it)

```
