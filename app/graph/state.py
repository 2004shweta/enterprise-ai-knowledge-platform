from typing import TypedDict

from app.retrieval.models import AccessFilter, SearchMode, SearchResult


class RagState(TypedDict):
    question: str
    active_question: str
    top_k: int
    search_mode: SearchMode
    access_filter: AccessFilter | None
    conversation_history: list[dict]
    preloaded_matches: list | None
    attempts: int
    results: list[SearchResult]
    answer: str
    sources: list[dict]
    needs_rewrite: bool
    grounded: bool
    workflow_steps: list[str]

 