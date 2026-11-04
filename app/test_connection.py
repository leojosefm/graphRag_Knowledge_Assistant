from app.database import Neo4jConnection

def main():
    db = Neo4jConnection()

    try:
        db.verify_connection()
        print("Successfully connected to Neo4j!")

        result = db.execute_query(
            "RETURN 'Hello from DataStack AI' AS message"
        )

        print(result)

    finally:
        db.close()

if __name__ == "__main__":
    main()
