# Jinja Templates in dbt

Jinja lets dbt combine SQL with reusable expressions and programming-like control flow. dbt renders the Jinja first, producing ordinary SQL, and then sends that compiled SQL to Databricks.

## What a template is

A **template** is text containing placeholders or instructions that are replaced when it is rendered. This is useful when part of a query changes while the overall pattern stays the same.

I like to think of a dbt model as having two layers:

```text
SQL + Jinja template
        ↓ dbt renders it
Compiled Databricks SQL
        ↓ Databricks executes it
Model result
```

Jinja does not normally process the table's rows. It generates the SQL that Databricks will use to process those rows.

## Recognizing Jinja syntax

Jinja uses three important delimiter styles. They do different jobs:

| Syntax | Purpose | Example |
|:---|:---|:---|
| `{{ ... }}` | Output the result of an expression | `{{ ref('stg_customers') }}` |
| `{% ... %}` | Perform logic without directly outputting a value | `{% for column in columns %}` |
| `{# ... #}` | Add a Jinja comment that will not appear in compiled SQL | `{# Explain the template logic #}` |

The transcript's idea of placing content inside double curly braces applies to **expressions**. Loops, conditions, variable assignments, and other control statements use `{% ... %}` instead.

## Useful dbt Jinja functions

dbt adds functions and variables to the standard Jinja environment. Some common ones are:

| Function | What it does |
|:---|:---|
| `ref()` | Refers to another dbt model and creates a dependency |
| `source()` | Refers to a source declared in YAML |
| `config()` | Configures the current resource, such as its materialization |
| `doc()` | Inserts a reusable documentation block into a description |
| `var()` | Reads a variable supplied to the dbt project |
| `env_var()` | Reads a value from an environment variable |

### Referring to another model

Instead of hardcoding a Databricks catalog and schema, use `ref()`:

```sql
select *
from {{ ref('stg_customers') }}
```

dbt replaces the expression with the correct relation for the active target. It also records that the current model depends on `stg_customers`, which helps determine build order and lineage.

### Configuring a model

The `config()` function sets configuration for the current model. It does not merely read existing settings:

```sql
{{ config(materialized='table') }}

select *
from {{ ref('stg_customers') }}
```

This tells dbt to materialize the model as a table.

## Removing repetitive SQL with a loop

Suppose a Databricks model needs to replace missing values in three date columns. Written directly, the SQL repeats the same expression:

```sql
select
    event_id,
    coalesce(start_date, date '1900-01-01') as start_date,
    coalesce(update_date, date '1900-01-01') as update_date,
    coalesce(end_date, date '1900-01-01') as end_date
from {{ ref('stg_events') }}
```

Jinja can generate those repeated column expressions from a list:

```sql
{% set date_columns = ['start_date', 'update_date', 'end_date'] %}

select
    event_id,
    {% for column_name in date_columns %}
    coalesce({{ column_name }}, date '1900-01-01') as {{ column_name }}{% if not loop.last %},{% endif %}
    {% endfor %}
from {{ ref('stg_events') }}
```

Here is what each part does:

* `{% set ... %}` creates the list of column names.
* `{% for ... %}` repeats the SQL once for each item.
* `{{ column_name }}` outputs the current column name.
* `loop.last` detects the final iteration so the template does not add a trailing comma.

The rendered result is ordinary SQL:

```sql
select
    event_id,
    coalesce(start_date, date '1900-01-01') as start_date,
    coalesce(update_date, date '1900-01-01') as update_date,
    coalesce(end_date, date '1900-01-01') as end_date
from development.magan_dev.stg_events
```

The exact relation produced by `ref()` depends on the active Databricks target.

## Inspecting compiled SQL

Jinja must ultimately produce valid SQL. When a templated model fails or behaves unexpectedly, inspecting the compiled version is one of the best debugging steps.

Compile the project without materializing the models:

```bash
dbt compile
```

To focus on one model, use:

```bash
dbt compile --select customer_event_dates
```

dbt writes compiled SQL under `target/compiled/<project_name>/`. Opening the original model beside its compiled SQL makes it easier to see exactly what Jinja generated.

## Quoting values inside Jinja

Strings passed to a Jinja function need quotes:

```sql
-- ✅ Passes the string "stg_customers" to ref()
from {{ ref('stg_customers') }}
```

Without quotes, Jinja looks for a variable with that name:

```sql
-- ❌ Looks for a Jinja variable named stg_customers
from {{ ref(stg_customers) }}
```

Do not add nested curly braces around an argument that is already inside a Jinja expression.

## When Jinja helps—and when it does not

Jinja is valuable when it removes meaningful repetition, handles environment-specific values, or expresses reusable project logic. It can also make a model harder to read when simple SQL would have been clearer.

A useful rule is to inspect the compiled query and ask whether another developer can still understand the transformation. A few repeated SQL lines may be easier to maintain than an overly clever template.

## Key takeaways

* dbt renders Jinja into SQL before Databricks executes the query.
* `{{ ... }}` outputs values, while `{% ... %}` controls logic.
* `ref()` resolves a model's relation and records a dependency.
* `config()` controls how the current model is built.
* Loops can generate repetitive SQL, but the result must still be valid SQL.
* `dbt compile` reveals the generated query without materializing the model.
* Jinja should improve maintainability, not hide straightforward SQL.
