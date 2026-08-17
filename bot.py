# ============================================================
# bot.py
# FREE FIRE DIAMOND TOP-UP BOT
# MAIN ENTRY FILE
# ============================================================

import os
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
)

from handlers import register_handlers


# ============================================================
# ENV
# ============================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is missing. "
        "Add BOT_TOKEN to Railway Variables or .env"
    )


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    format=(
        "%(asctime)s - "
        "%(name)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# MAIN
# ============================================================

def main():

    logger.info("Starting Free Fire Diamond Bot...")

    # Create Telegram application
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Register all handlers
    register_handlers(application)

    logger.info(
        "All handlers registered successfully."
    )

    logger.info(
        "Free Fire Diamond Bot is running..."
    )

    # Start bot
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
