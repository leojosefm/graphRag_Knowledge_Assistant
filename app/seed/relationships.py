from app.models.relationship import Relationship

RELATIONSHIPS = [
    # Kafka and Spark
    {
        "source": "Kafka",
        "relationship": Relationship.STREAMS_TO,
        "target": "Spark"
    },

    # Airflow integrations
    {
        "source": "Airflow",
        "relationship": Relationship.ORCHESTRATES,
        "target": "Spark"
    },
    {
        "source": "Airflow",
        "relationship": Relationship.CONNECTS_TO,
        "target": "Snowflake"
    },
    {
        "source": "Airflow",
        "relationship": Relationship.CONNECTS_TO,
        "target": "Databricks"
    },

    # Spark and Iceberg
    {
        "source": "Spark",
        "relationship": Relationship.READS_FROM,
        "target": "Iceberg"
    },
    {
        "source": "Spark",
        "relationship": Relationship.WRITES_TO,
        "target": "Iceberg"
    },

    # Snowflake and Iceberg
    {
        "source": "Snowflake",
        "relationship": Relationship.READS_FROM,
        "target": "Iceberg"
    },
    {
        "source": "Snowflake",
        "relationship": Relationship.WRITES_TO,
        "target": "Iceberg"
    },

    # Databricks and Spark
    {
        "source": "Databricks",
        "relationship": Relationship.PROVIDES,
        "target": "Spark"
    },

    # Databricks and Delta Lake
    {
        "source": "Databricks",
        "relationship": Relationship.SUPPORTS,
        "target": "Delta Lake"
    },
    {
        "source": "Databricks",
        "relationship": Relationship.READS_FROM,
        "target": "Delta Lake"
    },
    {
        "source": "Databricks",
        "relationship": Relationship.WRITES_TO,
        "target": "Delta Lake"
    },

    # Databricks and Iceberg
    {
        "source": "Databricks",
        "relationship": Relationship.SUPPORTS,
        "target": "Iceberg"
    },
    {
        "source": "Databricks",
        "relationship": Relationship.READS_FROM,
        "target": "Iceberg"
    },
    {
        "source": "Databricks",
        "relationship": Relationship.WRITES_TO,
        "target": "Iceberg"
    }
]