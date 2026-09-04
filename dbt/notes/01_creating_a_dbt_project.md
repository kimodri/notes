# Creating a dbt Project

A dbt project keeps the files needed to transform, organize, test, and document data in one structured folder. Because it is file-based, the project can be copied, modified, and tracked with source control such as Git.

## What a dbt project contains

A dbt project brings together the main pieces dbt needs to work with data:

* **Project configuration** — settings such as the project name and folder locations.
* **Connection configuration** — details about the data platform and the environment dbt should connect to.
* **Models** — SQL queries and templates that transform source data into useful datasets.
* **Documentation** — descriptions of the data and the relationships between different parts of the project.

I like to think of the project as the container for the transformation logic, configuration, and supporting documentation.

## Creating a project with `dbt init`

The `dbt init` command creates the initial folder structure and configuration files for a new project.

Run it without a name to be prompted for the project name and database adapter:

```bash
dbt init
```

You can also provide the project name directly:

```bash
dbt init test_project
```

In that case, dbt already knows the project name and continues with the remaining setup questions, such as which available database or data warehouse adapter to use.

## Profiles and targets

The project's connection details are configured in `profiles.yml`. A **profile** contains the information dbt needs to connect to a data platform.

One profile can define multiple **targets**, such as:

* `dev` for local development
* `staging` or `test` for validating changes
* `prod` for production runs

A target is more than a path. It is a named bundle of environment settings that tells dbt **where and how to run**. Depending on the data platform, this can include the host, SQL warehouse, database or catalog, schema, credentials, and number of processing threads.

### A Databricks example

Let's say both environments use Databricks. Development writes to a personal schema, while production writes to the shared analytics schema:

```yaml
test_project:
  target: dev
  outputs:
    dev:
      type: databricks
      host: my-workspace.cloud.databricks.com
      http_path: /sql/1.0/warehouses/dev-warehouse
      catalog: development
      schema: my_dev_schema
      token: "{{ env_var('DATABRICKS_TOKEN') }}"
    prod:
      type: databricks
      host: my-workspace.cloud.databricks.com
      http_path: /sql/1.0/warehouses/prod-warehouse
      catalog: production
      schema: analytics
      token: "{{ env_var('DATABRICKS_TOKEN') }}"
```

Here, `test_project` is the profile, while `dev` and `prod` are targets inside it. The `target: dev` setting makes `dev` the default. The token is read from an environment variable instead of being written directly in the file.

Running dbt without selecting a target uses the default:

```bash
dbt run
# Uses dev and builds models in development.my_dev_schema
```

To run against production, select the target explicitly:

```bash
dbt run --target prod
# Uses prod and builds models in production.analytics
```

The exact settings available under a target depend on the database adapter.

### Targets are not Git branches

Git branches and dbt targets answer different questions:

| Concept | Question it answers | Example |
|:---|:---|:---|
| Git branch | Which version of the code am I running? | `feature/customer_model` |
| dbt target | Where and how will that code run? | `dev` or `prod` |

They are often used together during development:

1. Create a Git feature branch and change a dbt model.
2. Run that code with the `dev` target.
3. Test and review the result without changing production tables.
4. Merge the approved code into the main branch.
5. A deployment process runs the merged code with the `prod` target.

For example:

```text
feature/customer_model + dev target
→ Experimental code runs in development.my_dev_schema

main branch + prod target
→ Approved code runs in production.analytics
```

The Git branch normally is not stored in the dbt target. A CI/CD system can connect the two concepts, such as by giving each pull request its own temporary schema, but they still serve separate purposes.

## Understanding YAML

YAML currently stands for **YAML Ain't Markup Language**. It is a human-readable text format commonly used for configuration files.

Whitespace is meaningful in YAML, much like indentation in Python. Items at the same level must use matching indentation:

```yaml
outputs:
  dev:
    type: databricks
  prod:
    type: databricks
```

In this example, `dev` and `prod` are aligned because they are both entries under `outputs`.

**Critical Rule:** Be consistent with indentation. Incorrect spacing can change the structure or make the YAML invalid. Spaces are preferred over tabs.

## Why the course uses DuckDB

DuckDB is an open-source, serverless database designed for analytical workloads. Like SQLite, it runs without a separate database server process.

It works well for this course because it is:

* easy to run locally;
* designed for analytics;
* fast for analytical queries because of its vectorized execution; and
* supported by dbt through an adapter.

DuckDB is convenient for local development and learning. A platform such as Databricks may be more suitable for a shared production environment where multiple users and systems need access.

## Key takeaways

* A dbt project is a structured collection of configuration, SQL models, and documentation.
* `dbt init` creates the starting project structure.
* A profile defines connection configuration and can contain environment-specific targets such as `dev` and `prod`.
* A target is a bundle of settings such as the Databricks warehouse, catalog, and schema—not just a file path.
* `target` selects the default target.
* Git branches select a version of the code; dbt targets select where and how that code runs.
* YAML indentation defines the configuration's structure.
* DuckDB provides a simple local database for learning and development.
