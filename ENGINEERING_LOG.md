# 📔 Engineering Log: ETL R Generator

**Project:** `etl-r-generator`
**Mission:** Transpile Optimized Logical IR (YAML) into idiomatic, vectorized R code (Tidyverse).
**Target Dialect:** R 4.x + `dplyr`, `lubridate`, `readr`.

---

## 🏗 Architecture: The Transpiler

We will use a **Visitor Pattern**. The generator will walk the list of Logical Operations and delegate to specific "Handlers" for each node type.



### 1. The Structure Strategy
We will generate a single `pipeline.R` script structured as a functional chain:
```r
library(tidyverse)
library(lubridate)

# 1. Ingestion
ds_001 <- read_csv("input.csv")

# 2. Transformation Chain
ds_final <- ds_001 %>%
  mutate(...) %>%
  filter(...) %>%
  inner_join(...)

# 3. Output
write_csv(ds_final, "output.csv")

```

### 2. The Expression Challenge

The core complexity is translating SPSS/Generic formulas into R.

* **Math:** `TRUNC(x)`  `floor(x)` or `trunc(x)`
* **Logic:** `x = 1 AND y = 2`  `x == 1 & y == 2`
* **Dates:** `DATE.MDY(m,d,y)`  `make_date(year=y, month=m, day=d)`
* **Types:** `NUMBER(str)`  `as.numeric(str)`

---

## ✅ TDD Checklist & Roadmap

### Phase 1: The Skeleton & I/O

* [ ] **Test 1.1:** Generate standard R header (library imports).
* [ ] **Test 1.2:** Generate `read_csv` block for `OpType.LOAD_CSV`.
* [ ] **Test 1.3:** Generate `write_csv` block for `OpType.SAVE_BINARY`.

### Phase 2: The Verbs (Structural Ops)

* [ ] **Test 2.1:** Generate `dplyr::filter()` from `OpType.FILTER`.
* [ ] **Test 2.2:** Generate `dplyr::arrange()` from `OpType.SORT`.
* [ ] **Test 2.3:** Generate `dplyr::inner_join()` from `OpType.JOIN`.
* [ ] **Test 2.4:** Generate `dplyr::summarise()` from `OpType.AGGREGATE`.

### Phase 3: The Brain (Batch Compute & Expressions)

* [ ] **Test 3.1:** Generate `dplyr::mutate()` from `OpType.BATCH_COMPUTE`.
* [ ] **Test 3.2:** **Transpiler:** Convert basic math (+, -, *, /).
* [ ] **Test 3.3:** **Transpiler:** Convert logic (AND, OR, =, <>).
* [ ] **Test 3.4:** **Transpiler:** Convert specific SPSS functions (`DATE.MDY` -> `make_date`).

### Phase 4: Integration

* [ ] **Test 4.1:** End-to-End generation of the "Monster" pipeline.
* [ ] **Test 4.2:** Syntax Check - Verify the generated string is valid R code (using `subprocess` to run `Rscript -e` if available, or static analysis).

---
# 📔 Engineering Log: ETL R Generator

**Project:** `etl-r-generator`
**Mission:** Transpile Optimized Logical IR into Idiomatic R (Tidyverse).
**Constraint:** STRICT adherence to Professor's Architecture (Formal IR, No String Scraping).

---

## 🏗 Architecture

We adhere to the "Visitor Pattern" to strictly separate **Traversal** (Walking the Graph) from **Rendering** (Printing R).

### 1. The Transpiler (Expression Engine)
We will NOT use regex replacement on full lines. We will parse specific function calls.
* `SYSMIS(x)` -> `is.na(x)`
* `DATE.MDY(m,d,y)` -> `make_date(y,m,d)`
* `RND(x)` -> `round(x)`

### 2. The Type Enforcer
R is strict about types.
* **Booleans:** Ensure `1/0` flags become `TRUE/FALSE` if used in logic.
* **Factors:** Detect categorical logic and generate `as.factor()`.

---

## ✅ TDD Checklist (Revised)

### Phase 1: Structure (Done)
* [x] **Test 1.1:** Header Generation.
* [x] **Test 1.2:** I/O (Load/Save).

### Phase 2: Verbs (Structural)
* [ ] **Test 2.1:** Filter (Strict condition wrapping).
* [ ] **Test 2.2:** Sort (Arrange).
* [ ] **Test 2.3:** Join (Explicit `by` clause handling).

### Phase 3: The Transpiler (The Professor's Concern)
* [ ] **Test 3.1:** Math Translation (`TRUNC`, `RND`).
* [ ] **Test 3.2:** Logic Translation (`AND`, `OR`, `SYSMIS`).
* [ ] **Test 3.3:** Date Translation (`DATE.MDY`).
* [ ] **Test 3.4:** Missing Value Handling (`na_if`).

### Phase 4: Batch Compute (The Logic)
* [ ] **Test 4.1:** Generate `mutate()` with multiple columns.
* [ ] **Test 4.2:** Integration of Transpiler into Mutate.

---