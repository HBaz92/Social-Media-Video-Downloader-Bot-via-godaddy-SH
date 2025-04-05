import os
import telebot
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Load environment variables
load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")

if not token:
    logging.error("No Telegram token found! Check .env file")
    exit(1)

# Create bot instance
bot = telebot.TeleBot(token)

# Remove any existing webhook
bot.remove_webhook()

# Set up the webhook
webhook_url = f"https://your-domain.com/webhook/{token.split(':')[1]}"
result = bot.set_webhook(url=webhook_url)

if result:
    logging.info(f"Webhook successfully set to: {webhook_url}")
else:
    logging.error("Failed to set webhook!")

# Get and log webhook info
webhook_info = bot.get_webhook_info()
logging.info(f"Current webhook URL: {webhook_info.url}")
logging.info(f"Pending updates: {webhook_info.pending_update_count}")
