# SQL Subqueries: The Data Engineer's Guide

### 1. The Core Concept

A **Subquery** (or "Nested Query") is simply a query inside another query.

* **Inner Query:** Executes first (usually) to provide data.
* **Outer Query:** Uses that data to perform the final task.

---

### 2. Standard Subqueries (The "Static" Helpers)

These run **once** for the entire operation. The database calculates the result, holds it in memory, and passes it to the outer query.

#### **A. In the `WHERE` Clause (Filtering)**

**Use Case:** Filter your main data based on a list generated from another table.

* **Analogy:** The Bouncer. "Is your name on this list?"

```sql
SELECT order_id, amount
FROM Orders
WHERE customer_id IN (
    -- Inner Query: Runs once, returns list of NY IDs [1, 5, 9]
    SELECT customer_id
    FROM Customers
    WHERE city = 'New York'
);

```

#### **B. In the `FROM` Clause (Derived Tables)**

**Use Case:** Create a temporary table on the fly to pre-aggregate data before joining.

* **Critical Rule:** You **MUST** give this subquery an alias (e.g., `AS sub`).

```sql
SELECT AVG(total_spend)
FROM (
    -- Inner Query: Shrinks table to 1 row per customer
    SELECT customer_id, SUM(amount) AS total_spend
    FROM Orders
    GROUP BY customer_id
) AS customer_totals; -- Alias is mandatory

```

#### **C. In the `SELECT` Clause (Single Value)**

**Use Case:** Calculate a single benchmark value (like a global average) and paste it onto every row.

* **Critical Rule:** Must return only **one cell** (1 row, 1 column).

```sql
SELECT
    product_name,
    price,
    (SELECT MAX(price) FROM Products) AS max_price_in_store
FROM Products;

```

---

### 3. Correlated Subqueries (The "Dynamic" Helpers)

These run **once for every single row** of the outer query. They are "Correlated" because the inner query refers to the outer query.

#### **A. The Concept: "The Loop"**

Instead of a one-time calculation, the database loops through the outer table. For every row, it pauses and runs the inner query using that row's specific ID or Category.

#### **B. The Syntax Pattern**

Look for the **"Link"** in the `WHERE` clause of the inner query.

```sql
SELECT product_name, category, price
FROM Products p1 -- Outer Alias
WHERE price = (
    SELECT MIN(price)
    FROM Products p2 -- Inner Alias
    WHERE p2.category = p1.category -- <--- THE LINK
);

```

* **Logic:** "For the toaster (Home Appliance), find the minimum price of *Home Appliances*. Does the toaster match?"

#### **C. The `EXISTS` Operator (Performance Optimization)**

This is the most common way Engineers use correlated subqueries. It checks if a relationship exists without returning heavy data. It stops looking as soon as it finds **one** match.

```sql
SELECT *
FROM Customers c
WHERE NOT EXISTS (
    -- Find if this customer has NO orders
    SELECT 1
    FROM Orders o
    WHERE o.customer_id = c.customer_id
);

```

---

### 4. Comparison: Standard vs. Correlated

| Feature | Standard Subquery | Correlated Subquery |
| --- | --- | --- |
| **Execution** | Runs **Once** total. | Runs **Once per Row** (N times). |
| **Dependency** | Independent (can run alone). | Dependent (needs outer row to run). |
| **Performance** | Generally Fast. | Can be Very Slow on big data (N+1 problem). |
| **Keyword** | Usually `IN`, `NOT IN`, `=`, `JOIN`. | Usually `EXISTS`, `NOT EXISTS`, `> AVG(...)`. |

---

### 5. Engineering Insight: When to use what?

1. **Prefer `JOIN`s** over Subqueries in `WHERE` if you need columns from both tables.
2. **Prefer `EXISTS**` over `IN` if you are checking huge tables (it handles NULLs and duplicates better).
3. **Avoid Correlated Subqueries** for calculation (like `> AVG`) on datasets with millions of rows. Use **Window Functions** instead (which we will learn soon).
