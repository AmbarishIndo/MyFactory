from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

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
