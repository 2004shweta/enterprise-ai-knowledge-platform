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
