# ============================================================
# admin.py
# FREE FIRE DIAMOND TOP-UP BOT
# ADMIN MANAGEMENT
# ============================================================

from datetime import datetime

from database import (
    get_db,
    get_user,
    is_admin,
    get_admin_role,
    change_balance,
    ban_user,
    unban_user,
    get_setting,
    set_setting,
)


# ============================================================
# ADMIN ACCESS
# ============================================================

async def check_admin(user_id: int):
    """Return True if user is an admin."""

    return await is_admin(user_id)


async def check_owner(user_id: int):
    """Only owner can perform sensitive admin actions."""

    role = await get_admin_role(user_id)

    return role == "owner"


# ============================================================
# ADMIN DASHBOARD STATISTICS
# ============================================================

async def get_dashboard_stats():

    db = await get_db()

    # Total users
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM users
    """)
    row = await cursor.fetchone()
    total_users = int(row["total"])

    # Active users
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM users
        WHERE is_banned = 0
    """)
    row = await cursor.fetchone()
    active_users = int(row["total"])

    # Banned users
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM users
        WHERE is_banned = 1
    """)
    row = await cursor.fetchone()
    banned_users = int(row["total"])

    # Total deposits
    cursor = await db.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM deposits
        WHERE status = 'approved'
    """)
    row = await cursor.fetchone()
    total_deposits = float(row["total"])

    # Total sales
    cursor = await db.execute("""
        SELECT COALESCE(SUM(price), 0) AS total
        FROM orders
        WHERE status = 'completed'
    """)
    row = await cursor.fetchone()
    total_sales = float(row["total"])

    # Total orders
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM orders
    """)
    row = await cursor.fetchone()
    total_orders = int(row["total"])

    # Pending orders
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM orders
        WHERE status IN ('pending', 'processing')
    """)
    row = await cursor.fetchone()
    pending_orders = int(row["total"])

    # Completed orders
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM orders
        WHERE status = 'completed'
    """)
    row = await cursor.fetchone()
    completed_orders = int(row["total"])

    # Pending deposits
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM deposits
        WHERE status = 'pending'
    """)
    row = await cursor.fetchone()
    pending_deposits = int(row["total"])

    # Active offers
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM offers
        WHERE is_active = 1
    """)
    row = await cursor.fetchone()
    active_offers = int(row["total"])

    await db.close()

    return {
        "users": total_users,
        "active": active_users,
        "banned": banned_users,
        "deposits": total_deposits,
        "sales": total_sales,
        "orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "pending_deposits": pending_deposits,
        "offers": active_offers,
    }


# ============================================================
# OFFER MANAGEMENT
# ============================================================

async def add_offer(
    name: str,
    diamonds: str,
    price: float,
    button_name: str,
    description: str = "",
    delivery_time: str = "1–5 Minutes",
    image_file_id: str | None = None,
):

    name = name.strip()
    diamonds = diamonds.strip()
    button_name = button_name.strip()
    description = description.strip()

    price = float(price)

    if not name:
        return False, "INVALID_NAME", None

    if not diamonds:
        return False, "INVALID_DIAMONDS", None

    if price <= 0:
        return False, "INVALID_PRICE", None

    if not button_name:
        return False, "INVALID_BUTTON", None

    db = await get_db()

    now = datetime.now().isoformat()

    cursor = await db.execute("""
        INSERT INTO offers
        (
            name,
            diamonds,
            price,
            button_name,
            description,
            delivery_time,
            image_file_id,
            is_active,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
    """, (
        name,
        diamonds,
        price,
        button_name,
        description,
        delivery_time,
        image_file_id,
        now,
        now,
    ))

    offer_id = cursor.lastrowid

    await db.commit()

    cursor = await db.execute("""
        SELECT *
        FROM offers
        WHERE id = ?
    """, (offer_id,))

    offer = await cursor.fetchone()

    await db.close()

    return True, "CREATED", offer


# ============================================================
# GET OFFER
# ============================================================

async def get_offer(offer_id: int):

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM offers
        WHERE id = ?
    """, (offer_id,))

    offer = await cursor.fetchone()

    await db.close()

    return offer


# ============================================================
# GET ALL OFFERS
# ============================================================

async def get_all_offers(
    active_only: bool = False,
    limit: int = 50,
    offset: int = 0,
):

    db = await get_db()

    if active_only:

        cursor = await db.execute("""
            SELECT *
            FROM offers
            WHERE is_active = 1
            ORDER BY id ASC
            LIMIT ? OFFSET ?
        """, (
            limit,
            offset,
        ))

    else:

        cursor = await db.execute("""
            SELECT *
            FROM offers
            ORDER BY id ASC
            LIMIT ? OFFSET ?
        """, (
            limit,
            offset,
        ))

    offers = await cursor.fetchall()

    await db.close()

    return offers


# ============================================================
# EDIT OFFER
# ============================================================

async def edit_offer(
    offer_id: int,
    name: str | None = None,
    diamonds: str | None = None,
    price: float | None = None,
    button_name: str | None = None,
    description: str | None = None,
    delivery_time: str | None = None,
    image_file_id: str | None = None,
):

    offer = await get_offer(offer_id)

    if not offer:
        return False, "OFFER_NOT_FOUND"

    # Keep old values if not supplied
    new_name = offer["name"] if name is None else name.strip()
    new_diamonds = (
        offer["diamonds"]
        if diamonds is None
        else diamonds.strip()
    )
    new_price = (
        float(offer["price"])
        if price is None
        else float(price)
    )
    new_button = (
        offer["button_name"]
        if button_name is None
        else button_name.strip()
    )
    new_description = (
        offer["description"] or ""
        if description is None
        else description.strip()
    )
    new_delivery = (
        offer["delivery_time"] or "1–5 Minutes"
        if delivery_time is None
        else delivery_time.strip()
    )
    new_image = (
        offer["image_file_id"]
        if image_file_id is None
        else image_file_id
    )

    if not new_name:
        return False, "INVALID_NAME"

    if not new_diamonds:
        return False, "INVALID_DIAMONDS"

    if new_price <= 0:
        return False, "INVALID_PRICE"

    if not new_button:
        return False, "INVALID_BUTTON"

    db = await get_db()

    await db.execute("""
        UPDATE offers
        SET
            name = ?,
            diamonds = ?,
            price = ?,
            button_name = ?,
            description = ?,
            delivery_time = ?,
            image_file_id = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        new_name,
        new_diamonds,
        new_price,
        new_button,
        new_description,
        new_delivery,
        new_image,
        datetime.now().isoformat(),
        offer_id,
    ))

    await db.commit()

    cursor = await db.execute("""
        SELECT *
        FROM offers
        WHERE id = ?
    """, (offer_id,))

    updated_offer = await cursor.fetchone()

    await db.close()

    return True, updated_offer


# ============================================================
# DELETE OFFER
# ============================================================

async def delete_offer(offer_id: int):

    offer = await get_offer(offer_id)

    if not offer:
        return False, "OFFER_NOT_FOUND"

    db = await get_db()

    # Do not delete historical order data.
    # Just disable the offer.
    await db.execute("""
        UPDATE offers
        SET
            is_active = 0,
            updated_at = ?
        WHERE id = ?
    """, (
        datetime.now().isoformat(),
        offer_id,
    ))

    await db.commit()
    await db.close()

    return True, "DELETED"


# ============================================================
# ENABLE / DISABLE OFFER
# ============================================================

async def toggle_offer(offer_id: int):

    offer = await get_offer(offer_id)

    if not offer:
        return False, "OFFER_NOT_FOUND", None

    new_status = 0 if offer["is_active"] else 1

    db = await get_db()

    await db.execute("""
        UPDATE offers
        SET
            is_active = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        new_status,
        datetime.now().isoformat(),
        offer_id,
    ))

    await db.commit()

    cursor = await db.execute("""
        SELECT *
        FROM offers
        WHERE id = ?
    """, (offer_id,))

    updated = await cursor.fetchone()

    await db.close()

    return True, "ENABLED" if new_status else "DISABLED", updated


# ============================================================
# USER MANAGEMENT
# ============================================================

async def search_users(
    query: str,
    limit: int = 20,
):

    query = query.strip()

    db = await get_db()

    # Search by Telegram ID, username or name.
    cursor = await db.execute("""
        SELECT *
        FROM users
        WHERE
            CAST(user_id AS TEXT) LIKE ?
            OR username LIKE ?
            OR first_name LIKE ?
        ORDER BY user_id DESC
        LIMIT ?
    """, (
        f"%{query}%",
        f"%{query}%",
        f"%{query}%",
        limit,
    ))

    users = await cursor.fetchall()

    await db.close()

    return users


# ============================================================
# GET ALL USERS
# ============================================================

async def get_all_users(
    limit: int = 50,
    offset: int = 0,
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM users
        ORDER BY user_id DESC
        LIMIT ? OFFSET ?
    """, (
        limit,
        offset,
    ))

    users = await cursor.fetchall()

    await db.close()

    return users


# ============================================================
# GET BANNED USERS
# ============================================================

async def get_banned_users(
    limit: int = 50,
    offset: int = 0,
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM users
        WHERE is_banned = 1
        ORDER BY user_id DESC
        LIMIT ? OFFSET ?
    """, (
        limit,
        offset,
    ))

    users = await cursor.fetchall()

    await db.close()

    return users


# ============================================================
# GET USER FULL DETAILS
# ============================================================

async def get_user_details(user_id: int):

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    user = await cursor.fetchone()

    if not user:
        await db.close()
        return None

    # Orders
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM orders
        WHERE user_id = ?
    """, (user_id,))

    orders = await cursor.fetchone()

    # Deposits
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM deposits
        WHERE
            user_id = ?
            AND status = 'approved'
    """, (user_id,))

    deposits = await cursor.fetchone()

    # Referral count
    cursor = await db.execute("""
        SELECT COUNT(*) AS total
        FROM referrals
        WHERE referrer_id = ?
    """, (user_id,))

    referrals = await cursor.fetchone()

    await db.close()

    return {
        "user": user,
        "orders": int(orders["total"]),
        "deposits": int(deposits["total"]),
        "referrals": int(referrals["total"]),
    }


# ============================================================
# ADD USER BALANCE
# ============================================================

async def admin_add_balance(
    admin_id: int,
    user_id: int,
    amount: float,
    description: str = "Manual balance added by admin",
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN"

    amount = float(amount)

    if amount <= 0:
        return False, "INVALID_AMOUNT"

    user = await get_user(user_id)

    if not user:
        return False, "USER_NOT_FOUND"

    success, result = await change_balance(
        user_id=user_id,
        amount=amount,
        transaction_type="admin_credit",
        description=description,
        admin_id=admin_id,
    )

    if not success:
        return False, result

    # Admin log
    await add_admin_log(
        admin_id=admin_id,
        action="add_balance",
        target_user_id=user_id,
        details=f"Added ৳{amount:.2f}",
    )

    return True, result


# ============================================================
# REMOVE USER BALANCE
# ============================================================

async def admin_remove_balance(
    admin_id: int,
    user_id: int,
    amount: float,
    description: str = "Manual balance removed by admin",
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN"

    amount = float(amount)

    if amount <= 0:
        return False, "INVALID_AMOUNT"

    user = await get_user(user_id)

    if not user:
        return False, "USER_NOT_FOUND"

    current_balance = float(user["balance"])

    if current_balance < amount:
        return False, "INSUFFICIENT_BALANCE"

    success, result = await change_balance(
        user_id=user_id,
        amount=-amount,
        transaction_type="admin_debit",
        description=description,
        admin_id=admin_id,
    )

    if not success:
        return False, result

    await add_admin_log(
        admin_id=admin_id,
        action="remove_balance",
        target_user_id=user_id,
        details=f"Removed ৳{amount:.2f}",
    )

    return True, result


# ============================================================
# BAN USER
# ============================================================

async def admin_ban_user(
    admin_id: int,
    user_id: int,
    reason: str = "",
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN"

    if await check_owner(user_id):
        return False, "CANNOT_BAN_OWNER"

    user = await get_user(user_id)

    if not user:
        return False, "USER_NOT_FOUND"

    await ban_user(
        user_id=user_id,
        reason=reason,
    )

    await add_admin_log(
        admin_id=admin_id,
        action="ban_user",
        target_user_id=user_id,
        details=f"Reason: {reason}",
    )

    return True, "BANNED"


# ============================================================
# UNBAN USER
# ============================================================

async def admin_unban_user(
    admin_id: int,
    user_id: int,
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN"

    user = await get_user(user_id)

    if not user:
        return False, "USER_NOT_FOUND"

    await unban_user(user_id)

    await add_admin_log(
        admin_id=admin_id,
        action="unban_user",
        target_user_id=user_id,
        details="User unbanned",
    )

    return True, "UNBANNED"


# ============================================================
# DEPOSIT MANAGEMENT
# ============================================================

async def get_deposit(deposit_id: int):

    db = await get_db()

    cursor = await db.execute("""
        SELECT
            deposits.*,
            users.username,
            users.first_name
        FROM deposits
        LEFT JOIN users
            ON deposits.user_id = users.user_id
        WHERE deposits.id = ?
    """, (deposit_id,))

    deposit = await cursor.fetchone()

    await db.close()

    return deposit


# ============================================================
# GET PENDING DEPOSITS
# ============================================================

async def get_pending_deposits(
    limit: int = 20,
    offset: int = 0,
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT
            deposits.*,
            users.username,
            users.first_name
        FROM deposits
        LEFT JOIN users
            ON deposits.user_id = users.user_id
        WHERE deposits.status = 'pending'
        ORDER BY deposits.id ASC
        LIMIT ? OFFSET ?
    """, (
        limit,
        offset,
    ))

    deposits = await cursor.fetchall()

    await db.close()

    return deposits


# ============================================================
# APPROVE DEPOSIT
# ============================================================

async def approve_deposit(
    admin_id: int,
    deposit_id: int,
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN", None

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM deposits
        WHERE id = ?
    """, (deposit_id,))

    deposit = await cursor.fetchone()

    if not deposit:
        await db.close()
        return False, "DEPOSIT_NOT_FOUND", None

    # Prevent double approval
    if deposit["status"] != "pending":
        await db.close()
        return False, "ALREADY_PROCESSED", deposit

    user_id = deposit["user_id"]
    amount = float(deposit["amount"])

    # --------------------------------------------------------
    # Update deposit first
    # --------------------------------------------------------

    now = datetime.now().isoformat()

    await db.execute("""
        UPDATE deposits
        SET
            status = 'approved',
            admin_id = ?,
            updated_at = ?
        WHERE id = ?
          AND status = 'pending'
    """, (
        admin_id,
        now,
        deposit_id,
    ))

    # --------------------------------------------------------
    # Add balance
    # --------------------------------------------------------

    cursor = await db.execute("""
        SELECT balance
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    user = await cursor.fetchone()

    if not user:
        await db.rollback()
        await db.close()
        return False, "USER_NOT_FOUND", None

    before = float(user["balance"])
    after = before + amount

    await db.execute("""
        UPDATE users
        SET
            balance = ?,
            total_deposit = total_deposit + ?
        WHERE user_id = ?
    """, (
        after,
        amount,
        user_id,
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
        "deposit",
        str(deposit_id),
        f"Deposit approved: {deposit['transaction_id']}",
        admin_id,
        now,
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
        "approve_deposit",
        user_id,
        str(deposit_id),
        f"Approved ৳{amount:.2f}",
        now,
    ))

    await db.commit()
    await db.close()

    return True, "APPROVED", {
        "deposit": deposit,
        "amount": amount,
        "balance": after,
    }


# ============================================================
# REJECT DEPOSIT
# ============================================================

async def reject_deposit(
    admin_id: int,
    deposit_id: int,
    reason: str = "",
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN", None

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM deposits
        WHERE id = ?
    """, (deposit_id,))

    deposit = await cursor.fetchone()

    if not deposit:
        await db.close()
        return False, "DEPOSIT_NOT_FOUND", None

    if deposit["status"] != "pending":
        await db.close()
        return False, "ALREADY_PROCESSED", deposit

    now = datetime.now().isoformat()

    await db.execute("""
        UPDATE deposits
        SET
            status = 'rejected',
            admin_id = ?,
            admin_note = ?,
            updated_at = ?
        WHERE id = ?
          AND status = 'pending'
    """, (
        admin_id,
        reason,
        now,
        deposit_id,
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
        "reject_deposit",
        deposit["user_id"],
        str(deposit_id),
        f"Reason: {reason}",
        now,
    ))

    await db.commit()
    await db.close()

    return True, "REJECTED", {
        "deposit": deposit,
        "reason": reason,
    }


# ============================================================
# ADMIN MANAGEMENT
# ============================================================

async def get_admins():

    db = await get_db()

    cursor = await db.execute("""
        SELECT
            admins.*,
            users.username,
            users.first_name
        FROM admins
        LEFT JOIN users
            ON admins.user_id = users.user_id
        ORDER BY
            CASE
                WHEN admins.role = 'owner'
                THEN 0
                ELSE 1
            END,
            admins.user_id ASC
    """)

    admins = await cursor.fetchall()

    await db.close()

    return admins


# ============================================================
# ADD ADMIN
# ============================================================

async def add_admin(
    owner_id: int,
    user_id: int,
    role: str = "admin",
):

    if not await check_owner(owner_id):
        return False, "OWNER_ONLY"

    if role not in (
        "admin",
        "support",
        "deposit_manager",
        "order_manager",
    ):
        return False, "INVALID_ROLE"

    user = await get_user(user_id)

    if not user:
        return False, "USER_NOT_FOUND"

    if await is_admin(user_id):
        return False, "ALREADY_ADMIN"

    db = await get_db()

    await db.execute("""
        INSERT INTO admins
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
        owner_id,
        datetime.now().isoformat(),
    ))

    await db.commit()
    await db.close()

    await add_admin_log(
        admin_id=owner_id,
        action="add_admin",
        target_user_id=user_id,
        details=f"Role: {role}",
    )

    return True, "ADMIN_ADDED"


# ============================================================
# REMOVE ADMIN
# ============================================================

async def remove_admin(
    owner_id: int,
    user_id: int,
):

    if not await check_owner(owner_id):
        return False, "OWNER_ONLY"

    role = await get_admin_role(user_id)

    if role is None:
        return False, "NOT_ADMIN"

    if role == "owner":
        return False, "CANNOT_REMOVE_OWNER"

    db = await get_db()

    await db.execute("""
        DELETE FROM admins
        WHERE user_id = ?
          AND role != 'owner'
    """, (user_id,))

    await db.commit()
    await db.close()

    await add_admin_log(
        admin_id=owner_id,
        action="remove_admin",
        target_user_id=user_id,
        details="Admin removed",
    )

    return True, "ADMIN_REMOVED"


# ============================================================
# ADMIN LOGS
# ============================================================

async def add_admin_log(
    admin_id: int,
    action: str,
    target_user_id: int | None = None,
    reference_id: str | None = None,
    details: str = "",
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
        datetime.now().isoformat(),
    ))

    await db.commit()
    await db.close()


async def get_admin_logs(
    limit: int = 50,
    offset: int = 0,
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM admin_logs
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (
        limit,
        offset,
    ))

    logs = await cursor.fetchall()

    await db.close()

    return logs


# ============================================================
# SETTINGS
# ============================================================

async def update_payment_setting(
    admin_id: int,
    method: str,
    value: str,
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN"

    method = method.lower().strip()

    allowed = {
        "bkash": "bkash_number",
        "nagad": "nagad_number",
        "rocket": "rocket_number",
        "binance": "binance_address",
    }

    if method not in allowed:
        return False, "INVALID_METHOD"

    await set_setting(
        allowed[method],
        value.strip(),
    )

    await add_admin_log(
        admin_id=admin_id,
        action="update_payment_setting",
        details=f"{method} payment setting updated",
    )

    return True, "UPDATED"


# ============================================================
# GET PAYMENT SETTINGS
# ============================================================

async def get_payment_settings():

    return {
        "bkash": await get_setting(
            "bkash_number",
            "",
        ),
        "nagad": await get_setting(
            "nagad_number",
            "",
        ),
        "rocket": await get_setting(
            "rocket_number",
            "",
        ),
        "binance": await get_setting(
            "binance_address",
            "",
        ),
    }


# ============================================================
# MAINTENANCE MODE
# ============================================================

async def set_maintenance_mode(
    admin_id: int,
    enabled: bool,
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN"

    value = "1" if enabled else "0"

    await set_setting(
        "maintenance_mode",
        value,
    )

    await add_admin_log(
        admin_id=admin_id,
        action="maintenance_mode",
        details=f"Enabled: {enabled}",
    )

    return True, value


async def maintenance_enabled():

    value = await get_setting(
        "maintenance_mode",
        "0",
    )

    return value == "1"


# ============================================================
# NEW OFFER NOTIFICATION SETTING
# ============================================================

async def set_offer_notifications(
    admin_id: int,
    enabled: bool,
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN"

    value = "1" if enabled else "0"

    await set_setting(
        "new_offer_notification",
        value,
    )

    await add_admin_log(
        admin_id=admin_id,
        action="offer_notification_setting",
        details=f"Enabled: {enabled}",
    )

    return True, value


async def offer_notifications_enabled():

    value = await get_setting(
        "new_offer_notification",
        "1",
    )

    return value == "1"


# ============================================================
# REFERRAL SETTINGS
# ============================================================

async def set_referral_settings(
    admin_id: int,
    enabled: bool | None = None,
    reward: float | None = None,
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN"

    if enabled is not None:

        await set_setting(
            "referral_enabled",
            "1" if enabled else "0",
        )

    if reward is not None:

        reward = float(reward)

        if reward < 0:
            return False, "INVALID_REWARD"

        await set_setting(
            "referral_reward",
            str(reward),
        )

    await add_admin_log(
        admin_id=admin_id,
        action="referral_settings",
        details=(
            f"enabled={enabled}, "
            f"reward={reward}"
        ),
    )

    return True, "UPDATED"


async def referral_enabled():

    value = await get_setting(
        "referral_enabled",
        "1",
    )

    return value == "1"


async def referral_reward():

    value = await get_setting(
        "referral_reward",
        "5",
    )

    try:
        return float(value)
    except (TypeError, ValueError):
        return 5.0


# ============================================================
# MINIMUM DEPOSIT
# ============================================================

async def set_minimum_deposit(
    admin_id: int,
    amount: float,
):

    if not await is_admin(admin_id):
        return False, "NOT_ADMIN"

    amount = float(amount)

    if amount <= 0:
        return False, "INVALID_AMOUNT"

    await set_setting(
        "min_deposit",
        str(amount),
    )

    await add_admin_log(
        admin_id=admin_id,
        action="minimum_deposit",
        details=f"Minimum deposit: ৳{amount:.2f}",
    )

    return True, amount


async def get_minimum_deposit():

    value = await get_setting(
        "min_deposit",
        "10",
    )

    try:
        return float(value)
    except (TypeError, ValueError):
        return 10.0


# ============================================================
# BROADCAST USER LISTS
# ============================================================

async def get_broadcast_users(
    target: str = "all",
):

    db = await get_db()

    target = target.lower().strip()

    if target == "all":

        cursor = await db.execute("""
            SELECT user_id
            FROM users
            WHERE is_banned = 0
            ORDER BY user_id ASC
        """)

    elif target == "active":

        cursor = await db.execute("""
            SELECT user_id
            FROM users
            WHERE
                is_banned = 0
                AND last_seen IS NOT NULL
            ORDER BY user_id ASC
        """)

    elif target == "depositors":

        cursor = await db.execute("""
            SELECT DISTINCT user_id
            FROM deposits
            WHERE status = 'approved'
            ORDER BY user_id ASC
        """)

    elif target == "buyers":

        cursor = await db.execute("""
            SELECT DISTINCT user_id
            FROM orders
            WHERE status = 'completed'
            ORDER BY user_id ASC
        """)

    else:

        await db.close()
        return []

    rows = await cursor.fetchall()

    await db.close()

    return [
        int(row["user_id"])
        for row in rows
    ]


# ============================================================
# BROADCAST LOG
# ============================================================

async def save_broadcast(
    admin_id: int,
    message: str,
    target: str,
    sent_count: int,
    failed_count: int,
):

    db = await get_db()

    await db.execute("""
        INSERT INTO broadcasts
        (
            admin_id,
            message,
            target,
            sent_count,
            failed_count,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        admin_id,
        message,
        target,
        sent_count,
        failed_count,
        datetime.now().isoformat(),
    ))

    await db.commit()
    await db.close()


# ============================================================
# BROADCAST HISTORY
# ============================================================

async def get_broadcast_history(
    limit: int = 20,
):

    db = await get_db()

    cursor = await db.execute("""
        SELECT *
        FROM broadcasts
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = await cursor.fetchall()

    await db.close()

    return rows


# ============================================================
# ADMIN ROLE PERMISSIONS
# ============================================================

ROLE_PERMISSIONS = {

    "owner": {
        "dashboard",
        "offers",
        "users",
        "deposits",
        "orders",
        "broadcast",
        "promo",
        "settings",
        "admins",
        "logs",
    },

    "admin": {
        "dashboard",
        "offers",
        "users",
        "deposits",
        "orders",
        "broadcast",
        "promo",
        "settings",
    },

    "support": {
        "dashboard",
        "users",
        "orders",
    },

    "deposit_manager": {
        "dashboard",
        "users",
        "deposits",
    },

    "order_manager": {
        "dashboard",
        "users",
        "orders",
    },
}


async def has_permission(
    user_id: int,
    permission: str,
):

    role = await get_admin_role(user_id)

    if not role:
        return False

    permissions = ROLE_PERMISSIONS.get(
        role,
        set(),
    )

    return permission in permissions
