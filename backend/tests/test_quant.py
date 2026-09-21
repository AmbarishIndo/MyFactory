import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from fastapi.testclient import TestClient

from backend.main import app
from backend.services.quant_service import (
    calculate_indicators,
    generate_signal,
    fetch_market_data,
)


class TestQuantServiceAndRouter(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_generate_signal_bullish(self):
        """Verify BUY_CALL generated when price > VWAP, price > EMA_21, RSI in 50-70."""
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        df = pd.DataFrame(
            {
                "Open": [100.0] * 30,
                "High": [110.0] * 30,
                "Low": [90.0] * 30,
                "Close": [100.0] * 29 + [108.0],
                "Volume": [1000] * 30,
            },
            index=dates,
        )
        df = calculate_indicators(df)
        df.loc[df.index[-1], "VWAP"] = 100.0
        df.loc[df.index[-1], "EMA_21"] = 102.0
        df.loc[df.index[-1], "RSI_14"] = 60.0

        res = generate_signal(df)
        self.assertEqual(res["signal"], "BUY_CALL")
        self.assertEqual(res["current_price"], 108.0)
        self.assertEqual(res["vwap"], 100.0)
        self.assertEqual(res["ema_21"], 102.0)
        self.assertEqual(res["rsi_14"], 60.0)

    def test_generate_signal_bearish(self):
        """Verify BUY_PUT generated when price < VWAP, price < EMA_21, RSI in 30-50."""
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        df = pd.DataFrame(
            {
                "Open": [100.0] * 30,
                "High": [110.0] * 30,
                "Low": [90.0] * 30,
                "Close": [100.0] * 29 + [90.0],
                "Volume": [1000] * 30,
            },
            index=dates,
        )
        df = calculate_indicators(df)
        df.loc[df.index[-1], "VWAP"] = 100.0
        df.loc[df.index[-1], "EMA_21"] = 98.0
        df.loc[df.index[-1], "RSI_14"] = 40.0

        res = generate_signal(df)
        self.assertEqual(res["signal"], "BUY_PUT")
        self.assertEqual(res["current_price"], 90.0)

    def test_generate_signal_neutral(self):
        """Verify NEUTRAL generated when conditions for BUY_CALL or BUY_PUT are not met."""
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        df = pd.DataFrame(
            {
                "Open": [100.0] * 30,
                "High": [110.0] * 30,
                "Low": [90.0] * 30,
                "Close": [100.0] * 30,
                "Volume": [1000] * 30,
            },
            index=dates,
        )
        df = calculate_indicators(df)
        df.loc[df.index[-1], "VWAP"] = 100.0
        df.loc[df.index[-1], "EMA_21"] = 100.0
        df.loc[df.index[-1], "RSI_14"] = 50.0

        res = generate_signal(df)
        self.assertEqual(res["signal"], "NEUTRAL")

    @patch("backend.routers.quant.add_agent_memory")
    @patch("backend.routers.quant.fetch_market_data")
    def test_screen_endpoint_success(self, mock_fetch, mock_add_memory):
        """Test POST /api/quant/screen endpoint returns signal, price, indicators, and logs memory."""
        mock_add_memory.return_value = "mock-memory-uuid-1234"

        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        df_mock = pd.DataFrame(
            {
                "Open": [150.0] * 30,
                "High": [155.0] * 30,
                "Low": [145.0] * 30,
                "Close": [150.0] * 29 + [160.0],
                "Volume": [50000] * 30,
            },
            index=dates,
        )
        mock_fetch.return_value = df_mock

        response = self.client.post("/api/quant/screen", json={"ticker": "AAPL"})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["ticker"], "AAPL")
        self.assertIn("signal", data)
        self.assertIn("current_price", data)
        self.assertIn("indicators", data)
        self.assertIn("vwap", data["indicators"])
        self.assertIn("ema_21", data["indicators"])
        self.assertIn("rsi_14", data["indicators"])
        self.assertIn("Screened AAPL:", data["strategy"])
        self.assertEqual(data["memory_id"], "mock-memory-uuid-1234")

        mock_add_memory.assert_called_once()
        _, kwargs = mock_add_memory.call_args
        self.assertEqual(kwargs["agent_name"], "Agent Omega")
        self.assertEqual(kwargs["roi_score"], 0.0)

    @patch("backend.routers.quant.fetch_market_data")
    def test_screen_endpoint_invalid_ticker(self, mock_fetch):
        """Test POST /api/quant/screen endpoint handles fetch failure gracefully."""
        mock_fetch.side_effect = ValueError("No market data found for ticker 'INVALID'")

        response = self.client.post("/api/quant/screen", json={"ticker": "INVALID"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("No market data found", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
