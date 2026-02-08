# SQL CTEs: The Data Engineer's Guide

### 1. The Core Concept

A **CTE (Common Table Expression)** is a temporary result set that you define at the very top of your query.

* **Think of it as:** A "Variable" that holds a table.
* **Lifetime:** It exists only for the millisecond that the query runs, then disappears.
* **Key Keyword:** `WITH`.

### 2. Standard Syntax

Always define the CTE first, then write the query that uses it.

```sql
WITH high_value_orders AS (
    -- Define the logic here
    SELECT order_id, amount
    FROM Orders
    WHERE amount > 500
)
-- Use it immediately like a normal table
SELECT *
FROM high_value_orders;

```

### 3. Chaining CTEs (The Pipeline Pattern)

You can define multiple CTEs to break a complex problem into sequential steps. Use a comma `,` to separate them.

**Syntax:**

```sql
WITH step_1 AS (
    SELECT ...
),
step_2 AS (
    SELECT ... FROM step_1 -- referring to previous step
),
step_3 AS (
    SELECT ... FROM step_2 -- referring to previous step
)
SELECT * FROM step_3;

```

### 4. CTE vs. Subquery: When to use which?

| Feature | CTE (`WITH`) | Subquery (`SELECT ... FROM (SELECT...)`) |
| --- | --- | --- |
| **Readability** | **High** (Top-to-bottom flow) | **Low** (Inside-out flow) |
| **Reusability** | Can be referenced multiple times in the same query. | Must be rewritten every time (unless simple logic). |
| **Recursion** | Can reference itself (Advanced). | Cannot reference itself. |
| **Performance** | Same as Subquery (in most modern databases). | Same as CTE. |

**Pro Rule:** If you need to nest more than one level deep (a subquery inside a subquery), **STOP** and rewrite it as a CTE chain.
