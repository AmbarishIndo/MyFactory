import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Set temporary directory for ChromaDB before importing app
temp_dir = tempfile.mkdtemp()
os.environ["CHROMA_DATA_DIR"] = temp_dir

from backend.services import chroma_service

@pytest.fixture(autouse=True)
def reset_chroma_db(monkeypatch):
    new_dir = tempfile.mkdtemp()
    monkeypatch.setattr(chroma_service, "_client", None)
    monkeypatch.setattr(chroma_service, "_collection", None)
    monkeypatch.setenv("CHROMA_DATA_DIR", new_dir)
    yield


from backend.main import app
from backend.services.broadcast_service import send_telegram_alert, publish_wordpress_post

client = TestClient(app)


def test_send_telegram_alert_success():
    with patch("backend.services.broadcast_service.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        res = send_telegram_alert("token123", "chat456", "Test alert")
        assert res is True
        mock_post.assert_called_once_with(
            "https://api.telegram.org/bottoken123/sendMessage",
            json={"chat_id": "chat456", "text": "Test alert"},
            timeout=10,
        )


def test_send_telegram_alert_failure():
    with patch("backend.services.broadcast_service.requests.post") as mock_post:
        mock_post.side_effect = Exception("Connection error")

        res = send_telegram_alert("token123", "chat456", "Test alert")
        assert res is False


def test_publish_wordpress_post_success():
    with patch("backend.services.broadcast_service.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        res = publish_wordpress_post(
            "https://mywp.com",
            "user",
            "pass",
            "Title",
            "<p>Content</p>",
        )
        assert res is True
        mock_post.assert_called_once_with(
            "https://mywp.com/wp-json/wp/v2/posts",
            json={"title": "Title", "content": "<p>Content</p>", "status": "publish"},
            auth=("user", "pass"),
            timeout=10,
        )


def test_publish_wordpress_post_failure():
    with patch("backend.services.broadcast_service.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.text = "Server Error"
        mock_post.return_value = mock_response

        res = publish_wordpress_post(
            "https://mywp.com",
            "user",
            "pass",
            "Title",
            "<p>Content</p>",
        )
        assert res is False


def test_alpha_status_endpoint():
    with TestClient(app) as client_ctx:
        response = client_ctx.get("/api/alpha/status")
        assert response.status_code == 200
        data = response.json()
        assert data["running"] is True
        assert data["status"] == "online"
        assert isinstance(data["jobs"], list)
        job_ids = [j["id"] for j in data["jobs"]]
        assert "daily_quant_run" in job_ids
        assert "daily_media_run" in job_ids


def test_alpha_trigger_quant_run_endpoint():
    with patch("backend.services.orchestrator_service.fetch_market_data") as mock_fetch, \
         patch("backend.services.orchestrator_service.calculate_indicators") as mock_calc, \
         patch("backend.services.orchestrator_service.generate_signal") as mock_signal, \
         patch("backend.services.orchestrator_service.send_telegram_alert") as mock_alert:

        import pandas as pd
        mock_fetch.return_value = pd.DataFrame({"Close": [100.0]})
        mock_calc.return_value = pd.DataFrame({"Close": [100.0]})
        mock_signal.return_value = {
            "signal": "BUY_CALL",
            "current_price": 100.0,
            "vwap": 95.0,
            "ema_21": 90.0,
            "rsi_14": 60.0,
        }
        mock_alert.return_value = True

        response = client.post("/api/alpha/trigger/quant_run")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["job"] == "quant_run"
        assert len(data["results"]) == 3
        assert len(data["alerts_sent"]) == 3


def test_alpha_trigger_media_run_endpoint():
    with patch("backend.services.orchestrator_service.publish_wordpress_post") as mock_wp:
        mock_wp.return_value = True

        response = client.post("/api/alpha/trigger/media_run")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["job"] == "media_run"
        assert "recipe_title" in data
        assert data["published"] is True


def test_alpha_trigger_invalid_job_endpoint():
    response = client.post("/api/alpha/trigger/unknown_job")
    assert response.status_code == 400
    assert "Unknown job" in response.json()["detail"]
