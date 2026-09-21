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


@router.post("/beta")
async def init_agent_beta():
    """Initialize Agent Beta (Market Scout)."""
    return {
        "status": "initialized",
        "agent": "Beta",
        "name": "Market Scout",
        "details": "Market Scout initialized and monitoring market opportunities."
    }


@router.post("/omega")
async def init_agent_omega():
    """Initialize Agent Omega (Quant Engine)."""
    return {
        "status": "initialized",
        "agent": "Omega",
        "name": "Quant Engine",
        "details": "Quant Engine initialized and algorithmic models active."
    }


@router.post("/sigma")
async def init_agent_sigma():
    """Initialize Agent Sigma (Media Studio)."""
    return {
        "status": "initialized",
        "agent": "Sigma",
        "name": "Media Studio",
        "details": "Media Studio initialized and content generation pipeline online."
    }
