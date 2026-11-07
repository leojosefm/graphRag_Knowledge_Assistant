from app.database.schema_manager import SchemaManager

schema = SchemaManager()

schema.create_vector_index()
schema.close()

