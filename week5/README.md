*Analytics Engineering*

**ETL vs ELT**

***ETL - Extract Transform Load***

- It takes longer for the data to be available on the Database, however, the data will be more stable and compliant because it was already clean.
- Higer Storage and Compute Costs


***ELT - Extract Load Transform***

- Faster and more flexible becasue the data is already loaded.
- Lower Costs and maintenance


**Dimensional Modeling**

***Kimball***

***Objective***
- Deliver data understandable to the business user
- Deliver faster query performance

***Approach***
- Denormalized data


Fact Tables
- Measurements, metrics or facts
- Corresponds to a business process
- "verbs"

Dimension Tables
- Corresponds to a business entity
- Provisdes context to a business process
- "nouns"



**What is dbt?**
dbt (data build tool) is a transformation tool that allows anyone thta knows SQL to deploy analytics code following software engineering best practices like modularity, portability, CI/CD, and documentation.

***How to use dbt?***

- dbt core
Allows the data transformation.
Builds and runs projects.
Include SQL comopilation logic, macros and database adapters.
Includes a CLI interface to run dbt commands locally

- dbt cloud
SaaS application to develop and manage dbt projects
Web-based IDE to develop, run and test a dbt project
jobs orchestartion
Logging and Alerting
Integrated Documentation



**How we are going to use dbt?**

Using BigQuery
- Development using the cloud IDE


**Create a project on dbt**

dbt provides a strater porject with all the basic folders ad files.

We can use it with:

- CLI
After installing it locally and setup the profiles.yml, run:

```bash
    dbt init
```
- dbt Cloud
After setting up the cloud credentials (repo and dwh) we strat the project on the web-based IDE.


dbt-project.yml

here we define global settings for our project like:
- name
- profile: the profile used for this project, we can change it to run for example on Postgres and then on BigQuery.



**Models**

Are used to represent objects in our model.This models are SQL Select statements with some jinja.

In the beggining of the model we will use the config macro:

- ***config***: this macro along with the parameters we will define is going to to add the DDL or DML to the model that we are writting.

By default, if we did not add this config macro to the model, it will be creating a view.

```jinja
{{
    config(
        materialized='table'
    )
}}
```

dbt provides 4 materialization startegies:
- ***Ephemeral***: simlar to have a cte. Are temporary and exist only for the duration of a single dbt run.
- ***View***: Virtual tables created by dbt that can be queried like regular tables.
- ***Table***: Physical representations of data that are created and stored in the databse.
- ***Incremental***: essentially is a table, but allow us to run our model incrementally. Run and add to our model only the latest data. Allow for efficient updates reducing the need of    full data refreshes.



***From*** clause of a dbt model:

- Sources
    Using the macro source, that we define in a yml file, that represent the connection to our data base.
    ``` form {{ source('sources_name', 'table_name') }} ```


- Seeds
    CSV files stored in our repository. Is like a copy command, it creates a table.
    Runs with ``` dbt seed -s file_name ```.
    Recommended for samller files with data that doesn't change frequently.


- Ref
    Is a macro that allows us to reference underlying tables and views that we have in the Data Warehouse.
    Run the same code in any environment, resolving the correct schema.
    Dependencies are build automatically.
    ``` from {{ ref('dbt_table/view_name') }} ```


Defining the sources macro in the schema.yml:

``` yml
version: 2
sources:
    - name: staging                     # Source name
      database: dataenginner-zoomcamp   # Represents the database(dataset) we have created on BigQuery
      schema: taxi_tripsdata            # The schema we have created with our source tables on BigQuery

      tables:
        - name: green_taxi              # table name on BigQuery
        - name: yellow_taxi 
```



**Macros**

Are like functions that can be used in multiple mdoels.
dbt has already some macros that we can use like: config, source, but we can define our own.

Macros doesn't retrun the final result, they return the code.

We create the macros under the Macros folder.

In jinja:
```jinja
{#
    This is a comment
#}
{% macro name_of_the_macro(params) -%}
    SQL Code
{%- endmacro %}
```


**Packages**

Using a macro from another project in the actual prtoject. Like using libraries that we can import to our project.
By adding this packages, trhe models and macros will become parto  of our own project.
We have to create a ``` packages.yml ``` file on the main directory of our project (at the same level as the dbt_project.yml). 
we can also import some packages form dbt on dbt package hub - https://hub.getdbt.com/.
After creating this ``` packages.yml ``` file we run the command ``` dbt deps ``` this will install all the dependencies that we brought from the packages.yml.



**Variables**

To define values that should be used across the project.
To use a variable we use the function:

``` {{ var('var_name') }} ```

Variables can be defined in 2 ways:
1- In dbt_project.yml file (global variables)
2- On the command line (it's value can be changed on the CLI)

We can define variables like this:

1- dbt_project.yml
``` yml 
        vars:
            var_name: var_value
```

2- 
```
    {% if var('is_test_run', default=True) %}
        limit 100
    {% endif %}
```

By default this value will be True so we will limit our results to 100.
We can chnage that value when running the model:
``` dbt build --select <model.sql> --vars '{'is_test_run': 'False'}'  ```



**Seeds**

Working with the dbt cloud we don't have a way of uploading a file directly to our working project.
We have 2 options, commit the poject and upload the file to git and then pulling it on dbt cloud. Or create the file manually.

If we are working ocally we can copy the file into dbt core.

then we run 
``` dbt seed ```

This will create the table based on the file into the database.

If any chnage happens to the file and we run the previous command again, by default, it will append the new values to the existing table. - DBT SEED CHANGE THE VALUE AND DO NOT APPEND.
To enforce a drop and creation of a new table werun this command:

``` dbt seed --full-refresh ```


To run the entier lineage model and seed que can do:

``` dbt build ```

to run a specific model and all of its dependencies we can do:
``` dbt build --select +<model_name> ```


**Tests**

Tests in dbt are essentially a select SQL query.
They are assumptions that we make about our data, thhese assumptions are compiled to SQL that return the amount of failing records.
Tests are defined on a column in the .yml file
dbt provides 4 tests out of the box, to check if the colum values are:
    - Unique
    - Not null
    - Accepted values
    - A foreign key to another table

We can create our own test or use packages.
Some usefull packages that we can use are: 
- dbt_utils
- dbt_expectations



***Severity:***
- Warn: continue runing but show the warning on the terminal.
- Never: stop runing
- Error: 

To run the tests we can do:

``` dbt test ``` 

We can also chose the model we want to run the tests, or a specific test.

If we do ``` dbt build ``` it will run all the tests.

The name of the test combine the name of the test, the name of the model and the name of the field, for example:

```accepted_values_stg_green_tripdata_Payment_type__False___var_payment_type_values_```



**Documentation**

dbt provides a way to generate documentation for our project and render it as a website.
This documentation includes:
- Information about the project
    - Model code (both form .sql and compile code)
    - Model dependencies
    - Sources
    - Auto generated DAG from the ref and sources macros
    - Descriptions from .yml file and tests

- Information about the Data Warehouse
    - Column names and data types
    - tables stats like size and rows

The documentation for the models is done on the schema.yml under the models tag, here we also can describe the columns one by one adding the tests we wnat to perform in each one.

To generate the documentation we can run:
``` dbt docs generate ```


**Deployment**

Take the project into production.
- Runing the models we created in our development environment in a production environment
- A deployment  environment will normally have a different schema in our DW and ideally a different user
- A development - deployment workflow will be something like:
    - Develop in a user branch
    - Create a pull request to merge into the main branch
    - Merge to main branch
    - Run the models in production with some additional changes
    - Schedule the models


***dbt project in Production:***

- dbt cloud includes a scheduler where we can create jobs to run in production.
- A single job can run multiple commands.
- Jobs can be triggered manually or on a schedule or via an API. This will share a lot of metadata that we can used afterwards.
- Each job will keep a log of the runs over time.
- A job couls also generate documentation that could be viewed under the run information.
- If dbt source freshness was run, the results can be viewed ate the end of a job.


***Continuous Integration (CI)***

- Is the practice of regularly merge development branches into a central repository, after which automated builds and tests are run.
- The gosl is to reduce adding bugs to teh production code and maintain a mopre stable project.
- dbt allows to enable CI on pull requests
- When a PR is ready to be merged, a webhooks is received in the dbt cloud that will enqueu a new run of the specific job.
- The run of the CI job will be against a temporary schema
- No PR will merge if the run is not completed successfully.



