**Social Media Video Downloader Bot**

<img alt="Telegram Bot" src="https://img.shields.io/badge/Telegram-Bot-blue">

<img alt="Python" src="https://img.shields.io/badge/Python-3.7+-green">

<img alt="GoDaddy" src="https://img.shields.io/badge/Hosting-GoDaddy-orange">

**Overview**

A powerful Telegram bot for downloading videos from major social media platforms, specifically designed to run reliably on GoDaddy shared hosting using Passenger WSGI.

**Supported Platforms**

| **Platform** | **Status**         | **Notes**                             |
| :----------- | :----------------- | :------------------------------------ |
| YouTube      | ✅ Fully supported | Most video formats                    |
| Facebook     | ✅ Fully supported | Public videos only                    |
| Instagram    | ✅ Fully supported | Posts and reels                       |
| Twitter/X    | ✅ Fully supported | Both video posts                      |
| TikTok       | ✅ Fully supported | Uses special user-agent configuration |
| Terabox      | ✅ Fully supported | Public files only                     |

**Key Features**

- **Multi-Platform Support**: One bot for all your social media video downloading needs
- **Private Access Control**: Limit usage to only you and authorized friends
- **Webhook Architecture**: Optimized for shared hosting environments with automatic recovery
- **Admin Commands**: Easily manage authorized users directly through Telegram
- **Resilient Design**: Automatically survives GoDaddy's application resets

**Setup Instructions**

**1. Create a Telegram Bot**

1. Message [@BotFather](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) on Telegram
1. Send the /newbot command
1. Choose a name and username for your bot
1. **Save the API token** provided - you'll need this for the [.env](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) file

**2. GoDaddy Python Application Setup**

1. Log into your GoDaddy account and access cPanel
1. Navigate to the **Setup Python App** section
1. Create a new Python application:
   1. Python version: 3.11 (recommended)
   1. Application root: /public_html/your-folder-name
   1. Application URL: Your domain or subdomain
   1. Application startup file: [passenger_wsgi.py](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)
   1. Application Entry Point: [application](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)

**3. Deploy Files to Server**

1. Upload all project files to your application directory via FTP or File Manager
1. Create a [.env](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) file with your bot token:

TELEGRAM_BOT_TOKEN=your_bot_token_here

1. Install required packages using GoDaddy's Python App dashboard:
   1. Go to your Python application settings
   1. Find the "Execute Python script" section
   1. Enter: python install_pip.py
   1. Click "Execute"

**4. Configure User Access**

1. Edit the [authorized_users.py](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) file:

# Change this to your actual Telegram ID

DEFAULT_ADMIN = 123456789  # ← Replace with your ID

1. To find your Telegram ID, message [@userinfobot](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)

**5. Initialize Webhook**

1. After deploying all files, visit:

https://yourdomain.com/webhook-status

1. If the webhook isn't configured, go to:

https://yourdomain.com/force\_webhook.py

**Important Configuration After GitHub Download**

After downloading this project from GitHub, you'll need to replace several placeholder values with your actual configuration:

1. **Set Your Bot Token**

   - Create a `.env` file in the root directory
   - Add your actual Telegram bot token:
     ```
     TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789
     ```
   - Replace the placeholder token with the one provided by BotFather

2. **Configure Administrator Access**

   - Edit `authorized_users.py`
   - Change the `DEFAULT_ADMIN` value to your actual Telegram ID:
     ```python
     # Replace with your actual Telegram ID - this grants you admin access
     DEFAULT_ADMIN = 123456789
     ```
   - You can get your ID by messaging @userinfobot on Telegram

3. **Update Domain References**

   - Search for and replace all instances of `your-domain.com` with your actual domain
   - Files that need domain updates:
     - `passenger_wsgi.py`
     - `core_wsgi.py`
     - `force_webhook.py`
     - `bot.py`

4. **Configure Web Interface**

   - Edit the bot link in `app.py` (around line 86):
     ```html
     <a
       href="https://t.me/YourBotUsername"
       class="bg-green-700 hover:bg-green-900 text-white font-bold py-2 px-4 rounded-full"
     >
       استخدم البوت الآن
     </a>
     ```
   - Replace `YourBotUsername` with your bot's actual username (without @)

5. **Update Server Paths**

   - Edit `.htaccess` file to match your GoDaddy hosting paths:
     ```
     PassengerAppRoot "/home/username/public_html/bot-folder"
     PassengerBaseURI "/"
     PassengerPython "/home/username/virtualenv/public_html/bot-folder/3.11/bin/python"
     ```
   - Replace `username` and `bot-folder` with your actual cPanel username and application directory

6. **Verify Configuration**
   - After making all replacements, visit your domain to check if the application loads
   - Check webhook status at `/webhook-status` to ensure proper connection to Telegram

**Technical Architecture**

The bot uses a specialized architecture to work reliably on GoDaddy shared hosting:

├── app.py              # Flask application for webhook handling

├── authorized_users.py # User access control system

├── bot.py              # Main bot implementation with GoDaddy compatibility

├── cleanup_tmp.py      # Temporary file cleanup script

├── core_wsgi.py        # Persistent implementation that survives resets

├── force_update.py     # Script to force application restart

├── force_webhook.py    # Manual webhook setup tool

├── passenger_wsgi.py   # GoDaddy's main entry point

├── utils.py            # Helper functions and downloaders

└── .env                # Environment variables

**Key Design Patterns**

1. **Webhook-Based Communication**
   1. Instead of polling (which doesn't work well on shared hosting)
   1. Telegram sends updates directly via HTTP requests
1. **Split Implementation Files**
   1. [passenger_wsgi.py](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) - May be reset by GoDaddy
   1. [core_wsgi.py](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) - Contains core logic that persists through resets
   1. [bot.py](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) - Has fallback WSGI app for GoDaddy compatibility
1. **User Authorization System**
   1. JSON-based whitelist stored in [authorized_users.json](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)
   1. Admin commands to manage users through Telegram interface
1. **Resource Management**
   1. Automatic cleanup of temporary files
   1. Error handling with detailed logging

**Bot Usage**

**Admin Commands**

| **Command**                                                                                                                                    | **Description**                           |
| :--------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------- |
| /start                                                                                                                                         | Welcome message and bot introduction      |
| /help                                                                                                                                          | Display help with all available commands  |
| [users](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) | List all authorized users (admin only)    |
| /add [user\_id]                                                                                                                                | Add a new authorized user (admin only)    |
| /remove [user\_id]                                                                                                                             | Remove a user from whitelist (admin only) |

**Downloading Videos**

1. **Send the video URL** to the bot from any supported platform
1. The bot will download and process the video
1. You'll receive the video file directly in Telegram

**Maintenance**

**Handling Server Restarts**

If the bot stops responding after a GoDaddy reset:

1. Check webhook status: https://yourdomain.com/webhook-status
1. If not connected, run: https://yourdomain.com/force\_webhook.py
1. For a complete restart: https://yourdomain.com/force\_update.py

**Cleaning Temporary Files**

Set up a cron job using GoDaddy's cPanel to run the cleanup script daily:

1. In cPanel, find **Cron Jobs**
1. Add a new job:

0 1 \* \* \* cd /home/username/public_html/your-folder && python cleanup_tmp.py

**Troubleshooting Guide**

**Decision Tree for Common Issues**

**Issue: Bot not responding to messages**

1. ✅ Check webhook status at /webhook-status
   1. If webhook URL is empty or incorrect:
      1. Run [force_webhook.py](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)
   1. If webhook is correct but still not working:
      1. Check server logs (next step)
1. ✅ Verify logs in [logs](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) directory
   1. Look for errors in [bot.log](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) or passenger.log
   1. Check if the Telegram token is loaded correctly
1. ✅ Check application status
   1. Visit your domain root to see if the application is running
   1. If not, try running [force_update.py](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)

**Issue: Downloads failing**

1. ✅ Verify yt-dlp is installed
   1. Run the installation script again if needed
   1. Check logs/bot.log for specific download errors
1. ✅ Platform-specific issues
   1. TikTok: Might need updated User-Agent (edit in [utils.py](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html))
   1. Private videos: Can't be downloaded (check URL privacy settings)
   1. Large videos: Check for timeout errors in logs

**Issue: Permission errors**

1. ✅ Check file permissions
   1. Ensure [.env](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) and log directories have correct permissions (644/755)
   1. Try re-uploading the critical files with proper permissions

**Understanding GoDaddy's Passenger WSGI**

GoDaddy shared hosting has specific requirements and limitations:

1. **Passenger WSGI Reset Behavior**
   1. After application restart, [passenger_wsgi.py](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) often reverts to default
   1. Solution: Our architecture provides fallback in [bot.py](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)
1. **Background Process Limitations**
   1. Long-running processes are terminated automatically
   1. Solution: We use webhooks instead of polling
1. **Memory & Resource Constraints**
   1. Downloads and processing must be efficient
   1. Solution: Automatic cleanup and resource management

**Security Notes**

- The bot token should be kept secret - never share your [.env](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) file
- The whitelist system ensures only authorized users can use your bot
- Webhook URLs use token validation to prevent unauthorized access

**Logs**

- Main bot logs: logs/bot.log
- Flask application logs: [flask.log](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)
- Passenger WSGI logs: logs/passenger.log
- Cleanup operation logs: logs/cleanup.log

**License**

Copyright © [Hassan Dev](vscode-file://vscode-app/c:/Program%20Files/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)
