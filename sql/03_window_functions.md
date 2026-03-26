# SQL Window Functions: The Data Engineer's Guide

### 1. The Core Concept

**Definition:**
A **Window Function** performs a calculation across a set of rows related to the current row — without collapsing them into a single output row the way `GROUP BY` does. Every original row remains in the result; the window function simply adds a new column alongside it.

* **Analogy:** Imagine a spreadsheet where you scroll down row by row. For each row, you highlight a group of nearby rows (the "window"), compute something over them, and write the result in a new column next to the current row. The rows never merge — they just get annotated.
* **Key Keyword:** `OVER()`.

**Syntax:**

```sql
function_name() OVER (
    [PARTITION BY column]   -- defines the group boundaries (resets the window)
    [ORDER BY column]       -- defines the order of rows within each window
    [frame_clause]          -- defines which rows within the window to include
)
```

**The difference from `GROUP BY`:**

```sql
-- GROUP BY: collapses rows — you lose individual rows
SELECT department, AVG(salary)
FROM Employees
GROUP BY department;
-- Returns 1 row per department

-- Window Function: keeps all rows, just adds the group average alongside
SELECT name, department, salary,
       AVG(salary) OVER (PARTITION BY department) AS dept_avg
FROM Employees;
-- Returns ALL employee rows, each showing their department's average
```

---

### 2. Chapter 1 — Numbering Rows

These functions assign a number to each row within its partition. All three use the same syntax — only the tie-handling logic differs.

#### **A. `ROW_NUMBER`**

**Use Case:** Assign a unique, sequential integer to every row. Ties are broken arbitrarily — every row gets a distinct number regardless.

```sql
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num
FROM Employees;

-- Output:
-- Alice   | Engineering | 90000 | 1
-- Bob     | Engineering | 75000 | 2
-- Charlie | Engineering | 75000 | 3   <-- same salary as Bob, but gets 3
-- Carol   | Marketing   | 80000 | 1   <-- resets to 1 for new partition
-- Dave    | Marketing   | 65000 | 2
```

**Real-world pattern — Deduplication:**
`ROW_NUMBER()` is the standard tool for keeping only the most recent version of a row.

```sql
-- Keep only the latest record per customer
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS rn
    FROM Orders
) ranked
WHERE rn = 1;
```

#### **B. `RANK`**

**Use Case:** Assign a rank where tied rows share the same number, but the sequence **skips** to account for the tie (gaps appear).

```sql
SELECT
    name,
    score,
    RANK() OVER (ORDER BY score DESC) AS rnk
FROM Results;

-- Output:
-- Alice | 100 | 1
-- Bob   | 100 | 1   <-- tied with Alice, both get 1
-- Carol |  90 | 3   <-- skipped 2 because two people tied for 1st
-- Dave  |  85 | 4
```

* **Analogy:** Olympic medals. Two gold medalists exist, so no silver is awarded — the next person gets bronze (rank 3).

#### **C. `DENSE_RANK`**

**Use Case:** Same as `RANK` for ties, but the sequence **never skips** — no gaps.

```sql
SELECT
    name,
    score,
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rnk
FROM Results;

-- Output:
-- Alice | 100 | 1
-- Bob   | 100 | 1   <-- tied, both get 1
-- Carol |  90 | 2   <-- no gap, next rank is 2
-- Dave  |  85 | 3
```

* **When to use `DENSE_RANK` over `RANK`:** When the rank number itself is meaningful as a category label — e.g., "Top 3 salary bands" — and you don't want a gap to produce an empty band.

#### **D. Side-by-Side Comparison**

Running all three on the same data makes the differences clear:

```sql
SELECT
    name,
    score,
    ROW_NUMBER()  OVER (ORDER BY score DESC) AS row_num,
    RANK()        OVER (ORDER BY score DESC) AS rnk,
    DENSE_RANK()  OVER (ORDER BY score DESC) AS dense_rnk
FROM Results;

-- Output:
-- name  | score | row_num | rnk | dense_rnk
-- Alice |   100 |       1 |   1 |         1
-- Bob   |   100 |       2 |   1 |         1
-- Carol |    90 |       3 |   3 |         2
-- Dave  |    85 |       4 |   4 |         3
```

| Function | Ties get same number? | Gaps after ties? | Always unique? |
| :--- | :--- | :--- | :--- |
| `ROW_NUMBER` | ❌ | — | ✅ |
| `RANK` | ✅ | ✅ | ❌ |
| `DENSE_RANK` | ✅ | ❌ | ❌ |

#### **E. `PARTITION BY` vs `ORDER BY` Inside `OVER()`**

These two clauses control completely different things:

* **`PARTITION BY column`:** Divides the result set into independent groups. The window function restarts its calculation for each group — like a `GROUP BY` that doesn't collapse rows. Omitting it means the entire result set is treated as one window.
* **`ORDER BY column`:** Defines the sort order *within* each partition. Required for ranking and fetching functions; changes the frame behaviour for aggregate functions (see Chapter 3).

```sql
-- No PARTITION BY, no ORDER BY: one window = entire table
-- AVG is computed over all rows globally
AVG(salary) OVER ()

-- PARTITION BY only: window = each department, no ordering
-- AVG is computed per department, same value for all rows in a dept
AVG(salary) OVER (PARTITION BY department)

-- Both: window = each department, ordered by salary descending
-- Used for ranking within departments
ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)
```

**Critical Rule:** Providing only `ORDER BY` (no `PARTITION BY`) inside `OVER()` means the window spans the entire result set, ordered — this implicitly creates a cumulative/running calculation. The default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

---

### 3. Chapter 2 — Fetching

Fetching functions look up the value of a column in a different row — either relative to the current row (LAG/LEAD) or anchored to the absolute start/end of the partition (FIRST_VALUE/LAST_VALUE).

#### **A. Relative Fetching: `LAG` and `LEAD`**

**Use Case:** Compare a row's value to the row before or after it without a self-join — essential for period-over-period analysis.

**Syntax:**
```sql
LAG(column, offset, default)  OVER (...)
LEAD(column, offset, default) OVER (...)
-- offset:  how many rows to go back/forward (default = 1)
-- default: value to return when no such row exists (default = NULL)
```

* **`LAG(col, n, default)`** — looks `n` rows **behind** the current row.
* **`LEAD(col, n, default)`** — looks `n` rows **ahead** of the current row.

**Example — Day-over-day revenue change:**

```sql
SELECT
    order_date,
    revenue,
    LAG(revenue, 1, 0)  OVER (ORDER BY order_date) AS prev_day_revenue,
    revenue - LAG(revenue, 1, 0) OVER (ORDER BY order_date) AS day_change
FROM DailySales;

-- Output:
-- 2024-01-01 | 100 |   0 | 100   <-- no prior day, default = 0
-- 2024-01-02 | 150 | 100 |  50
-- 2024-01-03 | 120 | 150 | -30
-- 2024-01-04 | 200 | 120 |  80
```

**Example — Comparing to the next row (LEAD):**

```sql
SELECT
    product,
    release_date,
    price,
    LEAD(price, 1) OVER (PARTITION BY product ORDER BY release_date) AS next_price,
    LEAD(price, 1) OVER (PARTITION BY product ORDER BY release_date) - price AS price_change
FROM ProductPrices;

-- Shows how price will change in the *next* version of each product
-- Last row per product returns NULL for next_price (no following row)
```

#### **B. Absolute Fetching: `FIRST_VALUE` and `LAST_VALUE`**

**Use Case:** Fetch the first or last value of a column within the partition — useful for comparisons like "how does this row compare to the best in its group?"

* **`FIRST_VALUE(col)`** — returns the first value in the window. Behaves correctly with the default frame.
* **`LAST_VALUE(col)`** — returns the last value in the window. Requires a frame override (see Critical Rule).

**Example:**

```sql
SELECT
    name,
    department,
    salary,
    -- Highest earner in the department (first row when sorted DESC)
    FIRST_VALUE(name) OVER (
        PARTITION BY department ORDER BY salary DESC
    ) AS top_earner,
    -- Lowest earner in the department (needs full frame)
    LAST_VALUE(name) OVER (
        PARTITION BY department
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_earner,
    -- % of salary compared to the top earner
    ROUND(salary * 100.0 /
        FIRST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC),
    1) AS pct_of_top
FROM Employees;
```

**Critical Rule — The `LAST_VALUE` trap:**

By default, when you add `ORDER BY` inside `OVER()`, SQL uses an implicit frame of `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. This means the window only "sees" from the first row up to the *current* row — so `LAST_VALUE` returns the current row's own value, not the actual last in the partition.

```sql
-- BAD: returns current row's salary, not the minimum
LAST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC)

-- GOOD: extend the frame to include all rows in the partition
LAST_VALUE(salary) OVER (
    PARTITION BY department
    ORDER BY salary DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

`FIRST_VALUE` does not have this problem because `UNBOUNDED PRECEDING` always reaches the start of the partition regardless of the frame's end boundary.

#### **C. Paging: `NTILE`**

**Use Case:** Divide rows into `n` roughly equal buckets — most commonly used to assign percentile labels (quartiles, deciles, top 10%).

**Syntax:**
```sql
NTILE(n) OVER (ORDER BY column)
-- Returns an integer from 1 to n, indicating which bucket each row belongs to
```

**Example — Salary quartiles:**

```sql
SELECT
    name,
    salary,
    NTILE(4) OVER (ORDER BY salary DESC) AS quartile
    -- 1 = top 25% earners, 4 = bottom 25% earners
FROM Employees;

-- Output:
-- Alice   | 95000 | 1
-- Bob     | 88000 | 1
-- Charlie | 75000 | 2
-- Dave    | 70000 | 2
-- Eve     | 65000 | 3
-- Frank   | 60000 | 3
-- Grace   | 45000 | 4
-- Henry   | 40000 | 4
```

**Example — Top 10% flag:**

```sql
SELECT
    name,
    salary,
    CASE WHEN NTILE(10) OVER (ORDER BY salary DESC) = 1
         THEN 'Top 10%'
         ELSE 'Other'
    END AS tier
FROM Employees;
```

* **Note:** If rows don't divide evenly into `n` buckets, the earlier buckets get one extra row (e.g., 10 rows into 3 buckets → buckets of 4, 3, 3).

---

### 4. Chapter 3 — Aggregate Functions & Frames

#### **A. Aggregate Window Functions**

**Definition:**
Standard aggregate functions — `SUM`, `AVG`, `MIN`, `MAX`, `COUNT` — become window functions when paired with `OVER()`. They calculate their result over the defined window without collapsing rows.

**Use Case:** The most common application is a **running total** — the accumulated value from the start of the partition up to the current row.

```sql
SELECT
    order_date,
    revenue,
    SUM(revenue)   OVER (ORDER BY order_date) AS running_total,
    AVG(revenue)   OVER (ORDER BY order_date) AS running_avg,
    MIN(revenue)   OVER (ORDER BY order_date) AS running_min,
    MAX(revenue)   OVER (ORDER BY order_date) AS running_max,
    COUNT(revenue) OVER (ORDER BY order_date) AS running_count
FROM DailySales;

-- Output:
-- date       | revenue | running_total | running_avg | running_min | running_max | running_count
-- 2024-01-01 |     100 |           100 |       100.0 |         100 |         100 |             1
-- 2024-01-02 |     150 |           250 |       125.0 |         100 |         150 |             2
-- 2024-01-03 |      80 |           330 |       110.0 |          80 |         150 |             3
-- 2024-01-04 |     200 |           530 |       132.5 |          80 |         200 |             4
```

**Running total partitioned by group:**

```sql
SELECT
    order_date,
    region,
    revenue,
    SUM(revenue) OVER (PARTITION BY region ORDER BY order_date) AS regional_running_total
FROM DailySales;
-- Running total resets for each region
```

#### **B. Frames — Controlling the Window Size**

**Definition:**
A **frame** specifies exactly which rows within a partition are included in the calculation for the current row. Without a frame clause, SQL uses a default that depends on whether `ORDER BY` is present:

* No `ORDER BY` → default frame: all rows in the partition (`RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`)
* With `ORDER BY` → default frame: first row to current row (`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`)

This default is what produces the running total behaviour you saw above. **Frames let you override that default.**

**Syntax:**

```sql
function() OVER (
    PARTITION BY ...
    ORDER BY ...
    {ROWS | RANGE} BETWEEN <start> AND <end>
)
```

**Frame boundary keywords:**

| Keyword | Meaning |
| :--- | :--- |
| `UNBOUNDED PRECEDING` | First row of the partition |
| `n PRECEDING` | `n` rows before the current row |
| `CURRENT ROW` | The current row itself |
| `n FOLLOWING` | `n` rows after the current row |
| `UNBOUNDED FOLLOWING` | Last row of the partition |

**Example — 3-day moving average (slide the window):**

```sql
SELECT
    order_date,
    revenue,
    AVG(revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        -- Window = current row + 2 rows behind = up to 3 rows total
    ) AS moving_avg_3d
FROM DailySales;

-- Output:
-- 2024-01-01 | 100 | 100.0    (only 1 row available)
-- 2024-01-02 | 150 | 125.0    (100 + 150 / 2)
-- 2024-01-03 |  80 | 110.0    (100 + 150 + 80 / 3)
-- 2024-01-04 | 200 | 143.3    (150 + 80 + 200 / 3, dropped the first row)
-- 2024-01-05 | 120 | 133.3    (80 + 200 + 120 / 3)
```

**Example — Centred moving average (look both directions):**

```sql
SELECT
    order_date,
    revenue,
    AVG(revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
        -- 5-row window centred on the current row
    ) AS centred_avg_5d
FROM DailySales;
```

#### **C. `ROWS` vs `RANGE`**

Both are frame modes, but they differ in how they define "which rows count":

* **`ROWS`:** Counts physical rows. `2 PRECEDING` always means exactly 2 rows above in the sorted order, regardless of their values.
* **`RANGE`:** Counts rows by value distance. `2 PRECEDING` means all rows whose `ORDER BY` value is within 2 units of the current row's value. All rows with equal `ORDER BY` values are treated as one logical boundary.

```sql
-- Dataset: order_date, revenue
-- 2024-01-01 | 100
-- 2024-01-01 | 150   <-- same date, two rows
-- 2024-01-02 | 200

-- ROWS: exactly 1 physical row behind
SUM(revenue) OVER (ORDER BY order_date ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)
-- For the 2nd row (2024-01-01, 150): sums 100 + 150 = 250
-- For the 3rd row (2024-01-02, 200): sums 150 + 200 = 350

-- RANGE: all rows where order_date is within current date range
SUM(revenue) OVER (ORDER BY order_date RANGE BETWEEN CURRENT ROW AND CURRENT ROW)
-- For the 2nd row (2024-01-01): includes BOTH 2024-01-01 rows = 100 + 150 = 250
-- Because both rows are "within range" of 2024-01-01
```

| Mode | Boundary type | Tie behaviour | Best for |
| :--- | :--- | :--- | :--- |
| `ROWS` | Physical row count | Ignores ties — deterministic | Moving averages, rolling calculations |
| `RANGE` | Value distance | Groups tied rows together | Date-based windows where all same-day rows should count equally |

* **Critical Rule:** Default to `ROWS` for moving calculations — it is predictable. `RANGE` with numeric/date values is powerful but can silently include more rows than expected when ties exist.

---

### 5. Chapter 4 — Pivoting, ROLLUP, and CUBE

#### **A. Pivot**

**Definition:**
**Pivoting** rotates row values into column headers, transforming a "tall" dataset into a "wide" one.

* **Analogy:** You have a spreadsheet with rows like `year=2023, quarter=Q1, revenue=500`. Pivoting turns `Q1`, `Q2`, `Q3`, `Q4` into their own columns, with one row per year.

**Before pivot:**

```
year | quarter | revenue
2023 | Q1      | 500
2023 | Q2      | 600
2023 | Q3      | 450
2023 | Q4      | 700
2024 | Q1      | 550
```

**After pivot:**

```
year | Q1  | Q2  | Q3  | Q4
2023 | 500 | 600 | 450 | 700
2024 | 550 | ... | ... | ...
```

**Standard SQL approach — `CASE` + `GROUP BY`:**

```sql
SELECT
    year,
    SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS Q1,
    SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS Q2,
    SUM(CASE WHEN quarter = 'Q3' THEN revenue ELSE 0 END) AS Q3,
    SUM(CASE WHEN quarter = 'Q4' THEN revenue ELSE 0 END) AS Q4
FROM Sales
GROUP BY year
ORDER BY year;
```

* **Note (PostgreSQL):** `CROSSTAB()` from the `tablefunc` extension offers a more dynamic pivot when the number of category values is not known ahead of time.

```sql
-- PostgreSQL CROSSTAB example
SELECT *
FROM CROSSTAB(
    'SELECT year, quarter, revenue FROM Sales ORDER BY 1, 2',
    'SELECT DISTINCT quarter FROM Sales ORDER BY 1'
) AS pivot_table(year INT, Q1 INT, Q2 INT, Q3 INT, Q4 INT);
```

#### **B. `ROLLUP`**

**Use Case:** Produce subtotals along a hierarchy plus a grand total — one `GROUP BY` that generates multiple levels of aggregation automatically.

* **Analogy:** A sales report that shows per-city numbers, then a country subtotal row, then a global total row — all in one query.

**The column order inside `ROLLUP` defines the hierarchy — leftmost = highest level.**

```sql
SELECT
    country,
    city,
    SUM(revenue) AS total_revenue
FROM Sales
GROUP BY ROLLUP(country, city)
ORDER BY country NULLS LAST, city NULLS LAST;

-- Output:
-- USA   | New York | 500   (leaf: city level)
-- USA   | Los Angeles | 300
-- USA   | NULL     | 800   (subtotal: country level)
-- UK    | London   | 400
-- UK    | NULL     | 400   (subtotal: country level)
-- NULL  | NULL     | 1200  (grand total)
```

* **`NULL` in the output means "all values in this column"** — it is the marker for subtotal/total rows.
* **Critical Rule:** Column order matters. `ROLLUP(country, city)` gives country → city hierarchy. `ROLLUP(city, country)` would give city → country, which is rarely meaningful.

**Distinguishing subtotal NULLs from real NULLs — use `GROUPING()`:**

```sql
SELECT
    CASE WHEN GROUPING(country) = 1 THEN 'ALL COUNTRIES' ELSE country END AS country,
    CASE WHEN GROUPING(city)    = 1 THEN 'SUBTOTAL'      ELSE city    END AS city,
    SUM(revenue) AS total_revenue
FROM Sales
GROUP BY ROLLUP(country, city);
-- GROUPING() returns 1 when the NULL is from ROLLUP, 0 when it's a real NULL
```

#### **C. `CUBE`**

**Use Case:** Produce subtotals for **every possible combination** of the grouped columns — more exhaustive than `ROLLUP`. Best suited for cross-dimensional reporting.

```sql
SELECT
    country,
    category,
    SUM(revenue) AS total_revenue
FROM Sales
GROUP BY CUBE(country, category)
ORDER BY country NULLS LAST, category NULLS LAST;

-- Produces ALL 4 grouping combinations (2² = 4):
-- (country, category)  → leaf level
-- (country, NULL)      → subtotal per country across all categories
-- (NULL, category)     → subtotal per category across all countries
-- (NULL, NULL)         → grand total
```

**When CUBE becomes large:**
With 3 columns, `CUBE` produces 2³ = 8 groupings. With 4, it produces 16. Use `ROLLUP` when you only need one hierarchical path.

#### **D. Comparison: `GROUP BY` vs `ROLLUP` vs `CUBE`**

| Feature | `GROUP BY` | `ROLLUP(a, b)` | `CUBE(a, b)` |
| :--- | :--- | :--- | :--- |
| Groupings produced | 1 | n+1 (hierarchy levels) | 2ⁿ (all combinations) |
| Grand total row | ❌ | ✅ | ✅ |
| Column-only subtotals | ❌ | ❌ | ✅ |
| Hierarchical subtotals | ❌ | ✅ | ✅ |
| **Use when** | Simple aggregation | Drill-down reports | Full cross-dimensional BI |

---

### 6. Engineering Insight: When to Use Window Functions

1. **Prefer window functions over correlated subqueries** for row-by-row comparisons (e.g., `salary > AVG(salary)` per department). Window functions compute the aggregate once per partition; correlated subqueries re-run for every single row.

2. **`ROW_NUMBER()` is the standard deduplication tool.** Partition by the natural key, order by the freshness timestamp, and filter on `rn = 1` in an outer query.

3. **Use `LAG`/`LEAD` instead of self-joins for period comparisons.** A self-join for yesterday's revenue requires matching on date arithmetic, is harder to read, and forces the engine to scan the table twice.

4. **Default to `ROWS` mode for any moving window.** `RANGE` silently inflates the window when tied `ORDER BY` values exist, causing subtle bugs in running calculations.

5. **`LAST_VALUE` always needs `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.** Without it, the default frame stops at the current row and `LAST_VALUE` returns the current row's own value — a silent bug.

6. **Multiple window functions in one `SELECT` do not scan the table multiple times.** The database is smart enough to compute all window functions with the same `OVER()` definition in a single pass — define them freely without worrying about performance.

7. **Use `NTILE` + `CASE` for tier labelling** instead of hardcoding percentile cutoffs. It adapts automatically when the dataset grows.
