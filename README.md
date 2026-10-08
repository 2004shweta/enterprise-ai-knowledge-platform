# Enterprise AI Knowledge Platform

A production-oriented Retrieval-Augmented Generation (RAG) application designed to provide grounded answers from a private knowledge base.

The project focuses on improving retrieval quality by combining **BM25 keyword search, dense vector retrieval, result fusion, and cross-encoder reranking** before sending context to the LLM.

> **Current status:** Actively being improved. The next focus is evaluating retrieval quality against a dedicated test set rather than relying only on subjective answer quality.

---

## 🔗 Links

- **GitHub:** https://github.com/2004shweta/enterprise-ai-knowledge-platform
- **Live API / Swagger:** http://3.107.235.158:8000/docs

---

## Why I Built This

My initial RAG implementation relied mainly on vector search.

While semantic search worked well for conceptually similar queries, it struggled with exact terms such as:

- Names
- IDs
- Error codes
- Technical identifiers
- Exact keywords

This led to an important lesson:

> **A good LLM cannot compensate for poor retrieval.**

Instead of immediately changing the LLM, I focused on improving the retrieval pipeline.

The current system combines lexical and semantic retrieval and then reranks the retrieved candidates before passing them to the LLM.

---

## Retrieval Pipeline

```text
                    User Query
                        │
                        ▼
                 Query Processing
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
        BM25 Keyword        Dense Vector Search
          Retrieval             PostgreSQL
                                + pgvector
              │                   │
              └─────────┬─────────┘
                        ▼
                 Result Fusion
                        │
                        ▼
              Cross-Encoder Reranker
                        │
                        ▼
              Relevant Context
                        │
                        ▼
                     LLM
                        │
                        ▼
                 Grounded Answer

Retrieval Components
1. BM25 Keyword Retrieval
Handles exact lexical matches and improves retrieval for queries containing identifiers, names, error codes, and specific terms.
2. Dense Vector Retrieval
Uses embeddings to retrieve semantically related content even when the exact wording differs.
3. Hybrid Retrieval
Combines keyword and semantic retrieval results to provide broader and more relevant candidate documents.
4. Cross-Encoder Reranking
Reranks retrieved candidates based on query-document relevance before the final context is passed to the LLM.
Tech Stack
Backend
- Python
- FastAPI
- LangGraph
- REST APIs
- Server-Sent Events (SSE)
AI / LLM
- Retrieval-Augmented Generation (RAG)
- OpenAI-compatible APIs
- LangGraph
- Embeddings
- BM25
- Cross-Encoder Reranking
Database
- PostgreSQL
- pgvector
- SQLAlchemy
- Alembic
Security & Reliability
- JWT Authentication
- Role / access-level based authorization
- Rate Limiting
- Query Caching
- Conversation History
- Grounding / retrieval checks
Infrastructure
- Docker
- Docker Compose
- AWS EC2
- GitHub Actions
Key Features
Hybrid Retrieval
Instead of relying exclusively on vector similarity, the system combines:
BM25 Keyword Search
        +
Dense Vector Search
        ↓
   Result Fusion
        ↓
Cross-Encoder Reranking

This helps address both semantic and exact-match retrieval problems.
JWT Authentication
Protected API endpoints use JWT-based authentication.
The application supports different access levels for controlling access to knowledge sources.
Query Caching
Frequently repeated queries can be served from cache to avoid unnecessary retrieval and LLM calls.
Rate Limiting
API requests are rate-limited to prevent excessive usage and provide basic protection against abuse.
Conversation History
The application maintains conversation context so users can continue multi-turn interactions.
SSE Streaming
Responses can be streamed progressively using Server-Sent Events instead of waiting for the complete LLM response.
Database Migrations
Alembic is used to manage PostgreSQL schema migrations.
Dockerized Deployment
The application and PostgreSQL/pgvector database are containerized for consistent development and deployment environments.
AWS Deployment
The FastAPI application is deployed on AWS EC2 with PostgreSQL/pgvector running as part of the deployment stack.
API Endpoints
The application exposes REST APIs for interacting with the knowledge platform.
Endpoint	Purpose
POST /ask	Ask a question and receive a grounded answer
GET /ask/stream	Stream an answer using SSE
POST /search	Search the knowledge base
POST /feedback	Submit response feedback


Additional endpoints are available through the Swagger documentation.
API Documentation
http://3.107.235.158:8000/docs
Local Development
1. Clone the repository
git clone https://github.com/2004shweta/enterprise-ai-knowledge-platform.git

cd enterprise-ai-knowledge-platform

2. Create a virtual environment
python -m venv .venv

Activate it:
Windows
.venv\Scripts\activate

Linux / macOS
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables
Create a .env file based on the project's configuration requirements.
Example:
APP_ENV=local

OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=2048

OPENAI_EMBEDDING_MODEL=openai/text-embedding-3-small

VECTOR_STORE_BACKEND=pgvector

POSTGRES_URL=postgresql://rag:password@localhost:5434/rag

EMBEDDING_DIMENSIONS=1536

CHUNK_SIZE=900
CHUNK_OVERLAP=150

Never commit API keys, JWT secrets, database passwords, or other credentials to GitHub.

PostgreSQL + pgvector
The application uses PostgreSQL with the pgvector extension for vector storage and similarity search.
Example Docker setup:
docker run -d \
  --name rag-pgvector \
  -e POSTGRES_USER=rag \
  -e POSTGRES_PASSWORD=rag \
  -e POSTGRES_DB=rag \
  -p 5434:5432 \
  pgvector/pgvector:pg16

Run database migrations:
alembic upgrade head

Run the Application
Start the FastAPI server:
uvicorn app.main:app --reload

The API will be available at:
http://localhost:8000

Swagger documentation:
http://localhost:8000/docs

Docker Deployment
Build and start the application:
docker compose up -d --build

Check running containers:
docker compose ps

View application logs:
docker compose logs app

AWS Deployment
The application is deployed using:
AWS EC2
   │
   ├── FastAPI Application
   │
   └── PostgreSQL + pgvector

The application is containerized using Docker and exposed through the FastAPI service.
Live API
http://3.107.235.158:8000/docs
The live endpoint depends on the EC2 instance being running and the configured network/security-group rules.

Retrieval Evaluation
One of the next development steps is to evaluate the retrieval pipeline quantitatively.
The planned evaluation compares:
Dense Retrieval
      vs
BM25
      vs
Hybrid Retrieval
      vs
Hybrid + Cross-Encoder Reranking

Metrics under consideration include:
- Recall@K
- Precision@K
- Mean Reciprocal Rank (MRR)
- Retrieval relevance
The goal is to measure whether each retrieval improvement actually improves the quality of retrieved context.
No performance improvement numbers are claimed until they are measured against a defined evaluation dataset.

Project Structure
enterprise-ai-knowledge-platform/
│
├── app/
│   ├── api/
│   ├── graph/
│   ├── retrieval/
│   ├── services/
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── migrations/
│
├── tests/
│
├── Dockerfile
├── docker-compose.pgvector.yml
├── requirements.txt
├── alembic.ini
└── README.md

Engineering Focus
This project focuses on practical backend and AI engineering concepts:
- Retrieval system design
- Hybrid search
- Vector databases
- Semantic search
- Information retrieval
- Reranking
- LLM integration
- API design
- Authentication
- Rate limiting
- Caching
- Streaming APIs
- PostgreSQL
- Docker
- Cloud deployment
- AI system evaluation
Current Development
The project is still actively being improved.
The immediate focus is retrieval evaluation:
1. Build a small representative evaluation dataset.
2. Run the same queries through different retrieval strategies.
3. Measure retrieval relevance.
4. Compare hybrid retrieval against dense-only retrieval.
5. Measure the impact of cross-encoder reranking.
6. Use the results to identify further retrieval improvements.
The goal is to make the system measurably better, rather than adding features without evaluating their impact.
