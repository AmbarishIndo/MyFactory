import os
import random
import logging
from typing import Dict, Any, List
from apscheduler.schedulers.asyncio import AsyncIOScheduler

try:
    from backend.services.quant_service import (
        fetch_market_data,
        calculate_indicators,
        generate_signal,
    )
    from backend.services.media_service import generate_recipe
    from backend.services.broadcast_service import send_telegram_alert, publish_wordpress_post
    from backend.services.chroma_service import add_agent_memory
except ImportError:
    from services.quant_service import (
        fetch_market_data,
        calculate_indicators,
        generate_signal,
    )
    from services.media_service import generate_recipe
    from services.broadcast_service import send_telegram_alert, publish_wordpress_post
    from services.chroma_service import add_agent_memory

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def daily_quant_run() -> Dict[str, Any]:
    """
    Agent Omega quant run:
    Iterates through hardcoded tickers, fetches data, evaluates signals,
    and sends Telegram alerts for BUY_CALL / BUY_PUT signals.
    """
    tickers = ["NVDA", "AAPL", "BTC-USD"]
    results = []
    alerts_sent = []

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "dummy_bot_token")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "dummy_chat_id")

    for ticker in tickers:
        try:
            df = fetch_market_data(ticker)
            df_ind = calculate_indicators(df)
            signal_data = generate_signal(df_ind)
            signal = signal_data["signal"]
            price = signal_data["current_price"]

            res = {
                "ticker": ticker,
                "signal": signal,
                "price": price,
                "rsi_14": signal_data["rsi_14"],
            }
            results.append(res)

            if signal in ["BUY_CALL", "BUY_PUT"]:
                alert_msg = (
                    f"🚨 [QUANT ALERT] Ticker: {ticker} | Signal: {signal} | "
                    f"Price: ${price:.2f} | RSI: {signal_data['rsi_14']:.1f}"
                )
                sent = send_telegram_alert(bot_token, chat_id, alert_msg)
                alerts_sent.append({
                    "ticker": ticker,
                    "signal": signal,
                    "message": alert_msg,
                    "delivered": sent,
                })

                # Log memory
                try:
                    add_agent_memory(
                        agent_name="Agent Alpha",
                        action_executed=f"Dispatched Telegram alert for {ticker}: {signal}",
                        kpi_metric="broadcast_alert",
                        roi_score=1.0,
                        metadata={"ticker": ticker, "signal": signal},
                    )
                except Exception as mem_err:
                    logger.warning(f"Failed to log memory for quant alert: {mem_err}")

        except Exception as e:
            logger.error(f"Error executing quant run for ticker {ticker}: {e}")
            results.append({"ticker": ticker, "error": str(e)})

    return {
        "status": "completed",
        "job": "quant_run",
        "results": results,
        "alerts_sent": alerts_sent,
    }


def recipe_card_to_html(recipe) -> str:
    """
    Converts a RecipeCard object into HTML format for WordPress publishing.
    """
    ingredients_html = "".join([f"<li>{ing}</li>" for ing in recipe.ingredients])
    instructions_html = "".join([f"<li>{inst}</li>" for inst in recipe.instructions])

    return (
        f"<h1>{recipe.title}</h1>\n"
        f"<p><strong>Cinematic Visual Prompt:</strong> {recipe.cinematic_image_prompt}</p>\n"
        f"<h2>Ingredients</h2>\n"
        f"<ul>\n{ingredients_html}\n</ul>\n"
        f"<h2>Instructions</h2>\n"
        f"<ol>\n{instructions_html}\n</ol>"
    )


async def daily_media_run() -> Dict[str, Any]:
    """
    Agent Sigma media run:
    Generates a recipe card for a random dish, converts it to HTML, and publishes to WordPress.
    """
    sample_dishes = ["Truffle Ramen", "Matcha Cheesecake", "Vegan Gnocchi", "Aesthetic Avocado Toast", "Cyberpunk Dumplings"]
    sample_diets = ["Gourmet", "Vegan", "Keto", "Gluten-Free"]

    dish = random.choice(sample_dishes)
    diet = random.choice(sample_diets)

    wp_url = os.getenv("WORDPRESS_URL", os.getenv("WP_URL", "https://example.com"))
    wp_user = os.getenv("WORDPRESS_USER", os.getenv("WP_USER", "admin"))
    wp_pass = os.getenv("WORDPRESS_PASS", os.getenv("WP_PASS", "password"))

    try:
        recipe = generate_recipe(dish_name=dish, diet_type=diet)
        html_content = recipe_card_to_html(recipe)
        published = publish_wordpress_post(wp_url, wp_user, wp_pass, recipe.title, html_content)

        # Log memory
        try:
            add_agent_memory(
                agent_name="Agent Alpha",
                action_executed=f"Published WordPress post for recipe: {recipe.title}",
                kpi_metric="content_broadcast",
                roi_score=1.0,
                metadata={"title": recipe.title, "dish": dish, "diet": diet},
            )
        except Exception as mem_err:
            logger.warning(f"Failed to log memory for media run: {mem_err}")

        return {
            "status": "completed",
            "job": "media_run",
            "recipe_title": recipe.title,
            "published": published,
            "dish": dish,
            "diet": diet,
        }
    except Exception as e:
        logger.error(f"Error executing media run: {e}")
        return {
            "status": "failed",
            "job": "media_run",
            "error": str(e),
        }


def start_scheduler():
    """
    Starts the AsyncIOScheduler and adds cron jobs if not already present.
    """
    if not scheduler.running:
        if not scheduler.get_job("daily_quant_run"):
            scheduler.add_job(
                daily_quant_run,
                "cron",
                hour=9,
                minute=0,
                id="daily_quant_run",
                replace_existing=True,
            )
        if not scheduler.get_job("daily_media_run"):
            scheduler.add_job(
                daily_media_run,
                "cron",
                hour=10,
                minute=0,
                id="daily_media_run",
                replace_existing=True,
            )
        try:
            scheduler.start()
            logger.info("Agent Alpha Scheduler started.")
        except RuntimeError as e:
            logger.warning(f"Could not start scheduler: {e}")


def stop_scheduler():
    """
    Stops the AsyncIOScheduler.
    """
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Agent Alpha Scheduler stopped.")


def get_scheduler_status() -> Dict[str, Any]:
    """
    Returns current status of the scheduler and list of active scheduled jobs.
    """
    jobs = []
    if scheduler.running or len(scheduler.get_jobs()) > 0:
        for job in scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": str(job.next_run_time) if job.next_run_time else None,
            })
    return {
        "running": scheduler.running,
        "jobs": jobs,
    }
