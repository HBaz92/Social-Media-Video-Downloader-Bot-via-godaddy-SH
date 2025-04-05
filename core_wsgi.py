import os
import sys
import logging
from dotenv import load_dotenv


def get_application():
    """
    Core implementation that returns the Flask application
    This will persist even when GoDaddy resets passenger_wsgi.py
    """
    # Load environment variables
    load_dotenv()

    # Manually check Telegram token
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        # Try to load from .env file directly if environment variable isn't set
        try:
            with open(os.path.join(os.path.dirname(__file__), ".env"), "r") as f:
                for line in f:
                    if line.startswith("TELEGRAM_BOT_TOKEN="):
                        os.environ["TELEGRAM_BOT_TOKEN"] = line.split("=", 1)[1].strip()
                        break
        except Exception as e:
            logging.error(f"Failed to load .env file: {e}")

    # Create logs and tmp directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("tmp", exist_ok=True)

    # Configure logging
    logging.basicConfig(
        filename="logs/passenger.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Import Flask app
    try:
        from app import app

        logging.info("WSGI application loaded successfully")

        # Set up webhook when application starts
        try:
            from bot import setup_webhook

            webhook_url = (
                "https://sm.hassan-dev.com/webhook/"
                + os.getenv("TELEGRAM_BOT_TOKEN").split(":")[1]
            )
            setup_webhook(webhook_url)
            logging.info("Webhook setup attempted at application startup")
        except Exception as e:
            logging.error(f"Error setting up webhook: {e}")

        return app
    except Exception as e:
        logging.error(f"Error loading application: {e}")
        # Create a simple app in case of failure
        from flask import Flask

        error_app = Flask(__name__)

        @error_app.route("/")
        def error_page():
            return "حدث خطأ في تحميل التطبيق. يرجى التحقق من السجلات."

        return error_app
