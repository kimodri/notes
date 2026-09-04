# Creating Custom Generic Data Tests

A custom generic data test packages a reusable failing-row query behind a name and a set of arguments. It works like dbt's built-in tests, but I define the validation logic myself and can apply it to many models or columns.

## Singular versus generic tests

Both test types return rows that violate an assertion, but they are organized differently:

| Test type | Best use | How it is applied |
|:---|:---|:---|
| Singular | One specific business rule | A standalone SQL file under `tests/` |
| Generic | The same rule applied in many places | A reusable Jinja test block referenced in YAML |

If I find myself copying the same singular test and changing only a model, column, or threshold, it is probably a good candidate for a generic test.

## Where generic tests live

Custom generic test definitions normally live under `tests/generic`. They may also be placed in the `macros` directory.

```text
tests/
└── generic/
    ├── positive_value.sql
    ├── value_between.sql
    └── column_gte_other.sql
```

A file can contain more than one `{% test %}` block, but one clearly named test per file is usually easier to find.

The reusable logic is **defined once** in this directory. It is then **applied** to each model or column that needs it through a property file. The definition is not copied for every model.

## Anatomy of a generic test

A generic test is defined with a Jinja `test` block:

```sql
{% test test_name(model, column_name) %}

    select *
    from {{ model }}
    where <failing condition using {{ column_name }}>

{% endtest %}
```

The important pieces are:

* `test_name` is the name used in YAML.
* `model` represents the relation being tested.
* `column_name` represents the column where the test is attached.
* Extra arguments can be added after the standard arguments.
* The query must return failing rows.

`model` and `column_name` are provided automatically from the YAML context. I do not normally write them inside `arguments:` when applying a column-level test.

## Example 1: No explicit arguments

This test checks that a numeric column is greater than zero. It needs only the automatically supplied `model` and `column_name` arguments.

```sql
-- tests/generic/positive_value.sql
{% test positive_value(model, column_name) %}

    select
        {{ column_name }}
    from {{ model }}
    where {{ column_name }} <= 0

{% endtest %}
```

Apply it to `total_fare` in the `taxi_rides_raw` model:

```yaml
version: 2

models:
  - name: taxi_rides_raw
    columns:
      - name: total_fare
        data_tests:
          - not_null
          - positive_value
```

The intended rule is `total_fare > 0`, so the test returns values where `total_fare <= 0`.

## Example 2: One numeric argument

A fixed zero threshold is not always enough. This version accepts a configurable minimum value:

```sql
-- tests/generic/greater_than.sql
{% test greater_than(model, column_name, minimum_value) %}

    select
        {{ column_name }}
    from {{ model }}
    where {{ column_name }} <= {{ minimum_value }}

{% endtest %}
```

Apply it with `minimum_value` nested under `arguments:`:

```yaml
models:
  - name: taxi_rides_raw
    columns:
      - name: trip_distance
        data_tests:
          - greater_than:
              arguments:
                minimum_value: 0
```

This asserts `trip_distance > 0`. The test returns rows where the value is less than or equal to the argument.

## Example 3: Multiple numeric arguments

A range test needs both a lower and upper boundary:

```sql
-- tests/generic/value_between.sql
{% test value_between(model, column_name, minimum_value, maximum_value) %}

    select
        {{ column_name }}
    from {{ model }}
    where {{ column_name }} < {{ minimum_value }}
       or {{ column_name }} > {{ maximum_value }}

{% endtest %}
```

Apply both arguments together:

```yaml
models:
  - name: taxi_rides_raw
    columns:
      - name: passenger_count
        data_tests:
          - value_between:
              arguments:
                minimum_value: 1
                maximum_value: 8
```

This test treats the boundaries as valid, so values from 1 through 8 pass.

## Example 4: Passing another column name

An argument can represent another column rather than a literal value. Suppose `total_fare` must be at least as large as `fare_amount`:

```sql
-- tests/generic/column_gte_other.sql
{% test column_gte_other(model, column_name, other_column) %}

    select
        {{ column_name }},
        {{ other_column }}
    from {{ model }}
    where {{ column_name }} < {{ other_column }}

{% endtest %}
```

Attach the test to `total_fare` and pass the other column by name:

```yaml
models:
  - name: taxi_rides_raw
    columns:
      - name: total_fare
        data_tests:
          - column_gte_other:
              arguments:
                other_column: fare_amount
```

The YAML strings identify columns, and Jinja renders them as SQL identifiers. As with the earlier singular test, null values need separate `not_null` assertions when they are not allowed.

## Example 5: Passing a string argument

String arguments usually need SQL quoting inside the generic test. This test rejects timestamps earlier than a configured date:

```sql
-- tests/generic/not_before.sql
{% test not_before(model, column_name, minimum_date) %}

    select
        {{ column_name }}
    from {{ model }}
    where {{ column_name }} < cast('{{ minimum_date }}' as timestamp)

{% endtest %}
```

The date is passed as a YAML string:

```yaml
models:
  - name: taxi_rides_raw
    columns:
      - name: tpep_pickup_datetime
        data_tests:
          - not_before:
              arguments:
                minimum_date: '2009-01-01'
```

Notice the difference:

* `{{ minimum_date }}` is a Jinja substitution.
* The surrounding single quotes make the rendered value a SQL string literal.
* `cast(... as timestamp)` gives Databricks an explicit comparison type.

Arguments in project-controlled YAML should still be treated as code configuration, not unrestricted user input.

## Example 6: Passing a list

An argument can be a YAML list. This test rejects payment codes that have been retired:

```sql
-- tests/generic/not_in_values.sql
{% test not_in_values(model, column_name, disallowed_values) %}

    select
        {{ column_name }}
    from {{ model }}
    where {{ column_name }} in (
        {% for value in disallowed_values %}
        {{ value }}{% if not loop.last %}, {% endif %}
        {% endfor %}
    )

{% endtest %}
```

Apply it by supplying a list:

```yaml
models:
  - name: taxi_rides_raw
    columns:
      - name: payment_type
        data_tests:
          - not_in_values:
              arguments:
                disallowed_values: [7, 8, 9]
```

This particular implementation expects numeric values because it renders them without SQL quotes. A reusable test meant for strings would need to quote and safely handle each rendered string value.

## Example 7: An optional argument with a default

Jinja test arguments can have defaults. This range test uses inclusive boundaries unless the YAML explicitly requests exclusive ones:

```sql
-- tests/generic/value_between_configurable.sql
{% test value_between_configurable(
    model,
    column_name,
    minimum_value,
    maximum_value,
    inclusive=true
) %}

    select
        {{ column_name }}
    from {{ model }}
    {% if inclusive %}
    where {{ column_name }} < {{ minimum_value }}
       or {{ column_name }} > {{ maximum_value }}
    {% else %}
    where {{ column_name }} <= {{ minimum_value }}
       or {{ column_name }} >= {{ maximum_value }}
    {% endif %}

{% endtest %}
```

Using the default requires only the two boundaries:

```yaml
- value_between_configurable:
    arguments:
      minimum_value: 1
      maximum_value: 8
```

Overriding the optional Boolean argument looks like this:

```yaml
- value_between_configurable:
    arguments:
      minimum_value: 1
      maximum_value: 8
      inclusive: false
```

With `inclusive: false`, only values strictly between 1 and 8 pass.

## Example 8: A model-level test without `column_name`

Not every generic test belongs to one column. A model-level test can accept `model` plus its own arguments.

This test verifies that a model's row count falls within an expected range:

```sql
-- tests/generic/row_count_between.sql
{% test row_count_between(model, minimum_rows, maximum_rows) %}

    select
        count(*) as actual_row_count
    from {{ model }}
    having count(*) < {{ minimum_rows }}
        or count(*) > {{ maximum_rows }}

{% endtest %}
```

Because this test applies to the whole model, declare it under the model's `data_tests:` key rather than beneath a column:

```yaml
models:
  - name: taxi_rides_raw
    data_tests:
      - row_count_between:
          arguments:
            minimum_rows: 1000
            maximum_rows: 100000000
```

The query returns one row containing the actual count when the assertion fails, or zero rows when it passes.

## Example 9: Passing another dbt relation

An argument can also be the relation returned by `ref()`. This custom test confirms that every value exists in a field on another model:

```sql
-- tests/generic/values_exist_in.sql
{% test values_exist_in(model, column_name, comparison_model, comparison_field) %}

    select
        source_rows.{{ column_name }}
    from {{ model }} as source_rows
    left join {{ comparison_model }} as valid_rows
        on source_rows.{{ column_name }} = valid_rows.{{ comparison_field }}
    where source_rows.{{ column_name }} is not null
      and valid_rows.{{ comparison_field }} is null

{% endtest %}
```

Apply it by passing the result of `ref()` as an argument:

```yaml
models:
  - name: taxi_rides_raw
    columns:
      - name: payment_type
        data_tests:
          - values_exist_in:
              arguments:
                comparison_model: ref('payment_types')
                comparison_field: payment_type
```

This example demonstrates relation arguments, although dbt's built-in `relationships` test already handles this common rule. Prefer the built-in test unless custom behavior is actually needed.

## Arguments versus test configuration

`arguments:` supplies values to the Jinja test function. `config:` controls how dbt treats the test itself.

```yaml
models:
  - name: taxi_rides_raw
    columns:
      - name: passenger_count
        data_tests:
          - value_between:
              arguments:
                minimum_value: 1
                maximum_value: 8
              config:
                severity: warn
                store_failures: true
```

In this example:

* `minimum_value` and `maximum_value` are received by the `value_between` test block.
* `severity: warn` tells dbt to report failures as warnings under its normal threshold behavior.
* `store_failures: true` tells dbt to save the failing rows for inspection.

Framework options such as `severity`, `where`, and `store_failures` belong under `config:`, not `arguments:`.

## Running and debugging generic tests

Run all tests attached to a model with:

```bash
dbt test --select taxi_rides_raw
```

Run one generic test by its test name with:

```bash
dbt test --select test_name:value_between
```

When a test fails:

1. Read the test name and failure count in the dbt output.
2. Inspect its compiled SQL under `target/compiled`.
3. Query its stored failures when `store_failures` is enabled.
4. Confirm that every YAML argument matches the Jinja function signature.
5. Check whether numeric values, strings, lists, relations, and column identifiers are rendered with the correct SQL syntax.

YAML indentation matters. `arguments:` and `config:` must be nested beneath the custom test name, and their own values must be nested one level further.

## Choosing good arguments

Arguments should describe the parts of a rule that genuinely change between uses. A good generic test is flexible enough to reuse but still easy to understand.

Prefer:

```text
value_between(model, column_name, minimum_value, maximum_value)
```

Be cautious with a test that needs a long list of switches and unrelated settings. At that point, two focused generic tests may be easier to read, document, and debug.

## Key takeaways

* A generic data test defines reusable failing-row logic in a Jinja `test` block.
* Define the test once, then apply it to each relevant model or column in YAML.
* `model` and `column_name` are supplied automatically for column-level tests.
* Extra arguments can be numbers, strings, Booleans, lists, column names, or dbt relations.
* Current dbt syntax nests extra inputs under `arguments:`.
* Model-level tests can omit `column_name` and validate the resource as a whole.
* `arguments:` changes the test query, while `config:` changes how dbt executes or evaluates the test.
* Every generic test must still return the rows that violate its assertion.
