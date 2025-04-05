import os
import sys
import logging
from dotenv import load_dotenv

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

# إضافة المجلد الحالي إلى مسار النظام
sys.path.insert(0, os.path.dirname(__file__))

# إنشاء مجلدات السجلات والملفات المؤقتة
os.makedirs("logs", exist_ok=True)
os.makedirs("tmp", exist_ok=True)

# تكوين السجلات
logging.basicConfig(
    filename="logs/passenger.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# استيراد تطبيق Flask من app.py
try:
    from app import app as application

    logging.info("WSGI application loaded successfully")

    # Set up webhook when application starts
    try:
        from bot import setup_webhook

        webhook_url = (
            "https://your-domain.com/webhook/"
            + os.getenv("TELEGRAM_BOT_TOKEN").split(":")[1]
        )
        setup_webhook(webhook_url)
        logging.info("Webhook setup attempted at application startup")
    except Exception as e:
        logging.error(f"Error setting up webhook: {e}")

except Exception as e:
    logging.error(f"Error loading application: {e}")
    # إنشاء تطبيق بسيط في حالة الفشل
    from flask import Flask

    application = Flask(__name__)

    @application.route("/")
    def error_page():
        return "حدث خطأ في تحميل التطبيق. يرجى التحقق من السجلات."
