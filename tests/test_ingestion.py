import pytest
import logging

from unittest.mock import MagicMock
from ingestion.ingestion import Ingestion, Logger

@pytest.fixture
def spark_mock():
    return MagicMock()

@pytest.fixture
def ingestion(spark_mock, tmp_path):
    log_file = tmp_path / "log.txt"
    print(log_file)
    return Ingestion(spark_mock, str(tmp_path), str(log_file))

def test_ingest_posts_success(ingestion, spark_mock):
    df_mock = MagicMock()
    spark_mock.read.csv.return_value = df_mock

    ingestion.ingest_posts("input/posts.txt", schema_posts={})
    df_mock.write.mode.return_value.parquet.assert_called_once_with(f"{ingestion.output_path}/posts")

def test_ingest_events_success(ingestion, spark_mock):
    df_mock = MagicMock()
    spark_mock.read.csv.return_value = df_mock

    ingestion.ingest_events("input/events.txt", schema_events={})
    df_mock.write.mode.return_value.parquet.assert_called_once_with(f"{ingestion.output_path}/events")

def test_logger_logs_to_file(tmp_path):
    log_file = tmp_path / "log.txt"
    print(log_file)
    logger = Logger(str(log_file), name="test_logger")
    logger.log("INFO", "Test message")

    for handler in logger.logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.flush()

    content = log_file.read_text()
    assert "Test message" in content