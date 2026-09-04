# Working with a dbt Project

Once a dbt project and its connection profile exist, most of the work happens in a repeating cycle: develop models, run them in a safe environment, inspect the results, and fix any problems.

## The basic dbt workflow

A typical workflow looks like this:

1. Create a project with `dbt init`, or copy an existing project.
2. Configure its connections and targets in `profiles.yml`.
3. Write or update data models.
4. Run the models in the development environment.
5. Verify the results and run tests.
6. Troubleshoot problems and repeat the process.

Most development time is spent working on models and repeating steps 3–6 as requirements or source data change.

## What a model represents

A dbt model is usually a `.sql` file containing a `select` statement. It describes how raw or previously transformed data should become a useful dataset.

For example, a model could select valid customer orders from a Databricks source table:

```sql
select
    order_id,
    customer_id,
    order_total
from raw.sales.orders
where order_status = 'completed'
```

When dbt runs this model, it executes the transformation on Databricks and creates the configured output, such as a table or view.

## Running models with `dbt run`

The `dbt run` command compiles the project's model code and executes it on the selected target:

```bash
dbt run
```

Running the command without `--target` uses the default target from `profiles.yml`. To select a target explicitly, use:

```bash
dbt run --target prod
```

A **target** is an environment configuration inside a profile; it is not another name for the profile itself.

The command output reports how dbt processed each model and whether it succeeded or failed. It is worth reading this output because it identifies the model involved, its status, and useful error details.

### Running a specific model

During development, it is often faster and safer to run only the model being changed:

```bash
dbt run --select customer_orders
```

Without a selection, `dbt run` attempts to run every enabled model that matches the command's selection rules.

## What materialization means

In dbt, a **materialization** controls how a model is represented in the data platform. Running a model might create or update a view, table, incremental table, or another supported type of relation.

Materialization is not simply another word for running dbt. It is the strategy dbt uses to build the model's result.

## Tables and views

Both tables and views can be queried, but they store their results differently.

| Feature | Table | View |
|:---|:---|:---|
| What is stored | The result data | The query definition |
| Storage use | Depends on the amount of data | Usually small |
| When results change | When data is inserted, updated, deleted, or the table is rebuilt | When queried, based on the current underlying data |
| Query work | Results have already been stored | The defining query normally runs when the view is queried |

An ordinary view behaves like a table from the user's perspective, but it usually does not store a separate copy of the result data. Its query reads from one or more underlying tables or views.

The exact behavior and available materializations depend on the database or data warehouse. Databricks, for example, also supports features beyond this basic table-versus-view distinction.

## Does `dbt run` mess up development?

Running dbt changes the models in the selected development destination, but that is normally the purpose of a development environment. It should not affect production when the targets are isolated correctly.

Let's say the Databricks targets point to these destinations:

```text
dev  → development.magan_dev
prod → production.analytics
```

Running the default development target builds or replaces model objects in `development.magan_dev`:

```bash
dbt run
```

Running the production target operates on `production.analytics` instead:

```bash
dbt run --target prod
```

The effect on an existing development model depends on its materialization:

* **View** — dbt creates or replaces its view definition.
* **Table** — dbt rebuilds the table with the latest model result.
* **Incremental** — dbt adds or merges records according to the model's incremental logic.
* **Ephemeral** — dbt does not create a separate database object; its SQL is included in models that depend on it.

This means a developer can temporarily break objects in their own development schema. The important protection is isolation: each developer can use a personal schema instead of sharing the same development output.

```text
development.magan_dev
development.alice_dev
development.bob_dev
```

### Avoiding accidental production changes

Before running a project, use `dbt debug` to validate the configured connection:

```bash
dbt debug
```

Check that the active target, Databricks catalog, and schema match the intended environment. The database connection shown in VS Code does not control where dbt builds models; dbt uses the active profile and target.

Production access should also be protected with appropriate permissions. Ideally, a developer's normal credentials cannot accidentally create or replace production objects.

## Key takeaways

* dbt development is a repeating cycle of modeling, running, checking, testing, and troubleshooting.
* `dbt run` compiles and executes models on the selected target.
* A materialization determines how dbt creates a model, such as a table or view.
* Tables store result data, while ordinary views store a query definition.
* A development run is expected to change development objects.
* Separate Databricks schemas and restricted production permissions make development safer.
