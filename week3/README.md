# Week3

## Orchestration

What is Orchestration?
Orchestration is the coordination and management of multiple computer systems, applications and/or services, stringing together multiple tasks in order to execute a larger workflow or process. These processes can consist of multiple tasks that are automated and can involve multiple systems.

The goal of orchestration is to streamline and optimize the execution of frequent, repeatable processes and thus to help data teams more easily manage complex tasks and workflows. Anytime a process is repeatable, and its tasks can be automated, orchestration can be used to save time, increase efficiency, and eliminate redundancies.


# Mage

![Architecture](https://github.com/PHenriquesReps/dataengineer-zoomcamp2024/blob/main/week3/image.png)

What is Mage?
Is an open-source tool for orchestrating, transferring, and integrating data.


Mage allows for a Hybrid environment 
    - Use the GUI for interactive development or the VSC.
    - Use Blocks as testable, reusable pieces of code.

Allows:
    - In-line testing and debugging
    - Fully-featured observability
    - DRY (don't repeat yourself) principles


## Core Concepts:

** Project ** 
We can have 1 or more projects. Is the overall environment.
Forms the basis for all the work we can do in Mage.
Contains the code for all our pipelines, blocks, and other assets.


** Pipelines **
Workflows that perform/execute some operation - for example. extracting, transforming. and loading data from an API.
Pipelines can contain Blocks (SQL, Python, R) and charts.
Each Pipeline is represented by a YAML file in the "pipelines" folder of our project.

** Blocks of code ** 
Files that can be executed independently or within a pipeline.
Together these blocks form the DAGs, that we call pipelines.
 They are reusable, atomic pieces of code that mage is orchestrating, based on the established dependencies.
Changing one block will change it everywhere it's used. However, we can detach blocks if we don't want those changes to propagate to them.

Anatomy of a Block:

1st - Imports
2nd - Decorator
3rd - Functions
4th - Assertion

** Note **: The only thing that gets executed or that will return anything is the code inside the function.


After understanding what Mage is and its general capabilities, we started creating ETL pipelines on it.


First, we need to run Mage and Postgres images using Docker-compose. 
After that, we open Mage at port 6789 on the browser to interact directly with the GUI.

# Connections

## Mage connection to Postgres.

Before we can get into the pipeline code, we need to first set up a Yaml profile in the `io_config.yml` file. This is where we define environmental variables that will allow us to authenticate for example to cloud providers and databases.
The `env_var()` is accessing the environmental variables that are defined in our mage-zoomcamp repository in the `.env` file.
This allows us to later reference them in our data exporter to authenticate to our local PostgreSQL instance.

## Mage connection to GCP
1- Create a Service Account with the relevant permissions
2- Create a Service Key
3- Update Mage Configurations
    - on the `io_config.yml` file, we need to update our google-connection
   
    ```bash
    GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/path/to/your/service/account/key.json"
    GOOGLE_LOCATION: EU # Optional
    ```

Then we can start creating our Pipelines using Mage, we can use SQL and/or Python to create the pipelines.

### Data Loader
Is used to load the data into Mage.

### Transformer
Is used to transform the data. 

### Data Exporter
Is used to export the data.

