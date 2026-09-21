from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)


class Agent(BaseModel):
    id: str
    name: str
    role: str
    status: str
    active_tasks: int


# Mock in-memory database
sample_agents = [
    {
        "id": "agent-001",
        "name": "Alpha-Ops",
        "role": "System Orchestrator",
        "status": "Active",
        "active_tasks": 4,
    },
    {
        "id": "agent-002",
        "name": "Beta-Analyst",
        "role": "Data Processing & Insights",
        "status": "Idle",
        "active_tasks": 0,
    },
    {
        "id": "agent-003",
        "name": "Gamma-Sentry",
        "role": "Security & Health Monitor",
        "status": "Active",
        "active_tasks": 2,
    },
]


@router.get("/", response_model=List[Agent])
async def get_agents():
    """Retrieve list of all managed agents."""
    return sample_agents


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    """Retrieve details for a specific agent."""
    for agent in sample_agents:
        if agent["id"] == agent_id:
            return agent
    raise HTTPException(status_code=404, detail="Agent not found")
