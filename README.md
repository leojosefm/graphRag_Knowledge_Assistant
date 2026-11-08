# Mini GraphRAG Knowledge Assistant


**Status: In Progress**

This is a learning project exploring knowledge graphs, vector search and LLM-powered agents to build a technical knowledge assistant.

The initial focus is on public documentation from the data engineering ecosystem, including Apache Airflow, Apache Kafka, Apache Spark and dbt.

The goal is to build a small, containerised application that allows users to explore technology relationships, retrieve relevant documentation and ask technical questions using natural language.

---

## Project Objectives

- Build a knowledge graph using Neo4j to represent technologies and their relationships.
- Explore graph-based retrieval alongside traditional vector search.
- Implement document ingestion, chunking and embedding generation.
- Develop a lightweight AI agent capable of using bounded retrieval tools.
- Build an interactive Streamlit application.
- Compare Vector RAG, Graph RAG and Hybrid GraphRAG.
- Keep LLM usage and token consumption measurable and controlled.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.12 |
| Graph database | Neo4j |
| Application UI | Streamlit |
| Graph visualisation | PyVis |
| Embeddings | Sentence Transformers (planned) |
| LLM | Hosted LLM or Ollama (TBD) |
| Containerisation | Docker / Docker Compose |
| Testing | pytest (planned) |

---

## Development Progress

### Phase 1 – Infrastructure Setup

**Status: Completed**

- Docker Compose environment configured.
- Neo4j Community Edition deployed.
- Streamlit application container configured.
- Application-to-Neo4j connectivity established.
- Environment variables and database credentials configured.

### Phase 2 – Knowledge Graph Foundation

**Status: Completed**

- Defined initial graph node labels and relationship types.
- Implemented Neo4j schema constraints.
- Created technology seed data.
- Implemented initial graph population using `MERGE`.
- Established a reusable graph repository layer.

### Phase 3 – Graph Repository

**Status: Implemented**

Implemented repository operations for:

- Creating nodes.
- Retrieving individual nodes.
- Retrieving all nodes.
- Updating nodes.
- Deleting nodes.
- Creating relationships.
- Retrieving neighbouring nodes.
- Retrieving relationships.
- Updating relationships.
- Deleting relationships.

### Phase 4 – Streamlit Graph Management UI

**Status: Complete**

Implemented:

- Technologies page for adding and deleting technologies.
- Relationships page for creating, editing and deleting relationships.
- Display of available technologies and relationships.

Further testing and refinement of relationship management is ongoing.

### Phase 5 – Graph Explorer

**Status: Implemented**

Implemented:

- Interactive graph visualisation using PyVis.
- Display technology nodes and directed relationships.
- Zooming and node repositioning.
- Interactive exploration of graph relationships.

Future enhancements:

- Filtering by technology category.
- Display node metadata.
- Search and highlight technologies.
### Phase 6 – Document Ingestion

**Status: Completed**

Implemented:

- Configurable documentation sources.
- Recursive documentation crawler.
- HTML parsing and content extraction.
- Document cleaning.
- Fixed-size document chunking.
- Neo4j document storage.
- Chunk storage.
- Technology → Document relationships.
- Document → Chunk relationships.

Currently working on:

- Better crawl filtering.
- Version-aware documentation.
- Incremental ingestion.
- Metadata enrichment.

### Phase 7 – Retrieval and GraphRAG

**Status: In Progress**

Implemented:

- Query embedding generation
- Neo4j vector similarity search
- Top-K semantic retrieval
- HNSW vector search

Currently working on:

- Graph-aware retrieval
- Hybrid graph + vector retrieval
- Source attribution
- Retrieval ranking
- Graph traversal queries

### Phase 8 – AI Agent

**Status: Planned**

- Implement bounded agent tools.
- Add question routing.
- Enable the agent to select appropriate retrieval tools.
- Generate answers using retrieved documentation and graph context.
- Track token consumption, latency and tool execution.

### Phase 9 – Evaluation

**Status: Planned**

Compare three retrieval approaches:

1. Vector-only RAG.
2. Graph-only retrieval.
3. Hybrid GraphRAG.

Evaluate answer correctness, retrieval relevance, citation support, latency, token usage and unsupported claims.

---

## Current Project Structure

```text
datastack-ai/
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
├── README.md
└── app/
    ├── streamlit_app.py
    ├── neo4j_connection.py
    ├── pages/
    │   ├── technologies.py
    │   ├── relationships.py
    │   └── graph_explorer.py
    ├── repositories/
    │   └── graph_repository.py
    ├── models/
    │   ├── labels.py
    │   ├── relationship.py
    │   └── technology_category.py
    ├── database/
    │   └── schema_manager.py
    └── seed/
        ├── technologies.py
        ├── relationships.py
        └── seed_graph.py
```

*Note: The Graph Explorer page is currently being developed. The structure will evolve as document ingestion and retrieval components are added.*

---

## Running the Application

### Prerequisites

- Docker Desktop
- Docker Compose
- Git

### Configuration

Create a `.env` file in the project root and configure the Neo4j password.

```env
NEO4J_PASSWORD=your_password
```

### Start the application

```bash
docker compose up --build -d
```

### Access the applications

| Application | URL |
|---|---|
| Streamlit | http://localhost:8501 |
| Neo4j Browser | http://localhost:7474 |


## Seed the Knowledge Graph

```bash
docker compose exec app python -m app.seed.seed_graph
```

## Ingest Documentation

```bash
docker compose exec app python -m app.ingestion.pipeline
```

## Test Vector Retrieval

```bash
docker compose exec app python -m app.retrieval.test_scripts.test_vector_retriever
```
## Test Semantic Retrieval

```bash
docker compose exec app python -m app.retrieval.test_scripts.test_hybrid_retriever
```



---

## Initial Documentation Sources

The knowledge assistant will initially focus on publicly available documentation:

- [Apache Airflow](https://airflow.apache.org/docs/)
- [Apache Kafka](https://kafka.apache.org/documentation/)
- [Apache Spark](https://spark.apache.org/docs/latest/)
- [dbt](https://docs.getdbt.com/)

Only a small, version-pinned documentation subset will be used for the initial prototype.

---

## Project Scope and Design Principles

- Use public documentation only.
- Keep the prototype small and reproducible.
- Use Neo4j for both graph storage and vector retrieval.
- Prefer local embeddings to minimise external API usage.
- Avoid unrestricted LLM-generated Cypher queries.
- Use predefined, parameterised graph queries.
- Keep agent execution bounded and measurable.
- Preserve source references to support grounded answers.

---
