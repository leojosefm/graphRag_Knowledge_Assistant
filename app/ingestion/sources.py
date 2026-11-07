from dataclasses import dataclass

@dataclass
class DocumentationSource:
    technology: str
    url: str
    scope_path: str = ""
    version: str = "latest"
    crawl_depth: int = 1


DOCUMENTATION_SOURCES = [
    DocumentationSource(
        technology="Spark",
        url="https://spark.apache.org/docs/latest/submitting-applications.html",
        scope_path="/docs/latest",
        ),

    DocumentationSource(
    technology="Spark",
    url="https://spark.apache.org/docs/latest/sql-programming-guide.html",
    scope_path="/docs/latest",

),

    DocumentationSource(
    technology="Airflow",
    url="https://airflow.apache.org/docs/apache-airflow-providers-apache-spark/stable/operators.html",
    scope_path="/docs/apache-airflow-providers-apache-spark",
),

    DocumentationSource(
    technology="dbt",
    url="https://docs.getdbt.com/docs/build/models",
    scope_path="/docs/build",

)

]