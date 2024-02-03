# Week1-2

## Resume:
This first weeks of the **Data Engineering ZoomCamp** wsa more to prepare all the infrastructure that we will use on the upcominh weeks.

We learn the fundamentals and get hands-on with **Docker**, creating containers to run our **Postgresql** database and connecting to it using both pgcli and pgAdmin.

We have taken data from NYC Taxi Data, and ingested into Postgres using Python.

After that we look into **Google Cloud Platform**, and used **Terraform** to deploy and destroy infrastructures on GCP.


## Architecture

During the course we will replicate the following architecture:

![architecture diagram](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/images/architecture/photo1700757552.jpeg)

The Datset used was from [NYC Taxi Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page). Specifically, we will use the [Yellow taxi trip records CSV file for January 2021](https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv). A dictionary to understand each field is available [here](https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf).



**Docker** is a _containerization software_ that allows us to isolate software in a similar way to virtual machines but in a much leaner way.

Docker Images

Docker containers

Docker-compose

To connect to docker we used both pgcli and pgAdmin.

The pgcli we add to install it on your local computer using:

pip install pgcli

Then we can run the docker image for postgres and pass some variables to define everything.

* 3 environment variables:
    - `POSTGRES_USER` is the username for logging into the database. We chose `root`.
    - `POSTGRES_PASSWORD` is the password for the database. We chose `root`
    - `POSTGRES_DB` is the name that we will give the database. We chose `ny_taxi`.
* The Volume, to create the mount between the host conmputer and the container.
    - `-v` points to the volume directory. The colon `:` separates the first part (path to the folder in the host computer) from the second part (path to the folder inside the container).
        - Path names must be absolute.
* The Port Mapping.
    - `-p` We map the default Postgres port to the same port in the host (5432).
* Image
    - The last argument is the image name and tag. We run the official `postgres` image on its version `13`.

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v "C://documents/dataengineer-zoomcamp2024/week1-2/ny_taxi_postgres_data:/var/lib/postgresql/data:rw" \
    -p 5432:5432 \
    postgres:13
```


Once the container is running, we can log into our database with [pgcli](https://www.pgcli.com/) with the following command:

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

`pgcli` is a handy tool but it's cumbersome to use. [`pgAdmin` is a web-based tool](https://www.pgadmin.org/) that makes it more convenient to access and manage our databases. It's possible to run pgAdmin as as container along with the Postgres container, but both containers will have to be in the same _virtual network_ so that they can find each other.

Despite this newtwork creation resolves our problem, Docker as a better solution for when we have multiple images that we want to run toghether.

### Docker Compose

Allows us to launch multiple containers using a single configuration file, so that we don't have to run multiple complex docker run commands separately.

Docker compose makes use of YAML files.

We can now run Docker compose by running the following command from the same directory where docker-compose.yaml is found. (-d to run the containers on the background)

```bash
docker-compose up -d
```

To shut down the containers we run:

```bash
docker-compose down
```

After this we can access postgres via PgAdmin using the browser on the port specified on the docker compose file, and perform our queries to the data we have loaded to there.

# Terraform

Terraform is an infrastructure as code tool that allows us to provision infrastructure resources as code, thus making it possible to handle infrastructure as an additional software component and take advantage of tools such as version control.

There are 2 important components to Terraform: the code files and Terraform commands.

The set of files used to describe infrastructure in Terraform is known as a Terraform ***configuration***. Terraform configuration files end up in `.tf` for files wtritten in Terraform language.

A simple structure for Terraform files are:
- main.tf (to define the porperties and resources)
- variables.tf (to define the variables to use)

There are 3 main blocks: `terraform`, `provider` and `resource`. There must only be a single `terraform` block but there may be multiple `provider` and `resource` blocks.

- The `terraform` block contains settings:
    - The `required_providers` sub-block specifies the providers required by the configuration. In this example there's only a single provider which we've called `google`.
        - A _provider_ is a plugin that Terraform uses to create and manage resources.
        - Each provider needs a `source` in order to install the right plugin. By default the Hashicorp repository is used, in a similar way to Docker images.
            - `hashicorp/google` is short for `registry.terraform.io/hashicorp/google` .

- The `provider` block configures a specific provider. Since we only have a single provider, there's only a single `provider` block for the `google` provider.
    - The contents of a provider block are provider-specific. The contents in this example are meant for GCP but may be different for AWS or Azure.

- The `resource` blocks define the actual components of our infrastructure.
    - `resource` blocks have 2 strings before the block: the resource ***type*** and the resource ***name***. Together the create the _resource ID_ in the shape of `type.name`.
    The resource types are defined in the Terraform documentation and refer to resources that cloud providers offer. 

### Commands:
- `terraform init` : initialize your work directory by downloading the necessary providers/plugins.
- `terraform fmt` (optional): formats your configuration files so that the format is consistent.
- `terraform validate` (optional): returns a success message if the configuration is valid and no errors are apparent.
- `terraform plan` :  creates a preview of the changes to be applied against a remote state, allowing you to review the changes before applying them.
- `terraform apply` : applies the changes to the infrastructure.
- `terraform destroy` : removes your stack from the infrastructure.

