# ============================================================
# orders.py
# FREE FIRE DIAMOND TOP-UP BOT
# MANUAL ORDER MANAGEMENT
# ============================================================

import secrets
from datetime import datetime

from database import (
    get_db,
    get_user,
    get_balance,
    change_balance,
)


# ============================================================
# ORDER CODE
# ============================================================

def generate_order_code():
    """
    Generate a unique order code.
    Example: FF8A31D92
    """

    return "FF" + secrets.token_hex(5).upper()


# ============================================================
# CREATE ORDER
# ============================================================

async def create_order(
    user_id: int,
    offer_id: int,
    offer_name: str,
    diamonds: str,
    price: float,
    uid: str,
    player_name: str = ""
):
    """
    Create a new manual order.

    Flow:
    1. Check user
    2. Check balance
    3. Deduct balance
    4. Create pending order
    """

    user = await get_user(user_id)

    if not user:
        return False, "USER_NOT_FOUND", None

    if user["is_banned"]:
        return False, "USER_BANNED", None

    balance = await get_balance(user_id)

    price = float(price)

    if balance < price:
        return False, "INSUFFICIENT_BALANCE", {
            "balance": balance,
            "required": price
        }

    # --------------------------------------------------------
    # Generate unique order code
    # --------------------------------------------------------

    db = await get_db()

    order_code = None

    for _ in range(10):

        candidate = generate_order_code()

        cursor = await db.execute("""
            SELECT id
            FROM orders
            WHERE order_code = ?
        """, (candidate,))

        exists = await cursor.fetchone()

        if not exists:
            order_code = candidate
            break

    if not order_code:
        await db.close()
        return False, "ORDER_CODE_ERROR", None

    now = datetime.now().isoformat()

    # --------------------------------------------------------
    # Deduct balance
    # --------------------------------------------------------

    before = balance
    after = balance - price

    await db.execute("""
        UPDATE users
        SET
            balance = ?,
            total_spent = total_spent + ?
        WHERE user_id = ?
    """, (
        after,
        price,
        user_id
    ))

    # --------------------------------------------------------
    # Balance transaction
    # --------------------------------------------------------

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
        -price,
        before,
        after,
        "order",
        order_code,
        f"Diamond order: {offer_name}",
        None,
        now
    ))

    # --------------------------------------------------------
    # Create order
    # --------------------------------------------------------

    cursor = await db.execute("""
        INSERT INTO orders
        (
            order_code,
            user_id,
            offer_id,
            offer_name,
            diamonds,
            price,
            uid,
            player_name,
            status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_code,
        user_id,
        offer_id,
        offer_name,
        diamonds,
        price,
        uid,
        player_name,
        "pending",
        now,
        now
    ))

    order_id = cursor.lastrowid

    await db.commit()
    await db.close()

    return True, "ORDER_CREATED", {
        "id": order_id,
        "order_code": order_code,
        "balance": after
    }


# ============================================================
# GET ORDER
# ============================================================

async def get_order(order_id: int):

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM orders
        WHERE id = ?
    """, (order_id,))

    order = await cursor.fetchone()

    await db.close()

    return order


# ============================================================
# GET ORDER BY CODE
# ============================================================

async def get_order_by_code(order_code: str):

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM orders
        WHERE order_code = ?
    """, (order_code,))

    order = await cursor.fetchone()

    await db.close()

    return order


# ============================================================
# GET USER ORDERS
# ============================================================

async def get_user_orders(
    user_id: int,
    limit: int = 10,
    offset: int = 0
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (
        user_id,
        limit,
        offset
    ))

    orders = await cursor.fetchall()

    await db.close()

    return orders


# ============================================================
# GET PENDING ORDERS
# ============================================================

async def get_pending_orders(
    limit: int = 10,
    offset: int = 0
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT
            orders.*,
            users.username,
            users.first_name
        FROM orders
        LEFT JOIN users
            ON orders.user_id = users.user_id
        WHERE orders.status = 'pending'
        ORDER BY orders.id ASC
        LIMIT ? OFFSET ?
    """, (
        limit,
        offset
    ))

    orders = await cursor.fetchall()

    await db.close()

    return orders


# ============================================================
# GET PROCESSING ORDERS
# ============================================================

async def get_processing_orders(
    limit: int = 10,
    offset: int = 0
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT
            orders.*,
            users.username,
            users.first_name
        FROM orders
        LEFT JOIN users
            ON orders.user_id = users.user_id
        WHERE orders.status = 'processing'
        ORDER BY orders.id ASC
        LIMIT ? OFFSET ?
    """, (
        limit,
        offset
    ))

    orders = await cursor.fetchall()

    await db.close()

    return orders


# ============================================================
# GET COMPLETED ORDERS
# ============================================================

async def get_completed_orders(
    limit: int = 10,
    offset: int = 0
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT
            orders.*,
            users.username,
            users.first_name
        FROM orders
        LEFT JOIN users
            ON orders.user_id = users.user_id
        WHERE orders.status = 'completed'
        ORDER BY orders.id DESC
        LIMIT ? OFFSET ?
    """, (
        limit,
        offset
    ))

    orders = await cursor.fetchall()

    await db.close()

    return orders


# ============================================================
# GET CANCELLED ORDERS
# ============================================================

async def get_cancelled_orders(
    limit: int = 10,
    offset: int = 0
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT
            orders.*,
            users.username,
            users.first_name
        FROM orders
        LEFT JOIN users
            ON orders.user_id = users.user_id
        WHERE orders.status = 'cancelled'
        ORDER BY orders.id DESC
        LIMIT ? OFFSET ?
    """, (
        limit,
        offset
    ))

    orders = await cursor.fetchall()

    await db.close()

    return orders


# ============================================================
# PROCESS ORDER
# ============================================================

async def process_order(
    order_id: int,
    admin_id: int
):
    """
    Change pending order -> processing.
    """

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM orders
        WHERE id = ?
    """, (order_id,))

    order = await cursor.fetchone()

    if not order:
        await db.close()
        return False, "ORDER_NOT_FOUND"

    if order["status"] != "pending":
        await db.close()
        return False, "INVALID_STATUS"

    now = datetime.now().isoformat()

    await db.execute("""
        UPDATE orders
        SET
            status = 'processing',
            admin_id = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        admin_id,
        now,
        order_id
    ))

    await db.commit()
    await db.close()

    return True, "PROCESSING"


# ============================================================
# COMPLETE ORDER
# ============================================================

async def complete_order(
    order_id: int,
    admin_id: int,
    admin_note: str = ""
):
    """
    Mark manual order as completed.

    Important:
    Balance was already deducted when order was created.
    Therefore completing an order does NOT deduct balance again.
    """

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM orders
        WHERE id = ?
    """, (order_id,))

    order = await cursor.fetchone()

    if not order:
        await db.close()
        return False, "ORDER_NOT_FOUND"

    if order["status"] not in ("pending", "processing"):
        await db.close()
        return False, "INVALID_STATUS"

    now = datetime.now().isoformat()

    await db.execute("""
        UPDATE orders
        SET
            status = 'completed',
            admin_id = ?,
            admin_note = ?,
            updated_at = ?,
            completed_at = ?
        WHERE id = ?
    """, (
        admin_id,
        admin_note,
        now,
        now,
        order_id
    ))

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
        "complete_order",
        order["user_id"],
        order["order_code"],
        f"Order completed manually: {order['offer_name']}",
        now
    ))

    await db.commit()
    await db.close()

    return True, "COMPLETED"


# ============================================================
# CANCEL ORDER
# ============================================================

async def cancel_order(
    order_id: int,
    admin_id: int,
    reason: str = ""
):
    """
    Cancel an order and refund the user's balance.

    This function is protected against double refunds.
    """

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM orders
        WHERE id = ?
    """, (order_id,))

    order = await cursor.fetchone()

    if not order:
        await db.close()
        return False, "ORDER_NOT_FOUND"

    if order["status"] not in ("pending", "processing"):
        await db.close()
        return False, "INVALID_STATUS"

    user_id = order["user_id"]
    amount = float(order["price"])

    # --------------------------------------------------------
    # Get current balance
    # --------------------------------------------------------

    cursor = await db.execute("""
        SELECT balance
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    user = await cursor.fetchone()

    if not user:
        await db.close()
        return False, "USER_NOT_FOUND"

    before = float(user["balance"])
    after = before + amount

    now = datetime.now().isoformat()

    # --------------------------------------------------------
    # Refund
    # --------------------------------------------------------

    await db.execute("""
        UPDATE users
        SET
            balance = ?,
            total_spent =
                CASE
                    WHEN total_spent >= ?
                    THEN total_spent - ?
                    ELSE 0
                END
        WHERE user_id = ?
    """, (
        after,
        amount,
        amount,
        user_id
    ))

    # --------------------------------------------------------
    # Balance transaction
    # --------------------------------------------------------

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
        "order_refund",
        order["order_code"],
        f"Refund for cancelled order #{order['order_code']}",
        admin_id,
        now
    ))

    # --------------------------------------------------------
    # Update order
    # --------------------------------------------------------

    await db.execute("""
        UPDATE orders
        SET
            status = 'cancelled',
            admin_id = ?,
            admin_note = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        admin_id,
        reason,
        now,
        order_id
    ))

    # --------------------------------------------------------
    # Admin log
    # --------------------------------------------------------

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
        "cancel_order",
        user_id,
        order["order_code"],
        f"Order cancelled and ৳{amount:.2f} refunded. Reason: {reason}",
        now
    ))

    await db.commit()
    await db.close()

    return True, {
        "status": "CANCELLED",
        "refund": amount,
        "balance": after
    }


# ============================================================
# UPDATE PLAYER NAME
# ============================================================

async def update_player_name(
    order_id: int,
    player_name: str
):

    db = await get_db()

    await db.execute("""
        UPDATE orders
        SET
            player_name = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        player_name,
        datetime.now().isoformat(),
        order_id
    ))

    await db.commit()
    await db.close()

    return True


# ============================================================
# ADD ADMIN NOTE
# ============================================================

async def add_order_note(
    order_id: int,
    admin_id: int,
    note: str
):

    db = await get_db()

    await db.execute("""
        UPDATE orders
        SET
            admin_note = ?,
            admin_id = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        note,
        admin_id,
        datetime.now().isoformat(),
        order_id
    ))

    await db.commit()
    await db.close()

    return True


# ============================================================
# SEARCH ORDER
# ============================================================

async def search_order(query: str):

    db = await get_db()

    query = query.strip()

    # Search by order code
    cursor = await db.execute("""
        SELECT
            orders.*,
            users.username,
            users.first_name
        FROM orders
        LEFT JOIN users
            ON orders.user_id = users.user_id
        WHERE
            orders.order_code LIKE ?
            OR orders.uid LIKE ?
        ORDER BY orders.id DESC
        LIMIT 20
    """, (
        f"%{query}%",
        f"%{query}%"
    ))

    orders = await cursor.fetchall()

    await db.close()

    return orders


# ============================================================
# COUNT USER ORDERS
# ============================================================

async def count_user_orders(user_id: int):

    db = await get_db()

    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM orders
        WHERE user_id = ?
    """, (user_id,))

    row = await cursor.fetchone()

    await db.close()

    return int(row["total"])


# ============================================================
# COUNT ORDERS
# ============================================================

async def count_orders(status: str | None = None):

    db = await get_db()

    if status:

        cursor = await db.execute("""
            SELECT COUNT(*) AS total
            FROM orders
            WHERE status = ?
        """, (status,))

    else:

        cursor = await db.execute("""
            SELECT COUNT(*) AS total
            FROM orders
        """)

    row = await cursor.fetchone()

    await db.close()

    return int(row["total"])


# ============================================================
# TOTAL SALES
# ============================================================

async def total_sales():

    db = await get_db()

    cursor = await db.execute("""
        SELECT COALESCE(SUM(price), 0) AS total
        FROM orders
        WHERE status = 'completed'
    """)

    row = await cursor.fetchone()

    await db.close()

    return float(row["total"])


# ============================================================
# USER TOTAL SPENT
# ============================================================

async def user_total_spent(user_id: int):

    db = await get_db()

    cursor = await db.execute("""
        SELECT COALESCE(SUM(price), 0) AS total
        FROM orders
        WHERE
            user_id = ?
            AND status = 'completed'
    """, (user_id,))

    row = await cursor.fetchone()

    await db.close()

    return float(row["total"])


# ============================================================
# RECENT ORDERS
# ============================================================

async def recent_orders(limit: int = 10):

    db = await get_db()

    cursor = await db.execute("""
        SELECT
            orders.*,
            users.username,
            users.first_name
        FROM orders
        LEFT JOIN users
            ON orders.user_id = users.user_id
        ORDER BY orders.id DESC
        LIMIT ?
    """, (limit,))

    orders = await cursor.fetchall()

    await db.close()

    return orders
