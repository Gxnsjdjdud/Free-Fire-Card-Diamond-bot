# ============================================================
# database.py
# FREE FIRE DIAMOND TOP-UP BOT
# FULL DATABASE
# ============================================================

import aiosqlite
from datetime import datetime

from config import DATABASE, OWNER_ID


# ============================================================
# HELPERS
# ============================================================

def now():
    return datetime.now().isoformat()


# ============================================================
# DATABASE CONNECTION
# ============================================================

async def get_db():

    db = await aiosqlite.connect(DATABASE)

    db.row_factory = aiosqlite.Row

    await db.execute("PRAGMA foreign_keys = ON")

    return db


# ============================================================
# INIT DATABASE
# ============================================================

async def init_db():

    db = await get_db()

    # ========================================================
    # USERS
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            balance REAL DEFAULT 0,
            total_deposit REAL DEFAULT 0,
            total_spent REAL DEFAULT 0,
            referral_count INTEGER DEFAULT 0,
            referred_by INTEGER,
            is_banned INTEGER DEFAULT 0,
            ban_reason TEXT,
            joined_at TEXT,
            last_seen TEXT
        )
    """)

    # ========================================================
    # ADMINS
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY,
            role TEXT DEFAULT 'admin',
            added_by INTEGER,
            added_at TEXT
        )
    """)

    # ========================================================
    # OFFERS
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            diamonds TEXT NOT NULL,
            price REAL NOT NULL,
            button_name TEXT NOT NULL,
            description TEXT DEFAULT '',
            delivery_time TEXT DEFAULT 'Manual',
            image_file_id TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    # ========================================================
    # DEPOSITS
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS deposits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            method TEXT DEFAULT 'manual',
            transaction_id TEXT NOT NULL UNIQUE,
            status TEXT DEFAULT 'pending',
            admin_id INTEGER,
            admin_note TEXT,
            created_at TEXT,
            updated_at TEXT,

            FOREIGN KEY(user_id)
                REFERENCES users(user_id)
        )
    """)

    # ========================================================
    # ORDERS
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_code TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            offer_id INTEGER,
            offer_name TEXT,
            diamonds TEXT,
            price REAL DEFAULT 0,
            uid TEXT,
            player_name TEXT,
            status TEXT DEFAULT 'pending',
            admin_id INTEGER,
            admin_note TEXT,
            created_at TEXT,
            updated_at TEXT,
            completed_at TEXT,

            FOREIGN KEY(user_id)
                REFERENCES users(user_id),

            FOREIGN KEY(offer_id)
                REFERENCES offers(id)
        )
    """)

    # ========================================================
    # BALANCE TRANSACTIONS
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS balance_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            balance_before REAL NOT NULL,
            balance_after REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            reference_id TEXT,
            description TEXT,
            admin_id INTEGER,
            created_at TEXT,

            FOREIGN KEY(user_id)
                REFERENCES users(user_id)
        )
    """)

    # ========================================================
    # PROMO CODES
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS promo_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            discount REAL DEFAULT 0,
            minimum_purchase REAL DEFAULT 0,
            max_uses INTEGER DEFAULT 0,
            used_count INTEGER DEFAULT 0,
            expires_at TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT
        )
    """)

    # ========================================================
    # PROMO USAGE
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS promo_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            promo_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            used_at TEXT,

            UNIQUE(promo_id, user_id),

            FOREIGN KEY(promo_id)
                REFERENCES promo_codes(id),

            FOREIGN KEY(user_id)
                REFERENCES users(user_id)
        )
    """)

    # ========================================================
    # REFERRALS
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER NOT NULL,
            referred_id INTEGER NOT NULL UNIQUE,
            reward REAL DEFAULT 0,
            created_at TEXT,

            FOREIGN KEY(referrer_id)
                REFERENCES users(user_id),

            FOREIGN KEY(referred_id)
                REFERENCES users(user_id)
        )
    """)

    # ========================================================
    # BROADCASTS
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS broadcasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER,
            message TEXT,
            target TEXT,
            sent_count INTEGER DEFAULT 0,
            failed_count INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    # ========================================================
    # ADMIN LOGS
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER,
            action TEXT,
            target_user_id INTEGER,
            reference_id TEXT,
            details TEXT,
            created_at TEXT
        )
    """)

    # ========================================================
    # SETTINGS
    # ========================================================

    await db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # ========================================================
    # DEFAULT SETTINGS
    # ========================================================

    default_settings = {

        "maintenance_mode": "0",

        "bkash_number": "",
        "nagad_number": "",
        "rocket_number": "",
        "binance_address": "",

        "support_username": "@YourSupport",

        "new_offer_notification": "1",

        "referral_enabled": "1",
        "referral_reward": "5",

        "min_deposit": "10",

        "welcome_message":
            "🎮 Welcome to Free Fire Diamond Top-Up Bot!"
    }

    for key, value in default_settings.items():

        await db.execute("""
            INSERT OR IGNORE INTO settings
            (key, value)
            VALUES (?, ?)
        """, (
            key,
            value
        ))

    # ========================================================
    # OWNER
    # ========================================================

    current_time = now()

    await db.execute("""
        INSERT OR IGNORE INTO admins
        (
            user_id,
            role,
            added_by,
            added_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        OWNER_ID,
        "owner",
        OWNER_ID,
        current_time
    ))

    await db.commit()
    await db.close()


# ============================================================
# USER FUNCTIONS
# ============================================================

async def create_or_update_user(
    user_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
):

    db = await get_db()

    current_time = now()

    cursor = await db.execute("""
        SELECT user_id
        FROM users
        WHERE user_id = ?
    """, (
        user_id,
    ))

    existing = await cursor.fetchone()

    if existing:

        await db.execute("""
            UPDATE users
            SET
                username = ?,
                first_name = ?,
                last_name = ?,
                last_seen = ?
            WHERE user_id = ?
        """, (
            username,
            first_name,
            last_name,
            current_time,
            user_id
        ))

    else:

        await db.execute("""
            INSERT INTO users
            (
                user_id,
                username,
                first_name,
                last_name,
                balance,
                joined_at,
                last_seen
            )
            VALUES (?, ?, ?, ?, 0, ?, ?)
        """, (
            user_id,
            username,
            first_name,
            last_name,
            current_time,
            current_time
        ))

    await db.commit()
    await db.close()


# ============================================================
# CREATE USER
# Compatibility for handlers.py
# ============================================================

async def create_user(
    user_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
):

    await create_or_update_user(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )

    return await get_user(user_id)


# ============================================================
# GET USER
# ============================================================

async def get_user(user_id: int):

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM users
        WHERE user_id = ?
    """, (
        user_id,
    ))

    user = await cursor.fetchone()

    await db.close()

    return user


# ============================================================
# GET ALL USERS
# ============================================================

async def get_all_users():

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM users
        ORDER BY joined_at DESC
    """)

    users = await cursor.fetchall()

    await db.close()

    return users


# ============================================================
# GET BALANCE
# ============================================================

async def get_balance(user_id: int):

    db = await get_db()

    cursor = await db.execute("""
        SELECT balance
        FROM users
        WHERE user_id = ?
    """, (
        user_id,
    ))

    row = await cursor.fetchone()

    await db.close()

    if not row:
        return 0.0

    return float(row["balance"])


# ============================================================
# CHANGE BALANCE
# ============================================================

async def change_balance(
    user_id: int,
    amount: float,
    transaction_type: str,
    description: str = "",
    reference_id: str | None = None,
    admin_id: int | None = None
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT balance
        FROM users
        WHERE user_id = ?
    """, (
        user_id,
    ))

    row = await cursor.fetchone()

    if not row:

        await db.close()

        return False, "USER_NOT_FOUND"

    before = float(row["balance"])

    after = before + float(amount)

    if after < 0:

        await db.close()

        return False, "INSUFFICIENT_BALANCE"

    await db.execute("""
        UPDATE users
        SET balance = ?
        WHERE user_id = ?
    """, (
        after,
        user_id
    ))

    await db.execute("""
        INSERT INTO balance_transactions
        (
            user_id,
            amount,
            balance_before,
            balance_after,
            transaction_type,
            reference_id,
            description,
            admin_id,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        amount,
        before,
        after,
        transaction_type,
        reference_id,
        description,
        admin_id,
        now()
    ))

    await db.commit()
    await db.close()

    return True, after


# ============================================================
# BAN USER
# ============================================================

async def ban_user(
    user_id: int,
    reason: str = ""
):

    db = await get_db()

    await db.execute("""
        UPDATE users
        SET
            is_banned = 1,
            ban_reason = ?
        WHERE user_id = ?
    """, (
        reason,
        user_id
    ))

    await db.commit()
    await db.close()

    return True


# ============================================================
# UNBAN USER
# ============================================================

async def unban_user(
    user_id: int
):

    db = await get_db()

    await db.execute("""
        UPDATE users
        SET
            is_banned = 0,
            ban_reason = NULL
        WHERE user_id = ?
    """, (
        user_id,
    ))

    await db.commit()
    await db.close()

    return True


# ============================================================
# CHECK BAN
# ============================================================

async def is_banned(
    user_id: int
):

    user = await get_user(user_id)

    if not user:
        return False

    return bool(user["is_banned"])


# ============================================================
# SETTINGS
# ============================================================

async def get_setting(
    key: str,
    default=None
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT value
        FROM settings
        WHERE key = ?
    """, (
        key,
    ))

    row = await cursor.fetchone()

    await db.close()

    if not row:
        return default

    return row["value"]


async def set_setting(
    key: str,
    value: str
):

    db = await get_db()

    await db.execute("""
        INSERT INTO settings
        (
            key,
            value
        )
        VALUES (?, ?)

        ON CONFLICT(key)
        DO UPDATE SET
            value = excluded.value
    """, (
        key,
        value
    ))

    await db.commit()
    await db.close()

    return True


# ============================================================
# ADMIN CHECK
# ============================================================

async def is_admin(
    user_id: int
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT user_id
        FROM admins
        WHERE user_id = ?
    """, (
        user_id,
    ))

    row = await cursor.fetchone()

    await db.close()

    return row is not None


# ============================================================
# ADMIN ROLE
# ============================================================

async def get_admin_role(
    user_id: int
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT role
        FROM admins
        WHERE user_id = ?
    """, (
        user_id,
    ))

    row = await cursor.fetchone()

    await db.close()

    if not row:
        return None

    return row["role"]


# ============================================================
# ADD ADMIN
# ============================================================

async def add_admin(
    user_id: int,
    role: str = "admin",
    added_by: int | None = None
):

    db = await get_db()

    await db.execute("""
        INSERT OR REPLACE INTO admins
        (
            user_id,
            role,
            added_by,
            added_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        role,
        added_by,
        now()
    ))

    await db.commit()
    await db.close()

    return True


# ============================================================
# REMOVE ADMIN
# ============================================================

async def remove_admin(
    user_id: int
):

    if user_id == OWNER_ID:
        return False

    db = await get_db()

    await db.execute("""
        DELETE FROM admins
        WHERE user_id = ?
    """, (
        user_id,
    ))

    await db.commit()
    await db.close()

    return True


# ============================================================
# GET ADMINS
# ============================================================

async def get_admins():

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM admins
        ORDER BY added_at DESC
    """)

    admins = await cursor.fetchall()

    await db.close()

    return admins


# ============================================================
# LOG ADMIN ACTION
# ============================================================

async def add_admin_log(
    admin_id: int,
    action: str,
    target_user_id: int | None = None,
    reference_id: str | None = None,
    details: str = ""
):

    db = await get_db()

    await db.execute("""
        INSERT INTO admin_logs
        (
            admin_id,
            action,
            target_user_id,
            reference_id,
            details,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        admin_id,
        action,
        target_user_id,
        reference_id,
        details,
        now()
    ))

    await db.commit()
    await db.close()


# ============================================================
# SEARCH USERS
# ============================================================

async def search_users(
    search: str
):

    db = await get_db()

    search = str(search).strip()

    cursor = await db.execute("""
        SELECT *
        FROM users
        WHERE
            CAST(user_id AS TEXT) = ?
            OR username LIKE ?
            OR first_name LIKE ?
        ORDER BY joined_at DESC
        LIMIT 50
    """, (
        search,
        f"%{search}%",
        f"%{search}%"
    ))

    users = await cursor.fetchall()

    await db.close()

    return users


# ============================================================
# USER STATS
# ============================================================

async def get_user_stats(
    user_id: int
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT
            COUNT(*) AS total_orders,
            COALESCE(
                SUM(
                    CASE
                        WHEN status = 'completed'
                        THEN price
                        ELSE 0
                    END
                ),
                0
            ) AS total_spent
        FROM orders
        WHERE user_id = ?
    """, (
        user_id,
    ))

    row = await cursor.fetchone()

    await db.close()

    return {
        "orders": int(row["total_orders"] or 0),
        "spent": float(row["total_spent"] or 0)
    }


# ============================================================
# DASHBOARD STATS
# ============================================================

async def get_dashboard_stats():

    db = await get_db()

    async def scalar(query):

        cursor = await db.execute(query)

        row = await cursor.fetchone()

        if not row:
            return 0

        return row[0] or 0

    users = await scalar("""
        SELECT COUNT(*)
        FROM users
    """)

    active = await scalar("""
        SELECT COUNT(*)
        FROM users
        WHERE is_banned = 0
    """)

    banned = await scalar("""
        SELECT COUNT(*)
        FROM users
        WHERE is_banned = 1
    """)

    deposits = await scalar("""
        SELECT COALESCE(SUM(amount), 0)
        FROM deposits
        WHERE status = 'approved'
    """)

    sales = await scalar("""
        SELECT COALESCE(SUM(price), 0)
        FROM orders
        WHERE status = 'completed'
    """)

    orders = await scalar("""
        SELECT COUNT(*)
        FROM orders
    """)

    pending_orders = await scalar("""
        SELECT COUNT(*)
        FROM orders
        WHERE status IN ('pending', 'processing')
    """)

    completed_orders = await scalar("""
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'completed'
    """)

    pending_deposits = await scalar("""
        SELECT COUNT(*)
        FROM deposits
        WHERE status = 'pending'
    """)

    offers = await scalar("""
        SELECT COUNT(*)
        FROM offers
        WHERE is_active = 1
    """)

    await db.close()

    return {
        "users": int(users),
        "active": int(active),
        "banned": int(banned),
        "deposits": float(deposits),
        "sales": float(sales),
        "orders": int(orders),
        "pending_orders": int(pending_orders),
        "completed_orders": int(completed_orders),
        "pending_deposits": int(pending_deposits),
        "offers": int(offers),
    }
