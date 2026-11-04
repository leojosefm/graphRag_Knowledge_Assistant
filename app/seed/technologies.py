from models.technology_category import TechnologyCategory

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
    }
]