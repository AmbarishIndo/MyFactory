import os
import uuid
from typing import Dict, List, Optional, Any
import chromadb

# Persistent ChromaDB storage directory
CHROMA_DATA_DIR = os.getenv("CHROMA_DATA_DIR", "./chroma_db")

# Initialize ChromaDB persistent client
_client = None
_collection = None


def get_chroma_client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DATA_DIR)
    return _client


def get_memory_collection():
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(name="agent_memory")
    return _collection


def add_agent_memory(
    agent_name: str,
    action_executed: str,
    kpi_metric: str,
    roi_score: float,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Embeds action_executed and stores it in ChromaDB with roi_score, agent_name, and kpi_metric in metadata.
    """
    collection = get_memory_collection()
    doc_id = str(uuid.uuid4())

    meta = {
        "agent_name": agent_name,
        "kpi_metric": kpi_metric,
        "roi_score": float(roi_score),
    }
    if metadata:
        meta.update(metadata)

    collection.add(
        documents=[action_executed],
        metadatas=[meta],
        ids=[doc_id],
    )
    return doc_id


def query_agent_memory(
    task_query: str,
    n_results: int = 10,
) -> List[Dict[str, Any]]:
    """
    Queries ChromaDB for the closest semantic matches to task_query.
    Returns a list of dicts containing document, metadata, and distance/id.
    """
    collection = get_memory_collection()

    # Check if collection is empty
    if collection.count() == 0:
        return []

    count = min(collection.count(), n_results)
    results = collection.query(
        query_texts=[task_query],
        n_results=count,
    )

    matches = []
    if results and results.get("ids") and len(results["ids"]) > 0:
        ids = results["ids"][0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0] if results.get("distances") else [None] * len(ids)

        for doc_id, doc, meta, dist in zip(ids, documents, metadatas, distances):
            matches.append({
                "id": doc_id,
                "action_executed": doc,
                "agent_name": meta.get("agent_name"),
                "kpi_metric": meta.get("kpi_metric"),
                "roi_score": meta.get("roi_score"),
                "metadata": meta,
                "distance": dist,
            })

    return matches
