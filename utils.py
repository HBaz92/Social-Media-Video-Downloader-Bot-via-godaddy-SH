import os
import random
import string
import logging
import subprocess
import requests
import socket
import time
from datetime import datetime


def clear():
    """Clear the terminal screen based on the OS"""
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Mac/Linux
        os.system("clear")


def random_name(length=12):
    """Generate a random filename"""
    letters = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for i in range(length)) + ".mp4"


def check_tmp():
    """Create tmp directory if it doesn't exist"""
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
        print("[+] Created tmp directory")


def check_system_ip():
    """Check and display system IP address"""
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(f" * SYSTEM IP ADDRESS : {ip}")
    except Exception as e:
        print(f"[!] Error getting IP: {e}")


def print_app_info():
    """Print application info header"""
    print(
        """
    #############################################
    # بوت تحميل الفيديو من وسائل التواصل الاجتماعي #
    #             إصدار البوت: 1.0.2             #
    #     المطور: حسن | hassan-dev.com          #
    #          حقوق النشر © hassan-dev.com       #
    #############################################
    """
    )


def check_downloader(url):
    """Check what type of downloader to use based on URL"""
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "facebook.com" in url or "fb.watch" in url:
        return "facebook"
    elif "instagram.com" in url:
        return "instagram"
    elif "twitter.com" in url or "x.com" in url:
        return "twitter"
    elif "terabox.com" in url:
        return "terabox"
    elif "tiktok.com" in url or "vm.tiktok.com" in url or "vt.tiktok.com" in url:
        return "tiktok"
    return None


def get_video_download_info(video_url, downloader):
    """Prepare video info for download directly with yt-dlp"""
    try:
        print(f"[+] Preparing to download from: {video_url}")
        # No need for API anymore, just pass the URL
        return {"status": True, "url": video_url, "downloader": downloader}
    except Exception as e:
        print(f"[+] Error preparing download: {e}")
        return {"status": False, "message": f"Error: {e}"}


def downloadFromUrl(url, destination_folder="tmp"):
    """Download video from URL using yt-dlp"""
    try:
        # Create the tmp folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        # Generate a random filename
        FileName = random_name()
        file_path = os.path.join(destination_folder, FileName)

        # Use yt-dlp to download the video
        print(f"[+] Downloading from: {url}")

        # Check if yt-dlp is installed
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            print("[!] yt-dlp not found. Make sure it's installed and in your PATH")
            return False

        # Check if this is a TikTok URL
        yt_dlp_args = [
            "yt-dlp",
            url,
            "-o",
            file_path,
            "--no-warnings",
            "--format",
            "best[ext=mp4]/best",  # Prefer MP4 format
        ]

        # For TikTok, add specific options
        if "tiktok.com" in url or "vm.tiktok.com" in url or "vt.tiktok.com" in url:
            print("[+] Detected TikTok URL, using specialized parameters")
            tiktok_options = get_tiktok_options()
            if tiktok_options.get("http_headers"):
                for header, value in tiktok_options["http_headers"].items():
                    yt_dlp_args.extend(["--add-header", f"{header}:{value}"])

            yt_dlp_args.extend(["--extractor-retries", "5"])
            yt_dlp_args.extend(["--no-check-certificate"])

            # Try using both methods to increase success rate
            try:
                result = subprocess.run(yt_dlp_args, capture_output=True, text=True)

                # If first attempt fails with yt-dlp, try alternative method with more options
                if result.returncode != 0:
                    print(
                        "[!] First TikTok download attempt failed, trying alternative method"
                    )
                    yt_dlp_args.extend(["--force-generic-extractor"])
                    result = subprocess.run(yt_dlp_args, capture_output=True, text=True)
            except Exception as e:
                print(f"[!] TikTok download error: {e}")
                return False
        else:
            # For non-TikTok URLs, proceed normally
            result = subprocess.run(yt_dlp_args, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[!] yt-dlp error: {result.stderr}")
            return False

        print(f"[+] File saved in: {file_path}")

        # Verify the file exists and has content
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return file_path
        else:
            print("[!] File download seems to have failed - empty or missing file")
            return False

    except Exception as e:
        print(f"[+] Download error: {e}")
        return False


def clean_tmp_folder():
    """تنظيف جميع الملفات في مجلد tmp عند بدء تشغيل البوت"""
    if os.path.exists("tmp"):
        count = 0
        for file in os.listdir("tmp"):
            file_path = os.path.join("tmp", file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    count += 1
            except Exception as e:
                print(f"[!] خطأ في حذف الملف {file_path}: {e}")
        if count > 0:
            print(f"[+] تم حذف {count} ملفات مؤقتة قديمة")
    else:
        os.makedirs("tmp")
        print("[+] تم إنشاء مجلد tmp")


def get_tiktok_options():
    """Get specialized options for TikTok downloads"""
    return {
        "cookiefile": "cookies.txt",
        "nowarnings": True,
        "quiet": True,
        "no_check_certificate": True,
        "extractor_retries": 5,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Referer": "https://www.tiktok.com/",
            "Accept-Language": "en-US,en;q=0.9",
        },
    }
