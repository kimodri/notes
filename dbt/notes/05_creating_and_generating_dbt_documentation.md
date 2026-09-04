# Creating and Generating dbt Documentation

dbt documentation turns project definitions and warehouse metadata into a searchable view of the data project. It gives engineers and data consumers a shared place to understand models, columns, tests, and lineage without requiring everyone to read the source code.

## Why documentation matters

Comments inside SQL are useful for developers, but many data consumers do not have access to the dbt repository. Centralized documentation gives them a known place to answer questions such as:

* What does this model represent?
* What does each column mean?
* Where did the data come from?
* Which models depend on this data?
* What tests are applied?
* How often should the data update?
* Who should use this dataset, and for what purpose?

Documentation can also record examples, known limitations, ownership, change information, and service-level agreements (SLAs). An SLA might describe the expected refresh time or availability of a dataset. These details normally need to be written by the team; dbt cannot infer every business meaning or promise automatically.

## Where dbt gets documentation

dbt combines information from several places:

* **Property files** provide descriptions, tests, and other declared metadata.
* **SQL models** provide the transformation code.
* **`ref()` and `source()` calls** define dependencies used to construct lineage.
* **Databricks metadata** provides information such as relation columns and data types when dbt can inspect them.

The generated documentation can show the project's directed acyclic graph, or **DAG**. This graph represents how data flows from sources through intermediate models to final datasets.

```text
Databricks source
       ↓
stg_customers
       ↓
customer_orders
       ↓
customer_summary
```

It is called *acyclic* because a model cannot eventually depend back on itself. That would create a circular dependency with no valid build order.

## Adding model and column descriptions

Descriptions are normally declared in a `.yml` property file under a configured model path. One property file can document multiple models; each entry is connected to its SQL model through the model's `name`.

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

      - name: full_name
        description: Customer's first and last names combined for display.
```

A model or column does not need a description to appear in the generated documentation. If dbt can inspect the Databricks relation, undocumented columns can still appear, but their business meaning will be missing.

Good descriptions explain meaning rather than repeat the identifier:

```yaml
# ❌ Repeats the column name without explaining it
description: The customer status.

# ✅ Explains the values and their meaning
description: Current account state: active, suspended, or closed.
```

## How lineage is created

dbt understands a dependency when a model uses `ref()` to refer to another model or `source()` to refer to a declared source.

For example, a staging model can read from a declared Databricks source:

```sql
-- models/staging/stg_customers.sql
select
    customer_id,
    first_name,
    last_name
from {{ source('crm', 'customers') }}
```

A downstream model can then depend on `stg_customers`:

```sql
-- models/marts/customer_names.sql
select
    customer_id,
    concat(first_name, ' ', last_name) as full_name
from {{ ref('stg_customers') }}
```

This creates a lineage relationship that dbt can display:

```text
source: crm.customers → stg_customers → customer_names
```

Hardcoding `raw.crm.customers` in SQL may work on Databricks, but it does not give dbt the same explicit source dependency. Using `source()` and `ref()` also lets dbt resolve the correct catalog and schema for the active environment.

## Generating the documentation site

To see the available documentation commands, run:

```bash
dbt docs -h
```

Generate the documentation with:

```bash
dbt docs generate
```

This processes the project and writes documentation artifacts and static website files under the project's `target` directory by default. It should be rerun when models, properties, tests, or warehouse metadata change.

A practical local workflow is:

```bash
dbt build --target dev
dbt docs generate --target dev
```

Building first makes sure the development models and tests are current. Documentation generation is a separate step and does not replace running or testing the models.

The exact generated artifacts vary between dbt versions. Current dbt Docs still uses `dbt docs generate` to export a static documentation site.

## Viewing documentation locally

Start dbt's local documentation server with:

```bash
dbt docs serve
```

This serves the generated site and normally opens it in a browser. A different port can be selected when necessary:

```bash
dbt docs serve --port 8081
```

`dbt docs serve` is intended as a convenient local preview. It is not a production web server and should not be exposed publicly.

## Sharing documentation

Because the generated documentation is a static site, it can be published using a controlled static hosting service. Possible destinations include cloud object storage or an organization's existing web platform.

Before publishing it, consider:

* who is allowed to see model and column names;
* whether SQL code or warehouse metadata is sensitive;
* how access will be authenticated;
* when the documentation should be regenerated; and
* who owns outdated or missing descriptions.

Teams using the dbt platform can use its Catalog experience instead of managing a static site themselves. The available metadata and features depend on the dbt product and version in use.

## What the documentation can show

A generated dbt documentation experience can include:

* model and source descriptions;
* column names, descriptions, and data types;
* model SQL;
* declared tests;
* upstream and downstream lineage; and
* warehouse metadata available to the active dbt connection.

Warehouse details such as relation size depend on the data platform, permissions, and metadata that dbt can retrieve. Documentation describes tests and may show their metadata, but documentation generation itself is not the same as executing those tests.

## Key takeaways

* dbt documentation gives engineers and data consumers a shared view of the project.
* Descriptions live in property files and can cover models, columns, sources, and other resources.
* `ref()` and `source()` create explicit dependencies that power the lineage graph.
* `dbt docs generate` produces the documentation site and its artifacts.
* `dbt docs serve` is useful for local preview, not public production hosting.
* Documentation must be regenerated as the project and its warehouse metadata change.
* Business meaning, ownership, examples, and SLAs still require thoughtful input from the team.
