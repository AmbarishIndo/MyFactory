import os
import tempfile
import pytest
from fastapi.testclient import TestClient

# Set temporary directory for ChromaDB before importing app
temp_dir = tempfile.mkdtemp()
os.environ["CHROMA_DATA_DIR"] = temp_dir

from backend.services import chroma_service

@pytest.fixture(autouse=True)
def reset_chroma_db(monkeypatch):
    # Reset ChromaDB global state so each test starts with an isolated/clean collection
    new_dir = tempfile.mkdtemp()
    monkeypatch.setattr(chroma_service, "_client", None)
    monkeypatch.setattr(chroma_service, "_collection", None)
    monkeypatch.setenv("CHROMA_DATA_DIR", new_dir)
    yield

from backend.main import app

client = TestClient(app)


def test_get_memory_logs_existing_endpoint():
    response = client.get("/api/memory/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_retrieve_empty_memory_bank():
    response = client.get("/api/memory/retrieve", params={"task_query": "highest converting tech thumbnail"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "highest converting tech thumbnail"
    assert data["best_strategy"] is None
    assert data["all_matches"] == []
    assert "No memory logs found" in data["message"]


def test_log_and_retrieve_agent_memory():
    # Log action 1
    payload1 = {
        "agent_name": "Agent Theta",
        "action_executed": "Created tech thumbnail with bold yellow title and high contrast background.",
        "kpi_metric": "CTR",
        "roi_score": 4.2,
    }
    log_res1 = client.post("/api/memory/log", json=payload1)
    assert log_res1.status_code == 200
    data1 = log_res1.json()
    assert data1["status"] == "success"
    assert "id" in data1

    # Log action 2 (higher ROI)
    payload2 = {
        "agent_name": "Agent Theta",
        "action_executed": "Created tech thumbnail with minimalist design and neon green accent.",
        "kpi_metric": "CTR",
        "roi_score": 8.9,
    }
    log_res2 = client.post("/api/memory/log", json=payload2)
    assert log_res2.status_code == 200

    # Retrieve memories for query
    retrieve_res = client.get("/api/memory/retrieve", params={"task_query": "highest converting tech thumbnail"})
    assert retrieve_res.status_code == 200
    retrieved_data = retrieve_res.json()
    assert retrieved_data["query"] == "highest converting tech thumbnail"
    assert retrieved_data["best_strategy"] is not None
    # Best strategy should have highest ROI score (8.9)
    assert retrieved_data["best_strategy"]["roi_score"] == 8.9
    assert "minimalist design" in retrieved_data["best_strategy"]["action_executed"]
    assert len(retrieved_data["all_matches"]) == 2
