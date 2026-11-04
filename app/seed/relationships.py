from app.models.relationship import Relationship

RELATIONSHIPS = [
    {
        "source": "Kafka",
        "relationship": Relationship.STREAMS_TO,
        "target": "Spark"
    },
    {
        "source": "Airflow",
        "relationship": Relationship.ORCHESTRATES,
        "target": "Spark"
    }
]