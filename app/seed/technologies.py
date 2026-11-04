from app.models.technology_category import TechnologyCategory

TECHNOLOGIES = [
    {
        "name": "Kafka",
        "category": TechnologyCategory.STREAMING,
        "description": "Distributed event streaming platform."
    },
    {
        "name": "Spark",
        "category": TechnologyCategory.PROCESSING,
        "description": "Distributed data processing engine."
    },
    {
        "name": "Airflow",
        "category": TechnologyCategory.ORCHESTRATION,
        "description": "Workflow orchestration platform."
    },
    {
        "name": "Iceberg",
        "category": TechnologyCategory.STORAGE,
        "description": "Open table format for huge analytic datasets."
    },
    {
        "name": "Snowflake",
        "category": TechnologyCategory.DATA_WAREHOUSE,
        "description": "Analytics data warehouse built for the cloud."
    },
    {
        "name": "Delta Lake",
        "category": TechnologyCategory.LAKEHOUSE,
        "description": "Open-source storage layer that brings reliability to data lakes."
    },
    {
        "name": "PostgreSQL",
        "category": TechnologyCategory.DATABASE,
        "description": "Open-source relational database management system."
    },
    {
        "name": "Databricks",
        "category": TechnologyCategory.LAKEHOUSE,
        "description": "Unified data and AI platform providing managed Apache Spark capabilities and supporting lakehouse architectures."
    }
]