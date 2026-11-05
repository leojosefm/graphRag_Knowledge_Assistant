from dataclasses import dataclass

@dataclass
class DocumentationSource:
    technology: str
    url: str
    version: str = "latest"
    crawl_depth: int = 1


DOCUMENTATION_SOURCES = [
    DocumentationSource(
        technology="Apache Spark",
        url="https://spark.apache.org/docs/latest/submitting-applications.html",
    
    ),

    DocumentationSource(
    technology="Spark",
    url="https://spark.apache.org/docs/latest/sql-programming-guide.html",

),

    DocumentationSource(
    technology="Airflow",
    url="https://airflow.apache.org/docs/apache-airflow-providers-apache-spark/stable/operators.html",

),

    DocumentationSource(
    technology="dbt",
    url="https://docs.getdbt.com/docs/build/models",

)

]