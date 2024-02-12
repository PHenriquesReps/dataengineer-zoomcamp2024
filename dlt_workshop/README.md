*dlt*

**What is dlt?**

dlt is a python library created for the purpose of assisting data engineers to build simpler, faster and more robust pipelines with minimal effort.

You can think of dlt as a loading tool that implements the best practices of data pipelines enabling you to just “use” those best practices in your own pipelines, in a declarative way.

This enables you to stop reinventing the flat tyre, and leverage dlt to build pipelines much faster than if you did everything from scratch.

dlt automates much of the tedious work a data engineer would do, and does it in a way that is robust. dlt can handle things like:

- Schema: Inferring and evolving schema, alerting changes, using schemas as data contracts.
- Typing data, flattening structures, renaming columns to fit database standards. In our example we will pass the “data” you can see above and see it normalised.
- Processing a stream of events/rows without filling memory. This includes extraction from generators.
- Loading to a variety of dbs or file formats.


dlt is an open-source library that you can add to your Python scripts to load data from various and often messy data sources into well-structured, live datasets.

You can install it using pip and there's no need to start any backends or containers. You can simply import dlt in your Python script and write a simple pipeline to load data from sources like APIs, databases, files, etc. into a destination of your choice.


**Benefits**

- Efficient Data Extraction and Loading
- Automated Schema Management
- Data Governance Support
- Flexibility and Scalability
- Post-Loading Transformations



**Extract Data**

Most data is stored behind an API

- Sometimes that’s a RESTful api for some business application, returning records of data.
- Sometimes the API returns a secure file path to something like a json or parquet file in a bucket that enables you to grab the data in bulk.
- Sometimes the API is something else (mongo, sql, other databases or applications) and will generally return records as JSON - the most common interchange format.


So here’s what you need to consider on extraction, to prevent the pipelines from breaking, and to keep them running smoothly.

Hardware limits
Network limits
Source api limits


How do we avoid hitting the hardware limit anf filling the memory?

***By Controling the max memory you use.***


We can control this memory used by streaming the data.

Streaming here refers to processing the data event by event or chunk by chunk instead of doing bulk operations.

To process data in a stream in python, we use ***generators***, which are functions that can return multiple times - by allowing multiple returns, the data can be released as it’s produced, as stream, instead of returning it all at once as a batch.


**Incremental Loading**

Incremental loading means that as we update our datasets with the new data, we would only load the new data, as opposed to making a full copy of a source’s data all over again and replacing the old version.

dlt currently supports 2 ways of loading incrementally:

***Append:***
    - We can use this for immutable or stateless events (data that doesn’t change), such as taxi rides - For example, every day there are new rides, and we could load the new ones only instead of the entire history.

    - We could also use this to load different versions of stateful data, for example for creating a “slowly changing dimension” table for auditing changes. For example, if we load a list of cars and their colors every day, and one day one car changes color, we need both sets of data to be able to discern that a change happened.


***Merge:***
    -  We can use this to update data that changes. For example, a taxi ride could have a payment status, which is originally “booked” but could later be changed into “paid”, “rejected” or “cancelled”

    