from fastapi import APIRouter, HTTPException

try:
    from backend.models.media_models import VideoScript, RecipeCard, VlogRequest, RecipeRequest
    from backend.services.media_service import generate_vlog_script, generate_recipe
    from backend.services.chroma_service import add_agent_memory
except ImportError:
    from models.media_models import VideoScript, RecipeCard, VlogRequest, RecipeRequest
    from services.media_service import generate_vlog_script, generate_recipe
    from services.chroma_service import add_agent_memory

router = APIRouter(
    prefix="/media",
    tags=["media"],
)


@router.post("/vlog", response_model=VideoScript)
async def create_vlog_script(payload: VlogRequest):
    """
    POST /api/media/vlog
    Generates a VideoScript based on topic and platform, logs the script string into ChromaDB under Agent Sigma,
    and returns the VideoScript model.
    """
    try:
        script = generate_vlog_script(topic=payload.topic, platform=payload.platform)
        script_json = script.model_dump_json()

        add_agent_memory(
            agent_name="Agent Sigma",
            action_executed=script_json,
            kpi_metric="viewer_retention",
            roi_score=0.0,
        )

        return script
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate vlog script: {str(e)}")


@router.post("/recipe", response_model=RecipeCard)
async def create_recipe_card(payload: RecipeRequest):
    """
    POST /api/media/recipe
    Generates a RecipeCard based on dish_name and diet_type, logs the card string into ChromaDB under Agent Sigma,
    and returns the RecipeCard model.
    """
    try:
        recipe = generate_recipe(dish_name=payload.dish_name, diet_type=payload.diet_type)
        recipe_json = recipe.model_dump_json()

        add_agent_memory(
            agent_name="Agent Sigma",
            action_executed=recipe_json,
            kpi_metric="affiliate_clicks",
            roi_score=0.0,
        )

        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recipe card: {str(e)}")
