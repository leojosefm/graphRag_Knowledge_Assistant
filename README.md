# DataStack AI

DataStack AI is a hands-on learning project that combines modern data engineering and AI technologies into a single application.

The goal is to understand how technologies such as Graph Databases, Vector Search, Knowledge Graphs, AI Agents and Retrieval Augmented Generation (RAG) work together in a real-world system.

This project is intentionally built from scratch with a production-style architecture.

---

# Tech Stack

- Python 3.11+
- Docker & Docker Compose
- Neo4j Graph Database
- Streamlit
- OpenAI
- Vector Search (Coming Soon)
- AI Agents (Coming Soon)

---

# Project Roadmap

## Phase 1 - Knowledge Graph

- [x] Docker setup
- [x] Neo4j
- [x] Repository Pattern
- [x] Seed Graph
- [ ] Streamlit UI

---

## Phase 2 - Document Processing

- [ ] PDF Upload
- [ ] Document Parsing
- [ ] Text Chunking
- [ ] Store Documents in Neo4j

---

## Phase 3 - Vector Search

- [ ] Generate Embeddings
- [ ] Create Vector Index
- [ ] Semantic Search

---

## Phase 4 - GraphRAG

- [ ] Combine Graph Search with Vector Search
- [ ] Context Retrieval
- [ ] LLM Integration

---

## Phase 5 - AI Agent

- [ ] AI Assistant
- [ ] Technology Recommendations
- [ ] Knowledge Graph Exploration

---

# Project Structure

```
datastack-ai/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
│
├── app/
│   ├── streamlit_app.py
│   ├── neo4j_connection.py
│   ├── test_connection.py
│   │
│   ├── repositories/
│   │      └── graph_repository.py
│   │
│   ├── models/
│   │      ├── labels.py
│   │      ├── relationship.py
│   │      └── technology_category.py
│   │
│   └── seed/
│          ├── technologies.py
│          ├── relationships.py
│          └── seed_graph.py
│
└── README.md
```

---

# Architecture

```
                Streamlit
                     │
                     ▼
             GraphRepository
                     │
                     ▼
            Neo4jConnection
                     │
                     ▼
                 Neo4j
```

Each layer has a single responsibility.

- Streamlit → User Interface
- Repository → Database Operations
- Connection → Neo4j Driver
- Neo4j → Graph Database

---

# Getting Started

## Clone Repository

```bash
git clone <repository-url>

cd datastack-ai
```

---

## Create Environment File

Create a `.env` file.

```text
NEO4J_URI=bolt://neo4j:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=datastack
```

---

## Build Docker Containers

```bash
docker compose up --build -d
```

---

## Verify Containers

```bash
docker compose ps
```

Expected:

```
neo4j      healthy

app        running
```

---

# Neo4j Browser

Open

```
http://localhost:7474
```

Login

Username

```
neo4j
```

Password

```
password
```

(or whatever you configured in `.env`)

---

# Test Neo4j Connection

```
docker compose exec app python -m app.test_connection
```

Expected output

```
Successfully connected to Neo4j
```

---

# Seed the Knowledge Graph

```
docker compose exec app python -m app.seed.seed_graph
```

This creates:

- Technology Nodes
- Relationships between technologies

---

# Verify Seed Data

Open Neo4j Browser.

Run

```cypher
MATCH (n)
RETURN n
```

To view relationships

```cypher
MATCH (n)-[r]->(m)
RETURN *
```

---

# Repository Pattern

The application follows the Repository Pattern.

Instead of executing Cypher directly throughout the application,

```
Streamlit

↓

GraphRepository

↓

Neo4j
```

All graph operations are centralized inside

```
graph_repository.py
```

Examples:

```python
repo.create_node(...)

repo.get_node(...)

repo.create_relationship(...)

repo.get_neighbors(...)
```

---

# Why Repository Pattern?

Benefits

- Single place for all Cypher queries
- Easier testing
- Cleaner architecture
- Separation of concerns
- Easily reusable by Streamlit and AI Agents

---

# Current Knowledge Graph

Technology Nodes contain

```
Name

Category

Description
```

Relationships currently include

```
STREAMS_TO

READS_FROM

WRITES_TO

ORCHESTRATES

TRANSFORMS

DEPENDS_ON
```

---

# Next Steps

The next milestone is to ingest real technical documentation.

The pipeline will be

```
PDF

↓

Chunking

↓

Embeddings

↓

Vector Index

↓

Neo4j Knowledge Graph

↓

GraphRAG

↓

AI Agent
```

---

# Learning Objectives

This project is designed to provide hands-on experience with:

- Graph Databases
- Cypher Query Language
- Repository Pattern
- Docker
- Vector Databases
- Embeddings
- Semantic Search
- Retrieval Augmented Generation (RAG)
- GraphRAG
- AI Agents
- Production-style Python project architecture

---

# License

MIT