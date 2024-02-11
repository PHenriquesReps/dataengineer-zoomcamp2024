# Data Warehouse

This lesson will cover the topics of _Data Warehouse_ and _BigQuery_.
# OLAP vs OLTP

_[Video source](https://www.youtube.com/watch?v=jrHljAoD6nM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=25)_

In Data Sxience, when we're discussing data processing systems, there are 2 main types: **OLAP** and **OLTP** systems.

* ***OLTP***: Online Transaction Processing.
* ***OLAP***: Online Analytical Processing.

An intuitive way of looking at both of these systems is that OLTP systems are "classic databases" whereas OLAP systems are catered for advanced data analytics purposes.

|   | OLTP | OLAP |
|---|---|---|
| Purpose | Control and run essential business operations in real time | Plan, solve problems, support decisions, discover hidden insights |
| Data updates | Short, fast updates initiated by user | Data periodically refreshed with scheduled, long-running batch jobs |
| Database design | Normalized databases for efficiency | Denormalized databases for analysis |
| Space requirements | Generally small if historical data is archived | Generally large due to aggregating large datasets |
| Backup and recovery | Regular backups required to ensure business continuity and meet legal and governance requirements | Lost data can be reloaded from OLTP database as needed in lieu of regular backups |
| Productivity | Increases productivity of end users | Increases productivity of business managers, data analysts and executives |
| Data view | Lists day-to-day business transactions | Multi-dimensional view of enterprise data |
| User examples | Customer-facing personnel, clerks, online shoppers | Knowledge workers such as data analysts, business analysts and executives |



# What is a Data Warehouse?

A **Data Warehouse** (DW) is an ***OLAP solution*** meant for ***reporting and data analysis***.

A DW receives data from different ***data sources*** which is then processed in a ***staging area*** before being ingested to the actual warehouse (a database) and arranged as needed. DWs may then feed data to separate ***Data Marts***; smaller database systems which end users may use for different purposes.



# BigQuery


BigQuery (BQ) is a Data Warehouse solution offered by Google Cloud Platform.
* BQ is ***serverless***. There are no servers to manage or database software to install; this is managed by Google and it's transparent to the customers.
* BQ is ***scalable*** and has ***high availability***. Google takes care of the underlying software and infrastructure.
* BQ has built-in features like Machine Learning, Geospatial Analysis and Business Intelligence among others.
* BQ maximizes flexibility by separating data analysis and storage in different _compute engines_, thus allowing the customers to budget accordingly and reduce costs.


## External tables

An ***external table*** is a table that acts like a standard BQ table. The table metadata (such as the schema) is stored in BQ storage but the data itself is external.

```sql
CREATE OR REPLACE EXTERNAL TABLE `dataenginner-zoomcamp.taxi_data.external_green_tripdata_2022`
OPTIONS (
  format = 'parquet',
  uris = [
    'gs://ph-taxi-data/green_taxi/7d18ddad719a47b4b24a75a51e574046-0.parquet'
    ]
);

```

BQ will figure out the table schema and the datatypes based on the contents of the files.

Be aware that BQ cannot determine processing costs of external tables.

You may import an external table into BQ as a regular internal table by copying the contents of the external table into a new internal table. For example:

```sql
CREATE OR REPLACE TABLE `dataenginner-zoomcamp.taxi_data.managed_green_tripdata` AS 
    Select 
        * 
    from 
        `taxi_data.external_green_tripdata_2022`;
```


## Partitions


You may partition a table by:
* ***Time-unit column***: tables are partitioned based on a `TIMESTAMP`, `DATE`, or `DATETIME` column in the table.
* ***Ingestion time***: tables are partitioned based on the timestamp when BigQuery ingests the data.
* ***Integer range***: tables are partitioned based on an integer column.


Querying a partitioned table is identical to querying a non-partitioned table, but the amount of processed data may be drastically different.


```sql
SELECT table_name, partition_id, total_rows
FROM `{schema_name}.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = '{table_name}'
ORDER BY total_rows DESC;
```

This is useful to check if there are data imbalances and/or biases in your partitions (Partition Skew).


## Clustering

***Clustering*** consists of rearranging a table based on the values of its columns so that the table is ordered according to any criteria. Clustering can be done based on one or multiple columns up to 4; the ***order*** of the columns in which the clustering is specified is important in order to determine the column priority.


Clustering may improve performance and lower costs on big datasets for certain types of queries, such as queries that use filter clauses and queries that aggregate data.