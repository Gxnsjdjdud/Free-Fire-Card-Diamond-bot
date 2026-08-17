# ============================================================
# bot.py
# FREE FIRE DIAMOND TOP-UP BOT
# ============================================================

import os
import logging
import asyncio

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application

from database import init_db
from handlers import register_handlers


# ============================================================
# ENV
# ============================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is missing. "
        "Add BOT_TOKEN in Railway Variables."
    )


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# MAIN
# ============================================================

async def startup():

    logger.info("Initializing database...")

    await init_db()

    logger.info("Database initialized successfully.")


def main():

    logger.info(
        "Starting Free Fire Diamond Top-Up Bot..."
    )

    # Initialize database
    asyncio.run(startup())

    # Create Telegram application
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Register handlers
    register_handlers(application)

    logger.info(
        "All handlers registered successfully."
    )

    logger.info(
        "Bot is now running..."
    )

    # Start Telegram polling
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
