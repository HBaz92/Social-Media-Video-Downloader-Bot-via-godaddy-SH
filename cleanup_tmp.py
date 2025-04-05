#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# تنظيف الملفات المؤقتة القديمة               #
# سيناريو التشغيل: كل 24 ساعة عبر cron job    #
#     المطور: حسن | hassan-dev.com          #
#############################################

import os
import time
import logging
from datetime import datetime

# إعداد مجلد السجلات
os.makedirs('logs', exist_ok=True)

# إعداد التسجيل
logging.basicConfig(
    filename='logs/cleanup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def cleanup_old_files(directory='tmp', hours=24):
    """حذف الملفات التي مضى عليها أكثر من 24 ساعة"""
    if not os.path.exists(directory):
        logging.warning(f"المجلد {directory} غير موجود، جاري إنشاؤه")
        os.makedirs(directory)
        return

    # الحصول على الوقت الحالي بالثواني
    current_time = time.time()
    # تحويل الساعات إلى ثواني
    time_threshold = current_time - (hours * 3600)
    
    file_count = 0
    deleted_count = 0
    total_size = 0

    logging.info(f"بدء تنظيف الملفات القديمة في مجلد {directory}")
    
    # مسح جميع الملفات في المجلد
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # تخطي المجلدات
        if os.path.isdir(file_path):
            continue
            
        file_count += 1
        file_stats = os.stat(file_path)
        
        # التحقق من عمر الملف
        if file_stats.st_mtime < time_threshold:
            try:
                file_size = os.path.getsize(file_path)
                total_size += file_size
                
                os.remove(file_path)
                deleted_count += 1
                
                # تسجيل عمر الملف
                file_modified = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                file_size_mb = file_size / (1024 * 1024)
                
                logging.info(f"تم حذف الملف: {filename} (الحجم: {file_size_mb:.2f} ميجابايت، تاريخ التعديل: {file_modified})")
            except Exception as e:
                logging.error(f"خطأ في حذف الملف {filename}: {e}")
    
    # حساب الحجم الكلي بالميجابايت
    total_size_mb = total_size / (1024 * 1024)
    
    logging.info(f"اكتمل التنظيف: تم حذف {deleted_count} من أصل {file_count} ملفات")
    logging.info(f"تم تحرير {total_size_mb:.2f} ميجابايت من مساحة التخزين")
    
    print(f"تم حذف {deleted_count} ملفات قديمة بحجم إجمالي {total_size_mb:.2f} ميجابايت")

if __name__ == "__main__":
    cleanup_old_files()