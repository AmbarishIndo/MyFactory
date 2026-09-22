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


def test_generate_vlog_script_endpoint():
    payload = {
        "topic": "72 Hours in Tokyo",
        "platform": "YouTube Shorts",
    }
    response = client.post("/api/media/vlog", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "title" in data
    assert "hook" in data
    assert data["platform"] == "YouTube Shorts"
    assert "72 Hours in Tokyo" in data["title"]
    assert isinstance(data["scenes"], list)
    assert len(data["scenes"]) > 0

    scene = data["scenes"][0]
    assert "timestamp" in scene
    assert "video_prompt" in scene
    assert "audio_cue" in scene


def test_generate_recipe_endpoint():
    payload = {
        "dish_name": "Gnocchi",
        "diet_type": "Vegan Gochujang",
    }
    response = client.post("/api/media/recipe", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "title" in data
    assert "Vegan Gochujang Gnocchi" in data["title"]
    assert isinstance(data["ingredients"], list)
    assert len(data["ingredients"]) > 0
    assert isinstance(data["instructions"], list)
    assert len(data["instructions"]) > 0
    assert "cinematic_image_prompt" in data
    assert "Hasselblad" in data["cinematic_image_prompt"] or "Gnocchi" in data["cinematic_image_prompt"]


def test_agent_sigma_memory_logging():
    # Calling endpoints should log actions into ChromaDB memory bank
    vlog_payload = {
        "topic": "Cyberpunk Neo-Seoul",
        "platform": "TikTok",
    }
    client.post("/api/media/vlog", json=vlog_payload)

    recipe_payload = {
        "dish_name": "Ramen",
        "diet_type": "Keto",
    }
    client.post("/api/media/recipe", json=recipe_payload)

    # Query memory bank to check if Agent Sigma actions were recorded
    retrieve_res = client.get("/api/memory/retrieve", params={"task_query": "Cyberpunk Neo-Seoul"})
    assert retrieve_res.status_code == 200
    retrieved_data = retrieve_res.json()

    # Check matches for Agent Sigma
    matches = retrieved_data.get("all_matches", [])
    agent_sigma_matches = [m for m in matches if m.get("agent_name") == "Agent Sigma"]
    assert len(agent_sigma_matches) > 0

    # Ensure kpi_metric and json output are present
    kpi_metrics = [m.get("kpi_metric") for m in agent_sigma_matches]
    assert "viewer_retention" in kpi_metrics or "affiliate_clicks" in kpi_metrics
