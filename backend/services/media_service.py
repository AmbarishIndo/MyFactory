try:
    from backend.models.media_models import Scene, VideoScript, RecipeCard
except ImportError:
    from models.media_models import Scene, VideoScript, RecipeCard


def generate_vlog_script(topic: str, platform: str) -> VideoScript:
    """
    Generates a structured VideoScript object for a faceless vlog on a given topic and platform.
    """
    title = f"No-Travel Faceless Vlog: {topic}"
    hook = f"Want to experience {topic} without ever booking a flight? Here is how."

    scenes = [
        Scene(
            timestamp="0:00 - 0:03",
            video_prompt=f"Hyper-realistic 8k cinematic drone shot flying through vibrant neon-lit streets relevant to {topic}, dusk setting, volumetric lighting.",
            audio_cue="[Upbeat lo-fi beat starts] Narration: What if you could explore the world right from your room?",
        ),
        Scene(
            timestamp="0:03 - 0:08",
            video_prompt=f"POV slow motion shot walking down a serene, atmospheric alleyway depicting {topic}, soft rainfall on glowing pavement.",
            audio_cue="[Subtle rain pitter-patter ASMR audio] Narration: Immerse yourself in the hidden gems of this iconic location.",
        ),
        Scene(
            timestamp="0:08 - 0:15",
            video_prompt=f"Macro shot of authentic local delicacies and aesthetic architecture related to {topic}, shallow depth of field.",
            audio_cue="[Sizzle sound effect, soft whisper] Narration: Like, comment, and follow for your daily virtual escape.",
        ),
    ]

    return VideoScript(
        title=title,
        hook=hook,
        platform=platform,
        scenes=scenes,
    )


def generate_recipe(dish_name: str, diet_type: str) -> RecipeCard:
    """
    Generates a structured RecipeCard object with ASMR sound design and cinematic image prompts.
    """
    title = f"{diet_type.strip() if diet_type else 'Gourmet'} {dish_name}"

    ingredients = [
        f"500g Fresh Ingredients tailored for {dish_name}",
        "2 tbsp Organic Olive Oil",
        "1 tbsp Spicy Gochujang Paste or diet-friendly seasoning",
        "3 cloves Garlic, finely minced",
        "Fresh herbs and toasted sesame seeds for garnish",
    ]

    instructions = [
        "[ASMR: Soft wood slicing sound] Finely chop garlic and prepare herbs on a solid oak cutting board.",
        "[ASMR: Sizzling hot pan sound] Heat olive oil in a heavy cast-iron skillet over medium-high heat.",
        "[ASMR: Liquid pour & bubbling sound] Add ingredients along with sauce base, tossing continuously until glazed and glossy.",
        "[ASMR: Crisp crunch audio] Plate delicately, garnish with fresh herbs and sesame seeds, and serve immediately.",
    ]

    cinematic_image_prompt = (
        f"Award-winning food photography of {title}, served in a dark ceramic bowl, "
        f"glistening glaze, steam rising softly, moody lighting, shallow depth of field, "
        f"shot on Hasselblad 85mm, 8k resolution, photorealistic."
    )

    return RecipeCard(
        title=title,
        ingredients=ingredients,
        instructions=instructions,
        cinematic_image_prompt=cinematic_image_prompt,
    )
