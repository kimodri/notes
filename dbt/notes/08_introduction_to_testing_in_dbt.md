# Introduction to Testing in dbt

Tests in dbt are assertions about data resources such as models, sources, seeds, and snapshots. They help detect unexpected nulls, duplicates, invalid values, broken relationships, and business-rule violations before unreliable data reaches consumers.

## How a dbt data test works

A dbt data test is ultimately a SQL query that searches for records that violate an assertion.

```text
zero failing rows     → PASS
one or more failures → WARN or ERROR
```

For example, a `not_null` test does not select the valid rows. Behind the scenes, it looks for rows where the tested column is null. If it finds none, the assertion passes.

A passing test means that its specific assertion held at the time of execution. It does not prove that the entire model is correct.

## Types of tests

Modern dbt distinguishes **data tests** from **unit tests**. This topic is about data tests, which validate data already available in the warehouse.

There are two ways to define a data test:

* **Generic data test** — reusable, parameterized test logic applied through YAML.
* **Singular data test** — a one-off SQL query written for a specific assertion.

The four tests included with dbt are built-in **generic data tests**, not a separate third test type.

| Built-in test | Assertion |
|:---|:---|
| `unique` | Each non-null value in a column appears only once |
| `not_null` | The column contains no null values |
| `accepted_values` | Every value belongs to an allowed list |
| `relationships` | Each value exists in a referenced field on another resource |

Generic and singular tests can also be created for project-specific rules.

## Declaring tests in a property file

Generic data tests are attached to resources in a YAML property file under the configured model path. The file can be named `model_properties.yml`, `schema.yml`, or another meaningful name.

A model does not need a separate YAML file of its own. One property file can describe and test several models by listing their names under `models:`.

### Testing a Databricks taxi model

Suppose `taxi_rides_raw` has the following expectations:

* `ride_id` identifies each ride and must be present and unique.
* `tpep_pickup_datetime` must be present.
* `payment_type` must be one of the codes 1 through 6.
* Each `payment_type` must exist in the `payment_types` reference model.

These assertions can be declared like this:

```yaml
version: 2

models:
  - name: taxi_rides_raw
    description: Cleaned New York taxi ride records in Databricks.
    columns:
      - name: ride_id
        description: Unique identifier for a taxi ride.
        data_tests:
          - not_null
          - unique

      - name: tpep_pickup_datetime
        description: Timestamp when the passenger was picked up.
        data_tests:
          - not_null

      - name: payment_type
        description: Numeric code describing how the ride was paid.
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: [1, 2, 3, 4, 5, 6]
          - relationships:
              arguments:
                to: ref('payment_types')
                field: payment_type
```

The `arguments:` level is the current syntax for inputs required by tests such as `accepted_values` and `relationships`. Older projects may place those inputs directly beneath the test name.

Older dbt projects may also use the YAML key `tests:`. It remains a backward-compatible alias, but `data_tests:` makes the distinction from unit tests clearer.

### Understanding the relationship test

This declaration:

```yaml
- relationships:
    arguments:
      to: ref('payment_types')
      field: payment_type
```

means:

> Every non-null value in `taxi_rides_raw.payment_type` should exist in `payment_types.payment_type`.

The relationship test checks referential integrity. If the child column must also be populated, add `not_null` separately, as shown in the full example.

## Running tests

Run all tests selected for the project with:

```bash
dbt test
```

Run tests associated with one model using:

```bash
dbt test --select taxi_rides_raw
```

`dbt test` does not build the model first. During development, the model can be rebuilt and then tested with two commands:

```bash
dbt run --select taxi_rides_raw
dbt test --select taxi_rides_raw
```

Alternatively, `dbt build` builds and tests selected resources in DAG order:

```bash
dbt build --select taxi_rides_raw
```

All commands use the active target unless another target is supplied. I should make sure that testing points to my Databricks development catalog and schema.

## Understanding the output

The command output shows the status of each test:

* **PASS** — the test query returned no failing rows.
* **WARN** — failures were found, but the test was configured not to stop the run.
* **ERROR** — failures exceeded the allowed threshold and the command failed.
* **SKIP** — dbt did not execute the test, often because an upstream resource failed.

The number displayed for a failure represents records or grouped results returned by the test query, depending on how that test is written.

## Investigating failed tests

The transcript suggests finding the compiled test SQL and manually running it. That works, but there are two useful approaches.

### Inspecting the compiled SQL

dbt includes the compiled test path in its output. Compiled test queries are written somewhere under `target/compiled`, although the exact subdirectory can vary by dbt version and project structure.

Opening that SQL shows the query dbt used to find invalid records. It can be copied into the Databricks SQL editor to inspect the results.

### Storing failing rows

For a faster debugging workflow, tell dbt to save the failing rows:

```bash
dbt test --select taxi_rides_raw --store-failures
```

dbt stores each test's current failures as a relation in a test audit schema. The exact Databricks catalog and schema name depend on the target and project configuration. The command output identifies the relation that can be queried.

This is especially useful when I need to inspect actual values rather than only the number of failures.

## Fixing the cause

After finding the invalid records, determine which layer owns the problem:

* **Source issue** — the producing system or ingestion pipeline may need correction.
* **Transformation issue** — update the dbt model to clean, filter, or calculate the data correctly.
* **Incorrect assertion** — update the test if the accepted business rules have legitimately changed.

Manually deleting bad records from Databricks is usually not a sustainable fix because the next load may recreate them. Fixing the source, ingestion process, or dbt transformation makes the correction repeatable.

After making the change, rebuild and retest the affected part of the project:

```bash
dbt build --select taxi_rides_raw
```

## Key takeaways

* Data tests return failing rows; zero failing rows means the test passes.
* dbt includes four generic data tests: `unique`, `not_null`, `accepted_values`, and `relationships`.
* Generic tests are declared under `data_tests:` in resource property files.
* `relationships` checks references between resources, while `not_null` must be added separately when nulls are forbidden.
* `dbt test --select` runs tests associated with a selected resource.
* `dbt build` can build and test resources in DAG order.
* Compiled SQL and `--store-failures` help reveal the records behind a failure.
* Fixing the repeatable data or transformation process is safer than manually deleting bad records.
