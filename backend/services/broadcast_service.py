import requests
import logging

logger = logging.getLogger(__name__)


def send_telegram_alert(bot_token: str, chat_id: str, message: str) -> bool:
    """
    Sends a message to a Telegram chat using the Telegram Bot API.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.ok:
            return True
        else:
            logger.error(f"Telegram API error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Failed to send Telegram alert: {e}")
        return False


def publish_wordpress_post(wp_url: str, wp_user: str, wp_pass: str, title: str, content: str) -> bool:
    """
    Publishes a post to a WordPress site using the WordPress REST API.
    """
    endpoint = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
    payload = {
        "title": title,
        "content": content,
        "status": "publish",
    }
    try:
        response = requests.post(
            endpoint,
            json=payload,
            auth=(wp_user, wp_pass),
            timeout=10,
        )
        if response.status_code in (200, 201) or response.ok:
            return True
        else:
            logger.error(f"WordPress API error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Failed to publish WordPress post: {e}")
        return False
