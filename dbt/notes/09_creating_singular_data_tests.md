# Creating Singular Data Tests in dbt

A singular data test is a custom SQL query written for one specific assertion. Instead of returning valid data, the query returns the rows that violate the rule. The test passes only when the query returns zero rows.

## What makes a test singular

Singular tests are useful for business rules that are too specific for dbt's built-in generic tests.

Each singular test:

* is a `.sql` file;
* normally lives in the project's `tests` directory;
* contains one query that returns failing rows; and
* gets its test name from the filename.

For example:

```text
tests/
└── assert_order_total_gte_subtotal.sql
```

A descriptive and unique filename matters because it appears in dbt's output and makes failures easier to identify.

## Think in terms of failing rows

Suppose the business rule is:

> Every order total must be greater than or equal to its subtotal.

The test query should search for the opposite condition:

```text
Expected rule:  order_total >= subtotal
Failing case:   order_total < subtotal
```

This can feel backward at first, but the mental model is simple:

```text
test query returns 0 rows → PASS
test query returns rows   → FAIL
```

## Creating the test with `ref()`

The test can use `ref()` to point to the `orders` dbt model:

```sql
-- tests/assert_order_total_gte_subtotal.sql
select
    order_id,
    subtotal,
    order_total
from {{ ref('orders') }}
where order_total < subtotal
```

Using `ref('orders')` does two things:

* it resolves the correct Databricks catalog, schema, and relation for the active target; and
* it tells dbt that the test depends on the `orders` model.

For a development target, the compiled query might refer to:

```sql
from development.magan_dev.orders
```

The singular test file should contain the query only—do not include `create table` or `create view`. It is also safest to omit the final semicolon because dbt wraps test SQL inside other SQL when it runs the assertion.

## Null values need a separate decision

The comparison `order_total < subtotal` does not catch null values. In SQL, a comparison involving `null` evaluates to unknown rather than true, so those rows are not returned by the filter.

If both values are required, add generic `not_null` tests in the model's property file:

```yaml
version: 2

models:
  - name: orders
    columns:
      - name: subtotal
        data_tests:
          - not_null

      - name: order_total
        data_tests:
          - not_null
```

This keeps the responsibilities clear:

* Generic tests confirm that the required amounts are present.
* The singular test confirms that the two amounts follow the business rule.

The rule itself should also match the business definition. Discounts or credits might legitimately make an order total smaller than its subtotal, so the test should be agreed on with the people who own the metric.

## Running a singular test

Run every test in the project with:

```bash
dbt test
```

Run only the singular test by its filename without `.sql`:

```bash
dbt test --select assert_order_total_gte_subtotal
```

Selecting one test is helpful in a large project because it avoids rerunning unrelated tests while debugging.

To save its failing rows in Databricks for inspection, add `--store-failures`:

```bash
dbt test --select assert_order_total_gte_subtotal --store-failures
```

## A practical development workflow

When creating a singular test:

1. Write the failing-row query in a Databricks SQL editor.
2. Confirm that the query returns only records that violate the rule.
3. Save it as a uniquely named `.sql` file under `tests/`.
4. Replace hardcoded dbt model names with `ref()`.
5. Run only the new test with `dbt test --select`.
6. Inspect the compiled SQL or stored failures if it fails.
7. Fix the correct layer and rerun the model and test.

Testing the query in a SQL editor first helps separate ordinary SQL mistakes from dbt or Jinja problems.

## Debugging a failure

If the test fails, start by inspecting the returned rows rather than immediately changing or deleting data.

Ask:

* Is the dbt model calculating `subtotal` or `order_total` incorrectly?
* Is the source data invalid?
* Is the assertion missing a legitimate business case?
* Is the test running against the intended Databricks target?

dbt writes the compiled test query under `target/compiled`. Its output usually points to the relevant file. Running that SQL in Databricks shows the records that caused the failure.

After correcting the model or the test, rebuild and test the relevant model:

```bash
dbt build --select orders
```

## What happens when the target changes

dbt evaluates `ref()` for the active target whenever the test is compiled and run. Changing a profile or target does not automatically mean the entire project must always be rerun first.

However, the referenced model must exist and contain current data in the new target. If I switch to another Databricks target that does not yet have the `orders` model, I should build it there before testing:

```bash
dbt build --select orders --target dev
```

This builds the selected model and runs its attached tests in the chosen environment.

## Key takeaways

* A singular test is one SQL file containing a query that returns failing rows.
* Zero returned rows means the test passes.
* Use `ref()` so the test follows the active Databricks target and becomes part of the DAG.
* Use a clear, unique filename because it becomes the test's name.
* SQL comparisons do not catch nulls automatically; test required values separately.
* `dbt test --select` runs one test without executing the full test suite.
* Build the referenced model when switching to a target where it does not yet exist or is outdated.
* Investigate whether the failure belongs to the source, transformation, or assertion before applying a fix.
