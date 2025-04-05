# coding=utf-8
#!/bin/python3
#############################################
# بوت تحميل الفيديو من وسائل التواصل الاجتماعي #
#             إصدار البوت: 1.0.2             #
#     المطور: حسن | hassan-dev.com          #
#          حقوق النشر © hassan-dev.com       #
#############################################
import logging
from dotenv import load_dotenv
import os
import telebot
import subprocess
from utils import *
from telebot import types
from time import sleep
from authorized_users import is_authorized, is_admin, add_user, remove_user

# إعداد مجلد السجلات
os.makedirs("logs", exist_ok=True)

# تكوين السجلات
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# تحميل المتغيرات البيئية
load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# إنشاء كائن البوت
bot = telebot.TeleBot(bot_token)

# Export the handle_message function so it can be imported elsewhere
__all__ = ["bot", "handle_message", "setup_webhook"]


def laodInfo():
    print_app_info()
    print(f" * TOKEN LOADED : {bot_token}")
    print("============================================================")


def setup_webhook(webhook_url):
    """Set up the webhook for the bot"""
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=webhook_url)
    logging.info(f"Webhook set to {webhook_url}")


def handle_add_user_command(message):
    """Add a user to the whitelist"""
    user_id = message.from_user.id
    command = message.text.split()

    if len(command) != 2:
        bot.reply_to(message, "❌ الصيغة الصحيحة: /add [user_id]")
        return

    if not is_admin(user_id):
        bot.reply_to(message, "⛔ هذا الأمر متاح للمسؤولين فقط.")
        return

    try:
        new_user_id = int(command[1])
        if add_user(new_user_id, added_by=user_id):
            bot.reply_to(message, f"✅ تمت إضافة المستخدم {new_user_id} بنجاح.")
        else:
            bot.reply_to(message, f"ℹ️ المستخدم {new_user_id} مصرح له بالفعل.")
    except ValueError:
        bot.reply_to(message, "❌ معرف المستخدم يجب أن يكون رقمًا.")


def handle_remove_user_command(message):
    """Remove a user from the whitelist"""
    user_id = message.from_user.id
    command = message.text.split()

    if len(command) != 2:
        bot.reply_to(message, "❌ الصيغة الصحيحة: /remove [user_id]")
        return

    if not is_admin(user_id):
        bot.reply_to(message, "⛔ هذا الأمر متاح للمسؤولين فقط.")
        return

    try:
        remove_user_id = int(command[1])
        if remove_user(remove_user_id, removed_by=user_id):
            bot.reply_to(message, f"✅ تمت إزالة المستخدم {remove_user_id} بنجاح.")
        else:
            bot.reply_to(message, f"ℹ️ المستخدم {remove_user_id} غير موجود في القائمة.")
    except ValueError:
        bot.reply_to(message, "❌ معرف المستخدم يجب أن يكون رقمًا.")


def handle_commands(message):
    """Handle bot commands"""
    user_id = message.from_user.id
    command = message.text.split()

    if command[0] == "/start":
        bot.reply_to(
            message, "مرحبًا بك في بوت تحميل الفيديو! أرسل لي رابط فيديو للتحميل."
        )

    elif command[0] == "/help":
        help_text = """🔍 *طريقة الاستخدام*:
1️⃣ أرسل رابط فيديو من يوتيوب، فيسبوك، انستغرام، تويتر، تيك توك، أو تيرابوكس
2️⃣ انتظر قليلاً أثناء معالجة الفيديو
3️⃣ سأرسل لك الفيديو مباشرة!

*الأوامر المتاحة*:
/help - عرض هذه الرسالة
/users - عرض المستخدمين المصرح لهم (للمسؤولين فقط)
/add [user_id] - إضافة مستخدم (للمسؤولين فقط)
/remove [user_id] - إزالة مستخدم (للمسؤولين فقط)"""
        bot.reply_to(message, help_text, parse_mode="Markdown")

    # Admin commands
    elif command[0] == "/users" and is_admin(user_id):
        from authorized_users import load_authorized_users

        users, admins = load_authorized_users()
        user_list = "\n".join([f"👤 User: {uid}" for uid in users])
        admin_list = "\n".join([f"👑 Admin: {uid}" for uid in admins])
        bot.reply_to(
            message,
            f"*المستخدمون المصرح لهم*:\n{admin_list}\n{user_list}",
            parse_mode="Markdown",
        )

    elif command[0] == "/add" and is_admin(user_id):
        handle_add_user_command(message)

    elif command[0] == "/remove" and is_admin(user_id):
        handle_remove_user_command(message)

    else:
        bot.reply_to(message, "أرسل رابط فيديو للتحميل أو استخدم /help للمساعدة.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = None
    wait_message = None
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id

        # Check if user is authorized
        if not is_authorized(user_id):
            # Special case for admin commands to add users
            if message.text and message.text.startswith("/add "):
                handle_add_user_command(message)
                return

            bot.reply_to(
                message,
                "⛔ أنت غير مصرح لك باستخدام هذا البوت. يرجى التواصل مع المسؤول.",
            )
            logging.warning(
                f"Unauthorized access attempt: user_id={user_id}, chat_id={chat_id}"
            )
            return

        # Rest of your existing handle_message code
        check_tmp()
        url = message.text

        # For authorized command handling
        if message.text.startswith("/"):
            handle_commands(message)
            return

        logging.info(
            f"New message from user_id: {user_id}, chat_id: {chat_id}, message: {url}"
        )

        wait_message = bot.reply_to(
            message, "⏳ الرجاء الانتظار، جاري تحميل الفيديو الخاص بك..."
        )
        downloader = check_downloader(url)

        if not downloader:
            bot.edit_message_text(
                text="❎ الرجاء إدخال رابط فيديو صالح (يوتيوب، فيسبوك، انستغرام، تويتر، تيك توك، تيرابوكس).",
                chat_id=chat_id,
                message_id=wait_message.message_id,
            )
            return

        download_info = get_video_download_info(url, downloader)

        if download_info["status"]:
            download_url = download_info.get("url", "")
            video_path = downloadFromUrl(download_url)

            if not video_path:
                bot.edit_message_text(
                    text="❎ فشل تحميل الفيديو. تأكد من صلاحية الرابط وحاول مرة أخرى.",
                    chat_id=chat_id,
                    message_id=wait_message.message_id,
                )
                return

            try:
                bot.edit_message_text(
                    text="✅ تم تحميل الفيديو بنجاح.",
                    chat_id=chat_id,
                    message_id=wait_message.message_id,
                )
            finally:
                if os.path.exists(video_path):
                    bot.send_chat_action(message.chat.id, "upload_video")
                    bot.edit_message_text(
                        text="⏳ الرجاء الانتظار، جاري رفع الفيديو الخاص بك...",
                        chat_id=chat_id,
                        message_id=wait_message.message_id,
                    )
                    try:
                        with open(video_path, "rb") as video:
                            bot.send_video(chat_id, video)
                        logging.info(f"Video uploaded successfully: {video_path}")
                    except telebot.apihelper.ApiException as e:
                        logging.error(f"Error uploading video: {e}")
                        bot.reply_to(
                            message,
                            "تعذر رفع الفيديو الخاص بك، حاول تنزيله يدويًا.",
                        )
                    try:
                        bot.delete_message(chat_id, wait_message.message_id)
                    except telebot.apihelper.ApiException as e:
                        logging.error(f"Error deleting message: {e}")
                    bot.reply_to(
                        message,
                        "شكرًا لاستخدام البوت الخاص بنا 💮😍\nتابعنا على hassan-dev.com",
                    )
                    os.remove(video_path)
                    logging.info(f"Video deleted: {video_path}")
                else:
                    bot.edit_message_text(
                        text="❎ الفيديو غير موجود في المسار!",
                        chat_id=chat_id,
                        message_id=wait_message.message_id,
                    )
        else:
            bot.edit_message_text(
                text="❎ فشل التنزيل. تأكد من تثبيت yt-dlp وصلاحية الرابط.",
                chat_id=chat_id,
                message_id=wait_message.message_id,
            )

    except Exception as e:
        logging.error(f"Error: {e}")

        # Safer error handling that checks if variables exist
        if chat_id is not None and wait_message is not None:
            try:
                bot.edit_message_text(
                    text="❎ حدث خطأ غير متوقع. الرجاء المحاولة مرة أخرى لاحقًا.",
                    chat_id=chat_id,
                    message_id=wait_message.message_id,
                )
            except:
                # Fallback if edit fails
                bot.send_message(
                    chat_id, "❎ حدث خطأ غير متوقع. الرجاء المحاولة مرة أخرى لاحقًا."
                )
        elif chat_id is not None:
            # If we have chat_id but not wait_message
            bot.send_message(
                chat_id, "❎ حدث خطأ غير متوقع. الرجاء المحاولة مرة أخرى لاحقًا."
            )


@bot.message_handler(
    func=lambda message: message.text
    and (
        "tiktok.com" in message.text.lower() or "vm.tiktok.com" in message.text.lower()
    )
)
def handle_tiktok(message):
    """Special handler for TikTok links"""
    # We'll just call the main handler but log specifically that it's TikTok
    logging.info(f"TikTok link detected: {message.text}")
    handle_message(message)


if __name__ == "__main__":
    try:
        # تنظيف المجلد المؤقت عند بدء التشغيل
        clean_tmp_folder()

        # طباعة معلومات البوت
        laodInfo()

        # بدء الاستطلاع
        logging.info("Bot started polling")
        bot.polling(none_stop=True)
    except Exception as e:
        logging.critical(f"Critical error in main thread: {e}")

# Make this file compatible with GoDaddy's default passenger_wsgi.py
try:
    # Import Flask app for WSGI compatibility
    from app import app as application
except Exception as e:
    # Create a minimal fallback app if the main app can't be loaded
    from flask import Flask

    application = Flask(__name__)

    @application.route("/")
    def error_page():
        return "حدث خطأ في تحميل التطبيق. يرجى التحقق من السجلات."

    # Still try to set up the webhook on app startup
    try:
        webhook_url = f"https://your-domain.com/webhook/{os.getenv('TELEGRAM_BOT_TOKEN').split(':')[1]}"
        setup_webhook(webhook_url)
        logging.info(f"Webhook set up via fallback: {webhook_url}")
    except Exception as e:
        logging.error(f"Failed to set up webhook in fallback mode: {e}")
