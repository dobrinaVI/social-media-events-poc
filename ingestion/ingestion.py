import traceback
import logging
import json
import os

from pyspark.sql import SparkSession
from datetime import datetime

class Ingestion():
    def __init__(self, spark: SparkSession, output_path:str, log_file):
        self.spark = spark
        self.output_path = output_path
        self.logger=Logger(log_file)

        os.makedirs(output_path, exist_ok=True)

    def ingest_posts(self, input_posts, schema_posts):
        try:
            df = self.spark.read.csv(input_posts, sep="\t", schema=schema_posts)
            df.write.mode("append").parquet(os.path.join(self.output_path, "posts"))
            self.logger.log("INFO", "Ingested posts: COMPLETED")
        except Exception as e:
            self.logger.log("ERROR", f"Ingested posts: FAILED - {e}")
            traceback.print_exc()

    def ingest_events(self, input_events, schema_events):
        try:
            df = self.spark.read.csv(input_events, sep="\t", schema=schema_events)
            df.write.mode("append").parquet(os.path.join(self.output_path, "events"))
            self.logger.log("INFO", "Ingested events: COMPLETED")
        except Exception as e:
            self.logger.log("ERROR", f"Ingested events: FAILED - {e}")
            traceback.print_exc()

class Logger():
    def __init__(self, log_file: str, level=logging.INFO, name: str="etl_logger"):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        if not any(isinstance(h, logging.FileHandler) for h in self.logger.handlers):
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(self._json_formatter())
            self.logger.addHandler(file_handler)

    def _json_formatter(self):
        formatter = logging.Formatter()
        formatter.format = self._format_record
        return formatter

    def _format_record(self, record):
        log_msg = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }
        return json.dumps(log_msg)

    def log(self, level, message):
        if level.lower() == 'info':
            self.logger.info(message)
        elif level.lower() == 'error':
            self.logger.error(message)
        else:
            # Accept custom numeric logging levels
            self.logger.log(level, message)            