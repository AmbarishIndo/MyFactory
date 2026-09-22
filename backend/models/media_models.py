from typing import List
from pydantic import BaseModel, Field


class Scene(BaseModel):
    timestamp: str = Field(..., description="Timestamp or duration of the scene (e.g., '0:00 - 0:05')")
    video_prompt: str = Field(..., description="Visual description for image-to-video diffusion models")
    audio_cue: str = Field(..., description="TTS dialogue or ASMR sound design instructions")


class VideoScript(BaseModel):
    title: str = Field(..., description="Title of the video script")
    hook: str = Field(..., description="Hook statement to grab viewer attention")
    platform: str = Field(..., description="Target platform, e.g. YouTube Shorts, TikTok")
    scenes: List[Scene] = Field(..., description="List of sequential scenes for the script")


class RecipeCard(BaseModel):
    title: str = Field(..., description="Title of the dish")
    ingredients: List[str] = Field(..., description="List of required ingredients")
    instructions: List[str] = Field(..., description="ASMR-focused cooking instructions")
    cinematic_image_prompt: str = Field(..., description="High-fidelity image generation prompt for Midjourney/DALL-E")


class VlogRequest(BaseModel):
    topic: str = Field(..., description="Topic of the faceless vlog")
    platform: str = Field(default="YouTube Shorts", description="Target platform")


class RecipeRequest(BaseModel):
    dish_name: str = Field(..., description="Name of the dish")
    diet_type: str = Field(default="Standard", description="Dietary preference or restrictions")
