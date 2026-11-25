import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get config from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/yourchannel")
CHANNEL_NAME = os.environ.get("CHANNEL_NAME", "My Channel")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send channel link when /start is issued."""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton(f"📢 Join {CHANNEL_NAME}", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"👋 Hello {user.first_name}!\n\n"
        f"Thanks for reaching out. Click the button below to join our channel:\n\n"
        f"👉 {CHANNEL_LINK}"
    )
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        disable_web_page_preview=False
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    await update.message.reply_text(
        "Use /start to get the link to our channel!"
    )

def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set!")
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Run the bot (polling mode)
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
