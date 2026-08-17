# ============================================================
# config.py
# FREE FIRE DIAMOND TOP-UP BOT
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# BOT
# ------------------------------------------------------------

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")

# Main Owner/Admin Telegram ID
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))

# Additional admins can be added from the dashboard/database.
# Do not put their IDs here unless you want static admins.
STATIC_ADMINS = [
    OWNER_ID,
]

# ------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------

DATABASE = "bot.db"

# ------------------------------------------------------------
# BOT SETTINGS
# ------------------------------------------------------------

BOT_NAME = "Free Fire Diamond Top-Up"

SUPPORT_USERNAME = "@Smart_Method_Owner"

# Minimum deposit
MIN_DEPOSIT = 10.00

# Minimum withdrawal if withdrawal feature is enabled later
MIN_WITHDRAW = 50.00

# Referral reward
REFERRAL_REWARD = 5.00

# ------------------------------------------------------------
# ORDER SETTINGS
# ------------------------------------------------------------

# Orders are MANUAL.
# No Free Fire API / automatic delivery will be used.

ORDER_AUTO_CANCEL_MINUTES = 60

# ------------------------------------------------------------
# PAGINATION
# ------------------------------------------------------------

USERS_PER_PAGE = 10
OFFERS_PER_PAGE = 10
ORDERS_PER_PAGE = 10
DEPOSITS_PER_PAGE = 10

# ------------------------------------------------------------
# TIMEZONE
# ------------------------------------------------------------

TIMEZONE = "Asia/Dhaka"
