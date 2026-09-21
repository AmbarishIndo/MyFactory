from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

try:
    from backend.services.quant_service import (
        fetch_market_data,
        calculate_indicators,
        generate_signal,
    )
    from backend.services.chroma_service import add_agent_memory
except ImportError:
    from ..services.quant_service import (
        fetch_market_data,
        calculate_indicators,
        generate_signal,
    )
    from ..services.chroma_service import add_agent_memory

router = APIRouter(
    prefix="/quant",
    tags=["quant"],
)


class QuantScreenRequest(BaseModel):
    ticker: str


class IndicatorValues(BaseModel):
    vwap: float
    ema_21: float
    rsi_14: float


class QuantScreenResponse(BaseModel):
    ticker: str
    signal: str
    current_price: float
    indicators: IndicatorValues
    strategy: str
    memory_id: Optional[str] = None


@router.post("/screen", response_model=QuantScreenResponse)
async def screen_ticker(payload: QuantScreenRequest):
    ticker = payload.ticker.strip().upper()
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker symbol cannot be empty")

    try:
        df = fetch_market_data(ticker)
        df_indicators = calculate_indicators(df)
        signal_data = generate_signal(df_indicators)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process ticker {ticker}: {str(e)}")

    signal = signal_data["signal"]
    price = signal_data["current_price"]
    vwap = signal_data["vwap"]
    ema_21 = signal_data["ema_21"]
    rsi_14 = signal_data["rsi_14"]

    # Construct strategy description string
    strategy = (
        f"Screened {ticker}: {signal} generated based on Price > VWAP and RSI {rsi_14:.1f}"
        if signal == "BUY_CALL"
        else (
            f"Screened {ticker}: {signal} generated based on Price < VWAP and RSI {rsi_14:.1f}"
            if signal == "BUY_PUT"
            else f"Screened {ticker}: {signal} generated based on neutral technical indicators"
        )
    )

    # Log strategy into ChromaDB via add_agent_memory
    memory_id = None
    try:
        memory_id = add_agent_memory(
            agent_name="Agent Omega",
            action_executed=strategy,
            kpi_metric="trading_signal",
            roi_score=0.0,
            metadata={
                "ticker": ticker,
                "signal": signal,
                "current_price": price,
                "rsi_14": rsi_14,
            },
        )
    except Exception:
        # ChromaDB logging error should not crash the request if memory storage fails
        pass

    return QuantScreenResponse(
        ticker=ticker,
        signal=signal,
        current_price=price,
        indicators=IndicatorValues(
            vwap=vwap,
            ema_21=ema_21,
            rsi_14=rsi_14,
        ),
        strategy=strategy,
        memory_id=memory_id,
    )
