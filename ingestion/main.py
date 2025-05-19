import json
import os

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from ingestion import Ingestion

def main():
    with open("config.json") as f:
        config = json.load(f)

    #print(config)    

    spark = SparkSession.builder.appName("SocialMediaETL").getOrCreate()

    # Convert schemas from config JSON
    schema_posts = StructType.fromJson(config["schema_posts"])
    schema_events = StructType.fromJson(config["schema_events"])

    etl = Ingestion(spark, config["output_path"], config["log_file"])
    etl.ingest_posts(config["input_posts"], schema_posts)
    etl.ingest_events(config["input_events"], schema_events)

    spark.stop()

if __name__ == "__main__":
    main()