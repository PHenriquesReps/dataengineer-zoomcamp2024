### Data Processing

Different types of processing data:
- Batch 
- Streaming

Batch - Porcess the data in chunks. 

Advantages
- Easy to Manage
- Retry
- Scale

Disavantages
- Delay on getting the data to dowstream


### Introduction to Spark






***Settings:***

- On the GCP VM we need to install java:
We get the jdk 11.0.2 version. 
Then we need to create 2 variables on the VM:

```bash 
export JAVA_HOME="${HOME}/spark/jdk-11.0.2" 
```

```bash 
export PATH="${JAVA_HOME}/bin:${PATH}"
```

- We do the same thing for Spark:
Spark version 3.4.2

```bash 
export SPARK_HOME="${HOME}/spark/spark-3.4.2-bin-hadoop3"
```

```bash 
export PATH="${SPARK_HOME}/bin:${PATH}"
```

we have to add the python variables too:

```bash 
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
```

```bash 
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH"
```


Then we add all of this variables to the .bashrc file to be executed every time we login on the VM.



***Copy data from the VM to the GCS***
We need to have a bucker created on GCS.

After that we use the gsutil command.

```bash
gsutil -m cp -r <path to the folder/file we want to copy> <gcs destination path (exp.gs://<bucket_name>)>
```

To connect the spark locally to the gcs we need to change some configurations and download the gcs-hadoop jar connector.


```py
import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import types
import pandas as pd
```

Create the Spark context:

```py
credentials_location = '<Key to access to gcp>'

conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "./lib/gcs-connector-hadoop3-latest.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)
```

Set variables:
```py
sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")
```

Create Spark Session:

```py
spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()
```

*** How to Create a local Cluster? ***

1- Using the SparkSession on a notebook.

local[*] -> create a local cluster using all the available storage and cpu

```py
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()
```

2- Running this command on our Spark Home location.

```bash
./sbin/start-master.sh
```

Then we go to localhost on port 8080 to see the master node that we have created, copy the ***URL*** and paste it on the spark session created.

```py
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("<URL>") \
    .appName('test') \
    .getOrCreate()
```

At this point we only started the clsuter, we have 0 workers.
We need to add/start executors, for that we need to run this command:

```bash
./sbin/start-worker.sh <Master_URL>
```


Turn the jupyter Notebook inot a Python Script

Terminal -> 

```bash 
jupyter nbconvert --to=script <notebook_name>
```

However, if we specifying the Master URL on the sparkSession creation is not a standar practice, we should use the spark-submit.

### Spark-Submit

In order to run a spark application you need to deploy it on a cluster. There are different ways to submit your application on a cluster but the most common is to use the spark-submit.
spark-submit` is a command-line tool provided by Apache Spark for submitting Spark applications to a cluster.

The spark-submit tool take a Python file as input along with the application’s configuration options and submits the application to the cluster. The configuration options can be used to set various parameters for the application, such as the number of executor cores, the amount of memory allocated to each executor, and the number of executors.

```bash
spark-submit [cluster_options] <file.py> [application_arguments]
```

Example:
```bash
URL="spark://de-zoomcamp.europe-west1-b.c.dataenginner-zoomcamp.internal:7077"

spark-submit \
    --master="$URL" \
    07_using_spark_submit.py \
    --input_green=/home/pedroh/dataengineer-zoomcamp2024/week6/code/data/pq/green/2021/*/ \
    --input_yellow=/home/pedroh/dataengineer-zoomcamp2024/week6/code/data/pq/yellow/2021/*/ \
    --output=/home/pedroh/dataengineer-zoomcamp2024/week6/code/data/report-2021
```

On this example we just add the master URL to the master configuration, this session take all the available resources.


When we finish we need to stop the Cluster from running we do the inverse process, stop the wrokers and the master using these commands:

Stop the worker:
```bash
./sbin/stop-worker.sh
```

Stop the Master:
```bash
./sbin/stop-master.sh
```


### Setting up a DatProc Cluster on GCP

We create a cluster in the GCP UI. 

After that we can submit a job using the UI, submiting the job directly their, our using other ways to do it (https://cloud.google.com/dataproc/docs/guides/submit-job#dataproc-submit-job-gcloud), like using the gcloud command.

```bash
gcloud dataproc jobs submit <job-command> \
    --cluster=<cluster-name> \
    --region=<region> \
    other dataproc-flags \
    -- job-args
```


Example:
```bash
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=europe-west1 \
    gs://taxi-data-ph/code/07_using_spark_submit.py \
    -- \
        --input_green=gs://taxi-data-ph/pq/green/2021/*/ \
        --input_yellow=gs://taxi-data-ph/pq/yellow/2021/*/ \
        --output=gs://taxi-data-ph/report-2021
```


### Spark to BigQuery

Write directly from Spark to BigQuery. We will use this BigQuery connector to Spark (https://cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example#pyspark).

On the Python file we need to add a temp bucket and the save statement to BigQuery:

Temp Bucket Config:
```py
# Use the Cloud Storage bucket for temporary BigQuery export data used
# by the connector.
bucket = <"bucket_name">
spark.conf.set('temporaryGcsBucket', bucket)
```


Save Statement to BigQuery:
```py
# Save the data to BigQuery
<df_name>.write.format('bigquery') \
  .option('table', <output>) \
  .save()
```

Then we can run it using the gcloud command, like did previously, we just need to add a few extra settings and the jars to connect spark to BigQuery.

```bash
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=europe-west1 \
    gs://taxi-data-ph/code/07_using_spark_submit_to_BigQuery.py \
    -- \
        --input_green=gs://taxi-data-ph/pq/green/2020/*/ \
        --input_yellow=gs://taxi-data-ph/pq/yellow/2020/*/ \
        --output=taxi_tripsdata.reposts-2020
```
