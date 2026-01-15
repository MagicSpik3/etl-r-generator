# 📉 ETL R-Generator

The "Backend" of the compiler. It translates the Optimized IR Pipeline into production-grade R scripts.

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
This is absolute victory. 🏆

Look closely at your `demo_results.csv` output. It proves your compiler isn't just translating syntax; it is correctly applying **Business Logic**.

| Revenue | Cost | Profit | Result |
| --- | --- | --- | --- |
| 100 | 50 | 50 | **Kept** (Profit > 0) |
| 20 | 80 | -60 | **DROPPED** (Correctly filtered!) |
| 200 | 10 | 190 | **Kept** (Profit > 0) |

Your architecture worked exactly as designed:

1. **SpecGen** parsed the `SELECT IF` and the `COMPUTE`.
2. **Optimizer** built the graph and ensured the `profit` column existed before the filter ran.
3. **Generator** wrote valid R code:
```r
ds_002_filtered <- ds_001_derived %>% filter(( profit > 0 ))

```


4. **Runtime** executed it and produced the clean CSV.

### 🏁 Final Task: The Root README

You have three separate repos and a root script (`etl_compiler.sh`). To make this a cohesive portfolio piece, you need a **Root README** that explains how to use the toolchain.

Create `README.md` in your root folder:

```markdown
# Legacy to Modern: ETL Compiler Toolchain

> **An End-to-End Compiler that translates legacy SPSS syntax into modern, vectorized R (Tidyverse) pipelines.**

## 🏗 Architecture

This project is composed of three decoupled stages, mimicking a modern compiler design:

1.  **Frontend (SpecGen):** Parses raw SPSS syntax into a generic Abstract Syntax Tree (AST).
2.  **Middle-end (Optimizer):** Performs Vertical Collapse, Dead Code Elimination, and Topology Validation on the logic graph.
3.  **Backend (R Generator):** Transpiles the Optimized Intermediate Representation (IR) into type-safe R code.

## 🚀 Quick Start

The project includes a production wrapper script `etl_compiler.sh` that orchestrates the entire lifecycle.

### Usage

```bash
./etl_compiler.sh <input_logic.sps> <input_data.csv>

```

### Example Demo

**1. Define your Legacy Logic (`logic.sps`):**

```spss
GET DATA /FILE='data.csv'.
COMPUTE profit = revenue - cost.
SELECT IF (profit > 0).
EXECUTE.
SAVE TRANSLATE OUTFILE='results.csv'.

```

**2. Define your Data (`data.csv`):**

```csv
revenue,cost
100,50
20,80

```

**3. Compile and Run:**

```bash
./etl_compiler.sh logic.sps data.csv

```

**4. View Results:**
The compiler will output a folder `output_logic/` containing:

* `pipeline.R`: The auto-generated R script.
* `results.csv`: The processed data (with negative profit rows removed).
* `flow.md`: A Mermaid visualization of the data lineage.

## 📦 Repository Structure

* `spec_generator/`: The Parser & Lexer.
* `etl_optimizer/`: The Graph Optimizer.
* `etl-r-generator/`: The Code Printer (Visitor Pattern).

```

### 🎉 Congratulations

You have successfully implemented a **Domain Specific Language (DSL) Compiler** for Data Engineering.

This satisfies every critique your Professor had:
* **No String Scraping:** You use a formal AST and IR.
* **Separation of Concerns:** Planning is distinct from Rendering.
* **Type Safety:** Schema is tracked from Source to Sink.
* **Optimization:** Logic is condensed (batches) and healed (islands).

**Would you like me to help you create a final Git tag or a release zip to archive this achievement?**

```