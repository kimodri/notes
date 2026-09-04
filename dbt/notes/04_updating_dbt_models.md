# Updating dbt Models

dbt models are meant to change as requirements, source data, and business logic evolve. Instead of starting over, I can update the existing SQL and configuration, rebuild the affected models in development, verify the results, and commit the change to Git.

## Why models need updates

A model might need to change because:

* a requirement was added or clarified;
* the original transformation is incomplete;
* the SQL contains a bug;
* a source table or column changed;
* data moved to a different source location;
* the output must move to another Databricks catalog or schema; or
* the model needs a different materialization.

Keeping transformations in a dbt project makes these changes easier to review and track. Git is not required to run dbt, but it provides a history of what changed, why it changed, and who changed it.

## A practical update workflow

A safe workflow separates code changes from production data changes:

1. Get the latest dbt project from Git.
2. Create or switch to a feature branch.
3. Find the affected `.sql` or `.yml` files.
4. Update the transformation or configuration.
5. Run the affected model against a personal Databricks development schema.
6. Test and inspect the result.
7. Commit the verified changes for review.
8. Merge and deploy through the team's normal production process.

For a project that is not already on the computer, start by cloning it:

```bash
git clone <repository-url>
cd <project-directory>
```

For normal development, a feature branch keeps the code change separate from the main branch:

```bash
git switch -c update-customer-model
```

The Git branch controls **which version of the code** I am editing. The dbt target controls **where that code runs**.

## Updating a SQL model

Let's say `stg_customers.sql` originally selects only a customer's name:

```sql
-- models/staging/stg_customers.sql
select
    customer_id,
    first_name,
    last_name
from raw.crm.customers
```

A new requirement asks for the full name and only active customers. I can update the existing model instead of creating a completely separate query:

```sql
-- models/staging/stg_customers.sql
select
    customer_id,
    first_name,
    last_name,
    concat(first_name, ' ', last_name) as full_name
from raw.crm.customers
where account_status = 'active'
```

I can then build only this model in my Databricks development environment:

```bash
dbt run --select stg_customers
```

If my active target points to `development.magan_dev`, the change affects the development relation rather than `production.analytics`.

After the run, I should inspect both the command output and the resulting data. A successful command means dbt executed the SQL; it does not guarantee that the business logic is correct.

## When to use a full refresh

The full-refresh option is written as `--full-refresh`, with `-f` as its shorter form:

```bash
dbt run --select customer_orders --full-refresh
```

This option is mainly relevant to **incremental models**. Instead of processing only new or changed records, dbt rebuilds the incremental model from scratch.

A full refresh can be useful when:

* incremental logic has changed;
* historical records must be recalculated;
* the existing incremental table has an incompatible structure; or
* earlier incremental runs produced incorrect stored results.

It can take much longer and consume more Databricks compute because it processes the complete dataset. It is also not a general fix for incorrect SQL: if the transformation logic is wrong, the query still needs to be corrected.

## Files that can be updated

Model behavior is not controlled only by `.sql` files. dbt projects also use YAML files for project configuration, model properties, tests, and documentation.

### `dbt_project.yml`

Each dbt project has one `dbt_project.yml` file at its root. It contains project-level information such as:

* the project name;
* the profile name;
* model and other resource paths; and
* default or scoped resource configurations.

Model configurations in this file can apply across the project or be narrowed to a folder or individual model. For example:

```yaml
name: customer_analytics
profile: customer_analytics

model-paths:
  - models

models:
  customer_analytics:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

This configuration creates models under `models/staging` as views and models under `models/marts` as tables. The settings are project configuration, but they do not have to apply identically to every model.

### Model property files

A model property file describes dbt resources. It can contain model descriptions, column documentation, tests, and other properties.

The file is sometimes called `model_properties.yml` or `schema.yml`, but the filename is not special. It can use any clear name ending in `.yml` as long as dbt can discover it under a configured model path.

**Critical Rule:** A separate YAML file is **not required for every model**. A SQL model can run without a property file, although it will not have any documentation, tests, or other properties that would have been declared there.

dbt connects a YAML entry to a SQL model through the entry's `name`, not through the YAML filename. The name must match the model's filename, including case:

```text
models/staging/stg_customers.sql
                       ↓
YAML entry: name: stg_customers
```

One YAML file can describe several models. For example, `staging.yml` could contain the properties for both `stg_customers.sql` and `stg_orders.sql`:

```yaml
version: 2

models:
  - name: stg_customers
    description: One cleaned record for each active customer.
    columns:
      - name: customer_id
        description: Unique identifier for the customer.
        data_tests:
          - not_null
          - unique

  - name: stg_orders
    description: One cleaned record for each order.
    columns:
      - name: order_id
        description: Unique identifier for the order.
        data_tests:
          - not_null
          - unique
```

A project can also contain multiple property files. dbt reads the files under the configured model paths and matches their entries to the named resources.

The organization is a team choice. Common patterns include:

* **One file per folder or subject area** — `staging.yml` describes all staging models.
* **One file per model** — `stg_customers.yml` sits beside `stg_customers.sql`.
* **A mixture** — simple related models share a file, while a complex model gets its own file.

For example, grouping properties by folder keeps the number of files manageable:

```text
models/
├── staging/
│   ├── stg_customers.sql
│   ├── stg_orders.sql
│   └── staging.yml
└── marts/
    ├── customer_orders.sql
    └── marts.yml
```

The important part is that the YAML remains easy to find and its `name` entries match the models they describe. The YAML filename does not have to match a model filename.

## Verifying an update

After updating a model, run and test the smallest useful selection:

```bash
dbt run --select stg_customers
dbt test --select stg_customers
```

Then review the Databricks output for unexpected row counts, missing values, duplicates, or incorrect calculations. Once the change behaves correctly, commit it to Git:

```bash
git add models/staging/stg_customers.sql models/staging/staging.yml
git commit -m "Update active customer model"
```

## Key takeaways

* Update existing models when requirements, logic, or data locations change.
* Test changes in a personal Databricks development schema before production.
* `dbt run --select` limits a development run to the relevant models.
* `--full-refresh` rebuilds incremental models from scratch and can be expensive.
* `dbt_project.yml` holds project configuration and can scope settings by folder or model.
* A model does not require its own property file; one `.yml` file can describe multiple models by name.
* A successful dbt run still requires checking that the resulting data is correct.
