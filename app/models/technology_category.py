from enum import StrEnum

class TechnologyCategory(StrEnum):
    STREAMING = "Streaming"
    PROCESSING = "Processing"
    ORCHESTRATION = "Orchestration"
    STORAGE = "Storage"
    DATABASE = "Database"
    DATA_WAREHOUSE = "Data Warehouse"
    LAKEHOUSE = "Lakehouse"
    MESSAGING = "Messaging"
    VISUALIZATION = "Visualization"
    ML = "Machine Learning"