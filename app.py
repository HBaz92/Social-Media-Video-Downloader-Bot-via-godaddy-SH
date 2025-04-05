import logging
import os
from flask import Flask, render_template_string, redirect, url_for, request
from telebot import types

# In app.py webhook route, you call handle_message but don't import it
from bot import setup_webhook, handle_message  # Missing this import

# إعداد مجلد السجلات
os.makedirs("logs", exist_ok=True)

app = Flask("SOCIAL-BOT")

# Import this after the Flask app is created
bot = None
handle_message = None

# Add after app configuration but before if __name__ == "__main__"
# Delayed imports to avoid circular references
from bot import bot, handle_message


@app.route("/")
def home():
    html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta property="og:title" content="hassan-dev.com | الصفحة الرئيسية">
  <meta property="og:type" content="website">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>حسن | hassan-dev.com</title>
  <meta name="description" content="بوت تحميل الفيديو من وسائل التواصل الاجتماعي">
  <meta name="keywords" content="تحميل فيديو,يوتيوب,فيسبوك,انستغرام,تويتر,تيليجرام بوت">
  <meta name="author" content="Hassan">

  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/all.css">
  <link rel="stylesheet" href="https://unpkg.com/tailwindcss@2.2.19/dist/tailwind.min.css"/> 
</head>

<body class="font-sans antialiased text-gray-900 leading-normal tracking-wider bg-cover" style="background-image:url('https://source.unsplash.com/1L71sPT5XKc');">
  <div class="max-w-4xl flex items-center h-auto lg:h-screen flex-wrap mx-auto my-32 lg:my-0">
    <div id="profile" class="w-full lg:w-3/5 rounded-lg lg:rounded-l-lg lg:rounded-r-none shadow-2xl bg-white opacity-75 mx-6 lg:mx-0">
      <div class="p-4 md:p-12 text-center lg:text-left">
        <h1 class="text-3xl font-bold pt-8 lg:pt-0">بوت تحميل الفيديو</h1>
        <div class="mx-auto lg:mx-0 w-4/5 pt-3 border-b-2 border-green-500 opacity-25"></div>
        <p class="pt-8 text-sm">مرحبًا! هذا بوت لتحميل مقاطع الفيديو من منصات التواصل الاجتماعي المختلفة بما في ذلك يوتيوب وفيسبوك وانستغرام وتويتر وتيرابوكس.</p>
        <p class="pt-2 text-sm">يمكنك استخدام البوت مباشرة على تيليجرام!</p>
        
        <div class="pt-12 pb-8">
          <a href="https://t.me/YourBotUsername" class="bg-green-700 hover:bg-green-900 text-white font-bold py-2 px-4 rounded-full">
            استخدم البوت الآن
          </a>
        </div>

        <div class="mt-6 pb-16 lg:pb-0 w-4/5 lg:w-full mx-auto flex flex-wrap items-center justify-between">
          <a class="link" href="https://hassan-dev.com" data-tippy-content="زيارة الموقع"><svg class="h-6 fill-current text-gray-600 hover:text-green-700" role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>الموقع</title><path d="M10 20a10 10 0 1 1 0-20 10 10 0 0 1 0 20zm7.75-8a8.01 8.01 0 0 0 0-4h-3.82a28.81 28.81 0 0 1 0 4h3.82zm-.82 2h-3.22a14.44 14.44 0 0 1-.95 3.51A8.03 8.03 0 0 0 16.93 14zm-8.85-2h3.84a24.61 24.61 0 0 0 0-4H8.08a24.61 24.61 0 0 0 0 4zm.25 2c.41 2.4 1.13 4 1.67 4s1.26-1.6 1.67-4H8.33zm-6.08-2h3.82a28.81 28.81 0 0 1 0-4H2.25a8.01 8.01 0 0 0 0 4zm.82 2a8.03 8.03 0 0 0 4.17 3.51c-.42-.96-.74-2.16-.95-3.51H3.07zm13.86-8a8.03 8.03 0 0 0-4.17-3.51c.42.96.74 2.16.95 3.51h3.22zm-8.6 0h3.34c-.41-2.4-1.13-4-1.67-4S8.74 3.6 8.33 6zM3.07 6h3.22c.2-1.35.53-2.55.95-3.51A8.03 8.03 0 0 0 3.07 6z"/></svg></a>
        </div>
      </div>
    </div>
    
    <div class="w-full lg:w-2/5">
      <img src="YOUR_LOGO_URL" class="rounded-none lg:rounded-lg shadow-2xl hidden lg:block">
    </div>
  </div>
</body>
</html>"""
    return render_template_string(html_content)


@app.route("/health")
def health_check():
    """نقطة نهاية للتحقق من صحة التطبيق"""
    return {"status": "ok", "version": "1.0.2"}


@app.route("/start-bot")
def start_bot_route():
    """واجهة ويب لبدء تشغيل البوت"""
    try:
        os.system("python bot_service.py start")
        return "تم بدء تشغيل البوت بنجاح"
    except Exception as e:
        return f"حدث خطأ: {e}"


@app.route("/webhook/<token>", methods=["POST"])
def webhook(token):
    if token != os.getenv("TELEGRAM_BOT_TOKEN").split(":")[1]:
        return "Unauthorized", 401

    update = request.get_json()
    # Process the update here or pass to a function
    if "message" in update and "text" in update["message"]:
        # Mock the message object that would normally be passed to handle_message
        message = types.Message.de_json(update["message"])
        handle_message(message)
    return "OK", 200


# Add a new route for debugging webhook status
@app.route("/webhook-status")
def webhook_status():
    try:
        from bot import bot

        webhook_info = bot.get_webhook_info()
        return {
            "webhook_url": webhook_info.url,
            "has_webhook": bool(webhook_info.url),
            "pending_updates": webhook_info.pending_update_count,
            "telegram_token_loaded": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
            "token_suffix": (
                os.getenv("TELEGRAM_BOT_TOKEN").split(":")[-1]
                if os.getenv("TELEGRAM_BOT_TOKEN")
                else None
            ),
        }
    except Exception as e:
        return {"error": str(e)}


# تكوين سجلات Flask
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
log.propagate = False

# تكوين سجل التطبيق
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/flask.log")
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
app.logger.addHandler(handler)

if __name__ == "__main__":
    # تشغيل محلي فقط للاختبار
    app.run(host="127.0.0.1", port=5000, debug=False)
