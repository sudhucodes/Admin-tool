import logging
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from io import BytesIO
import asyncio
from dotenv import load_dotenv
import os
import requests  # Added for sending data to Google Sheets

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Google Sheets Web App URL (replace with your deployment URL)
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwe1czYUl8AAncht8iCWiVB052BzGApEXuWfjNTvMtqVjVoddspQ1j6YVWiMhRVru1CDg/exec"

# Function to log download to Google Sheets
def log_download_to_sheets(user_id, user_name, reel_url):
    data = {
        "user_id": user_id,
        "user_name": user_name or "Anonymous",  # Handle None username
        "reel_url": reel_url
    }
    try:
        response = requests.post(WEB_APP_URL, json=data)
        if response.status_code == 200:
            logger.info("Logged to Google Sheets successfully.")
        else:
            logger.error("Failed to log download: %s", response.text)
    except Exception as e:
        logger.error("Error logging to Google Sheets: %s", str(e))

# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    welcome_message_1 = "👋 Welcome to the Instagram Reel Downloader Bot!"
    welcome_message_2 = "📥 Please send me the link to the Instagram Reel you want to download."

    await update.message.reply_text(welcome_message_1)
    await asyncio.sleep(1)  # Wait for 1 second before sending the next message
    await update.message.reply_text(welcome_message_2)

# Download reel handler
async def download_reel(update: Update, context: CallbackContext) -> None:
    reel_url = update.message.text
    user_id = update.effective_user.id  # Get the user ID
    user_name = update.effective_user.username  # Get the user name

    # Log the download request to Google Sheets
    log_download_to_sheets(user_id, user_name, reel_url)

    # Send "Please wait" message
    wait_message = await update.message.reply_text("⏳ Please wait, downloading your video...")

    video_downloaded = False  # Flag to track download success

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'outtmpl': '%(title)s.%(ext)s',
            'socket_timeout': 60,  # Set a timeout for socket operations
        }

        # Download the video and get it in an in-memory buffer
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(reel_url, download=False)  # Extract info without downloading
            video_title = info_dict.get('title', 'Video')
            video_url = info_dict['url']
            video_size = info_dict.get('filesize', None)  # Get video size

            # Check file size (max size is 50MB for Telegram)
            if video_size and video_size > 50 * 1024 * 1024:
                await update.message.reply_text("🚫 The video is too large to send via Telegram (max 50MB).")
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
                return

            # Download video to in-memory buffer
            buffer = BytesIO()
            buffer.write(ydl.urlopen(video_url).read())
            buffer.seek(0)  # Move to the start of the BytesIO buffer

            # Send the video file
            await context.bot.send_video(chat_id=update.effective_chat.id, video=buffer, caption=f'Download complete: {video_title}')
            video_downloaded = True  # Set flag to true if video sent successfully

            # Delete "please wait" message
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)

    except Exception as e:
        logger.error("Error downloading video: %s", str(e))
        await update.message.reply_text(f'❌ An error occurred: {str(e)}')

    # Only send feedback message if the video was downloaded successfully
    if video_downloaded:
        feedback_message = "✅ If you enjoyed our service, follow me on Instagram @apexdownloader!"
        await update.message.reply_text(feedback_message)

    # Delete "please wait" message if an error occurred
    if not video_downloaded and wait_message:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)

# Main function to run the bot
def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_reel))

    logger.info("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
