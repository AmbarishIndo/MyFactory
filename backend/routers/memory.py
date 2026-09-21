from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Any

try:
    from backend.services.chroma_service import add_agent_memory, query_agent_memory
except ImportError:
    from services.chroma_service import add_agent_memory, query_agent_memory

router = APIRouter(
    prefix="/memory",
    tags=["memory"],
)


class MemoryLog(BaseModel):
    id: str
    agent_id: str
    timestamp: str
    content: str
    type: str


class MemoryLogInput(BaseModel):
    agent_name: str = Field(..., description="Name of the agent logging the action")
    action_executed: str = Field(..., description="Action or strategy executed by the agent")
    kpi_metric: str = Field(..., description="Key Performance Indicator measured (e.g., CTR, Conversion)")
    roi_score: float = Field(..., description="Return on Investment or impact score")


class MemoryLogResponse(BaseModel):
    status: str
    id: str
    message: str


class RetrievedMemory(BaseModel):
    id: str
    agent_name: Optional[str] = None
    action_executed: str
    kpi_metric: Optional[str] = None
    roi_score: Optional[float] = None
    distance: Optional[float] = None


class RetrievalResponse(BaseModel):
    query: str
    best_strategy: Optional[RetrievedMemory] = None
    all_matches: List[RetrievedMemory] = []
    message: Optional[str] = None


sample_memory_logs = [
    {
        "id": "mem-001",
        "agent_id": "agent-001",
        "timestamp": "2025-01-01T12:00:00Z",
        "content": "Initialized central command communication loop.",
        "type": "system",
    },
    {
        "id": "mem-002",
        "agent_id": "agent-003",
        "timestamp": "2025-01-01T12:05:00Z",
        "content": "Perimeter scan completed. No anomalies detected.",
        "type": "audit",
    },
]


@router.get("/", response_model=List[MemoryLog])
async def get_memory_logs():
    """Retrieve shared memory and context logs."""
    return sample_memory_logs


@router.post("/log", response_model=MemoryLogResponse)
async def log_agent_memory(payload: MemoryLogInput):
    """
    POST /api/memory/log
    Accepts agent_name, action_executed, kpi_metric, and roi_score.
    Embeds action_executed and stores in ChromaDB with metadata.
    """
    try:
        doc_id = add_agent_memory(
            agent_name=payload.agent_name,
            action_executed=payload.action_executed,
            kpi_metric=payload.kpi_metric,
            roi_score=payload.roi_score,
        )
        return MemoryLogResponse(
            status="success",
            id=doc_id,
            message="Agent action logged to RAG Memory Bank.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log memory: {str(e)}")


@router.get("/retrieve", response_model=RetrievalResponse)
async def retrieve_agent_memory(task_query: str = Query(..., description="Query task string to find optimal historical strategies")):
    """
    GET /api/memory/retrieve
    Queries ChromaDB for closest semantic matches to task_query, filters for highest roi_score,
    and returns top-performing strategies as historical context. Handles empty database gracefully.
    """
    try:
        matches = query_agent_memory(task_query=task_query, n_results=10)

        if not matches:
            return RetrievalResponse(
                query=task_query,
                best_strategy=None,
                all_matches=[],
                message="No memory logs found in memory bank.",
            )

        formatted_matches = [
            RetrievedMemory(
                id=m["id"],
                agent_name=m["agent_name"],
                action_executed=m["action_executed"],
                kpi_metric=m["kpi_metric"],
                roi_score=m["roi_score"],
                distance=m["distance"],
            )
            for m in matches
        ]

        # Filter/sort by highest roi_score
        # Items with roi_score None are sorted last
        sorted_matches = sorted(
            formatted_matches,
            key=lambda item: item.roi_score if item.roi_score is not None else float("-inf"),
            reverse=True,
        )

        best_strategy = sorted_matches[0] if sorted_matches else None

        return RetrievalResponse(
            query=task_query,
            best_strategy=best_strategy,
            all_matches=sorted_matches,
            message="Successfully retrieved top-performing strategies.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve memory: {str(e)}")
