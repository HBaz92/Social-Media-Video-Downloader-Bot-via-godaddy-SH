#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# خدمة تشغيل البوت في الخلفية                 #
# سيناريو التشغيل: عبر cron job عند إعادة     #
# تشغيل الخادم أو بشكل يدوي                  #
#     المطور: حسن | hassan-dev.com          #
#############################################
# إعدادات البيئة
import subprocess
import os
import sys
import signal
import time
import logging
from datetime import datetime

# إعداد مجلد السجلات
os.makedirs("logs", exist_ok=True)

# إعداد التسجيل
logging.basicConfig(
    filename="logs/bot_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def is_bot_running():
    """التحقق مما إذا كان البوت قيد التشغيل بالفعل"""
    try:
        with open("bot.pid", "r") as f:
            pid = int(f.read().strip())

        # التحقق مما إذا كانت العملية لا تزال قائمة
        os.kill(pid, 0)
        return True
    except (FileNotFoundError, ProcessLookupError, ValueError, OSError):
        return False


def start_bot():
    """بدء تشغيل البوت في الخلفية"""
    if is_bot_running():
        logging.info("البوت قيد التشغيل بالفعل")
        return

    logging.info("جاري بدء تشغيل البوت...")

    # استخدام nohup لإبقاء البوت يعمل حتى بعد انتهاء الجلسة
    try:
        process = subprocess.Popen(
            [sys.executable, "bot.py"],
            stdout=open("logs/bot_output.log", "a"),
            stderr=open("logs/bot_error.log", "a"),
            preexec_fn=os.setpgrp,
        )

        # حفظ معرف العملية
        with open("bot.pid", "w") as f:
            f.write(str(process.pid))

        logging.info(f"تم بدء تشغيل البوت بنجاح (PID: {process.pid})")
        print(f"تم بدء تشغيل البوت بنجاح (PID: {process.pid})")
    except Exception as e:
        logging.error(f"فشل بدء تشغيل البوت: {e}")
        print(f"فشل بدء تشغيل البوت: {e}")


def stop_bot():
    """إيقاف تشغيل البوت"""
    try:
        with open("bot.pid", "r") as f:
            pid = int(f.read().strip())

        # إرسال إشارة إنهاء للعملية
        os.kill(pid, signal.SIGTERM)

        # انتظار للتأكد من توقف العملية
        time.sleep(2)

        try:
            # التحقق مما إذا كانت العملية لا تزال موجودة
            os.kill(pid, 0)
            # إذا وصلنا إلى هنا، فالعملية لا تزال موجودة، استخدم SIGKILL
            os.kill(pid, signal.SIGKILL)
            logging.warning(f"تم إجبار البوت على التوقف (PID: {pid})")
        except OSError:
            # العملية توقفت بالفعل
            logging.info(f"تم إيقاف تشغيل البوت بنجاح (PID: {pid})")

        # حذف ملف PID
        os.remove("bot.pid")
        print(f"تم إيقاف تشغيل البوت (PID: {pid})")
    except (FileNotFoundError, ValueError):
        logging.warning("ملف PID غير موجود أو غير صالح")
        print("البوت ليس قيد التشغيل حاليًا")
    except ProcessLookupError:
        logging.warning(f"العملية ذات المعرف {pid} غير موجودة")
        # حذف ملف PID القديم
        try:
            os.remove("bot.pid")
        except:
            pass
        print(f"البوت ليس قيد التشغيل حاليًا (PID غير صالح: {pid})")
    except Exception as e:
        logging.error(f"خطأ عند إيقاف تشغيل البوت: {e}")
        print(f"خطأ عند إيقاف تشغيل البوت: {e}")


def restart_bot():
    """إعادة تشغيل البوت"""
    stop_bot()
    time.sleep(2)  # انتظار لمدة ثانيتين
    start_bot()


if __name__ == "__main__":
    # تنظيف مجلد tmp عند بدء التشغيل
    try:
        from utils import clean_tmp_folder

        clean_tmp_folder()
    except Exception as e:
        logging.warning(f"لم يتم تنظيف المجلد المؤقت: {e}")

    # التحقق من وجود وسيط في سطر الأوامر
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "start":
            start_bot()
        elif command == "stop":
            stop_bot()
        elif command == "restart":
            restart_bot()
        else:
            print("أمر غير صالح. استخدم: start, stop أو restart")
    else:
        # بدون وسائط، نفترض بدء التشغيل
        start_bot()
