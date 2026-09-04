# What Is a dbt Model?

The word *model* has a broad meaning in data work, but dbt uses it in a specific way. A dbt model is transformation logic—usually a SQL `select` statement—that dbt turns into an object such as a view or table in the target data platform.

## The general idea of a data model

A **data model** describes how a dataset is organized and how people should interpret it. It identifies the things being represented, their attributes, and the relationships between them.

For example, an animal dataset might contain:

| species | number_of_legs | can_fly | is_venomous |
|:---|:---|:---|:---|
| Eagle | 2 | true | false |
| Cobra | 0 | false | true |

Choosing these columns creates a shared definition of what information matters when describing an animal. A different purpose might require other attributes, such as habitat or conservation status.

Every data model involves trade-offs. Adding more attributes can make it more useful, but it can also increase complexity, processing work, and storage requirements. The right design depends on how people need to use the data.

## What model means in dbt

In dbt, a **model** is a reusable data transformation. A SQL model normally consists of a `select` statement saved in a `.sql` file inside the project's `models` directory.

The model file describes the desired result. dbt handles creating that result in Databricks according to the configured materialization, such as a view or table.

```text
Raw Databricks data
        ↓
SQL transformation in a dbt model
        ↓
View or table in the target catalog and schema
```

dbt can also support Python models on compatible data platforms, but this course focuses on SQL models.

## Creating a simple model

Let's create a staging model that selects customer names from a Databricks table.

First, place the SQL file under the project's `models` directory. Subfolders help organize related models, and their names may also be used later for configuration.

```text
models/
└── staging/
    └── stg_customers.sql
```

The model contains the transformation query:

```sql
-- models/staging/stg_customers.sql
select
    customer_id,
    first_name,
    last_name
from raw.crm.customers
```

In this Databricks relation name:

* `raw` is the catalog.
* `crm` is the schema.
* `customers` is the table.

Run only this model during development with:

```bash
dbt run --select stg_customers
```

By default, the filename becomes the model's name. Where dbt creates the result depends on the active target's catalog and schema, while its materialization determines whether the result is a view, table, or another supported relation.

For example, if the active development target uses `development.magan_dev`, the model could be created as:

```text
development.magan_dev.stg_customers
```

## Models describe transformations

The SQL file does not normally contain commands such as `create table` or `create view`. It contains the query that produces the desired dataset, and dbt generates the required creation statements.

This separation lets the same model logic be materialized differently through configuration. For example, a lightweight staging model could be a view during development and a table where persisted results are useful.

## Understanding Parquet

**Parquet** is a binary, column-oriented file format designed for efficient storage and analytical queries. Instead of organizing values primarily by row, it stores values from the same column together. This lets an analytics engine avoid reading unrelated columns from a wide dataset.

Parquet is useful for storing and exchanging large datasets because it supports compression and preserves schema information. It is not accurate to say that all database tables are row-based; databases and warehouses may use row-oriented, column-oriented, or other storage layouts.

### Reading a Parquet file in Databricks

Databricks can query Parquet files directly. For example, a file in a Unity Catalog volume can be read with the `read_files` table-valued function:

```sql
select *
from read_files(
    '/Volumes/main/raw/source_files/customers.parquet',
    format => 'parquet'
)
```

A dbt model could use this query as its input and then select, rename, filter, or derive columns from the file.

Databricks commonly uses **Delta Lake** for managed analytics tables. Delta tables store their data in Parquet files and add a transaction log for features such as reliable updates and table history.

## Key takeaways

* A general data model defines how data is organized and understood.
* A dbt model defines a transformation and is usually a SQL `select` statement in a `.sql` file.
* dbt turns the model query into a view, table, or another configured materialization.
* A model's filename normally becomes its name.
* The active target determines the Databricks catalog and schema where the result is built.
* Parquet is a column-oriented file format that Databricks can query directly.
