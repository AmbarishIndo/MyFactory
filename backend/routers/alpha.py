from fastapi import APIRouter, HTTPException
from typing import Dict, Any

try:
    from backend.services.orchestrator_service import (
        daily_quant_run,
        daily_media_run,
        get_scheduler_status,
    )
except ImportError:
    from ..services.orchestrator_service import (
        daily_quant_run,
        daily_media_run,
        get_scheduler_status,
    )

router = APIRouter(
    prefix="/alpha",
    tags=["alpha"],
)


@router.get("/status")
async def get_alpha_status() -> Dict[str, Any]:
    """
    Returns the running status of the orchestrator scheduler and its active jobs.
    """
    status = get_scheduler_status()
    return {
        "status": "online" if status["running"] else "idle",
        "running": status["running"],
        "jobs": status["jobs"],
    }


@router.post("/trigger/{job_name}")
async def trigger_job(job_name: str) -> Dict[str, Any]:
    """
    Manually triggers a scheduled job (quant_run or media_run) immediately.
    """
    job_key = job_name.lower().strip()
    if job_key in ["quant_run", "quant"]:
        res = await daily_quant_run()
        return res
    elif job_key in ["media_run", "media"]:
        res = await daily_media_run()
        return res
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown job '{job_name}'. Valid jobs are 'quant_run' and 'media_run'.",
        )
