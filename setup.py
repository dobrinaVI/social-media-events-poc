from setuptools import setup, find_packages

setup(
    name="social-media-events-poc",
    version="1.0.0",
    description="Social Media Events POC",
    author="Dobrina Ivanova",
    author_email="dobrina.v.ivanova@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pyspark==3.5.3",
        "requests==2.26.0",
        "ruff==0.7.3",
        "pytest-pythonpath==0.7.4",
        "duckdb==1.2.2", 
        "dbt-core==1.9.4",
        "dbt-duckdb==1.9.3",
        'pandas==2.2.3',
        'pyarrow==20.0.0',
    ],
    entry_points={
        "console_scripts": [
            "ingestion=ingestion.main:main"
        ]
    },
    python_requires=">=3.10",
)