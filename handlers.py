# ============================================================
# handlers.py
# FREE FIRE DIAMOND TOP-UP BOT
# USER + ADMIN HANDLERS
# ============================================================

import asyncio
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from database import (
    get_user,
    create_user,
    get_balance,
    get_setting,
)

from keyboards import (
    main_menu_keyboard,
    admin_dashboard_keyboard,
    offers_keyboard,
)

from messages import (
    TEXT,
)

from admin import (
    check_admin,
    check_owner,
    get_dashboard_stats,
    get_all_offers,
    add_offer,
    edit_offer,
    delete_offer,
    toggle_offer,
    search_users,
    get_user_details,
    admin_add_balance,
    admin_remove_balance,
    admin_ban_user,
    admin_unban_user,
    get_pending_deposits,
    approve_deposit,
    reject_deposit,
    get_admins,
    add_admin,
    remove_admin,
    get_broadcast_users,
    save_broadcast,
    has_permission,
)

from orders import (
    create_order,
    get_user_orders,
    get_order,
    get_pending_orders,
    process_order,
    complete_order,
    cancel_order,
)


logger = logging.getLogger(__name__)


# ============================================================
# HELPERS
# ============================================================

def tr(key: str, default: str = ""):
    """
    Get message from messages.py.

    Supports:
        TEXT["key"]
    """

    try:
        value = TEXT.get(key)

        if isinstance(value, str):
            return value

        if isinstance(value, dict):
            return value.get("en", default)

    except Exception:
        pass

    return default


async def ensure_user(update: Update):

    tg_user = update.effective_user

    if not tg_user:
        return None

    user = await get_user(tg_user.id)

    if not user:
        try:
            await create_user(
                user_id=tg_user.id,
                username=tg_user.username or "",
                first_name=tg_user.first_name or "",
                last_name=tg_user.last_name or "",
            )

            user = await get_user(tg_user.id)

        except TypeError:
            # Compatibility fallback
            await create_user(
                tg_user.id,
                tg_user.username or "",
                tg_user.first_name or "",
            )

            user = await get_user(tg_user.id)

    return user


async def safe_edit(
    query,
    text,
    reply_markup=None,
):

    try:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

    except Exception:
        try:
            await query.message.reply_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
        except Exception:
            pass


async def send_text(
    update,
    text,
    reply_markup=None,
):

    if update.callback_query:

        await safe_edit(
            update.callback_query,
            text,
            reply_markup,
        )

    else:

        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )


# ============================================================
# START
# ============================================================

async def start_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user = await ensure_user(update)

    if not user:
        return

    context.user_data.clear()

    keyboard = main_menu_keyboard()

    balance = await get_balance(
        update.effective_user.id
    )

    text = (
        "💎 <b>FREE FIRE TOP-UP</b>\n\n"
        "Welcome! 🎮\n\n"
        f"💰 Balance: <code>৳{balance:.2f}</code>\n\n"
        "Choose an option below:"
    )

    await send_text(
        update,
        text,
        keyboard,
    )


# ============================================================
# BALANCE
# ============================================================

async def balance_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user = await ensure_user(update)

    if not user:
        return

    balance = await get_balance(
        update.effective_user.id
    )

    text = (
        "💰 <b>Your Balance</b>\n\n"
        f"Available Balance: "
        f"<code>৳{balance:.2f}</code>\n\n"
        "You can use your balance to place "
        "Free Fire top-up orders."
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Deposit",
                callback_data="deposit",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="home",
            )
        ],
    ])

    await send_text(
        update,
        text,
        keyboard,
    )


# ============================================================
# OFFERS
# ============================================================

async def offers_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user = await ensure_user(update)

    if not user:
        return

    offers = await get_all_offers(
        active_only=True
    )

    if not offers:

        text = (
            "💎 <b>Diamond Offers</b>\n\n"
            "❌ No offers are available right now."
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data="home",
                )
            ]
        ])

        await send_text(
            update,
            text,
            keyboard,
        )

        return

    keyboard = offers_keyboard(offers)

    text = (
        "💎 <b>Free Fire Diamond Offers</b>\n\n"
        "Select your preferred package:"
    )

    await send_text(
        update,
        text,
        keyboard,
    )


# ============================================================
# OFFER SELECTED
# ============================================================

async def offer_selected(
    query,
    context,
    offer_id: int,
):

    offer = await __get_offer(offer_id)

    if not offer:

        await safe_edit(
            query,
            "❌ Offer not found.",
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Back",
                        callback_data="offers",
                    )
                ]
            ]),
        )

        return

    context.user_data["selected_offer"] = offer_id

    price = float(offer["price"])

    text = (
        "💎 <b>Offer Details</b>\n\n"
        f"📦 <b>{offer['name']}</b>\n"
        f"💎 Diamonds: <b>{offer['diamonds']}</b>\n"
        f"💰 Price: <b>৳{price:.2f}</b>\n"
    )

    if offer["description"]:
        text += (
            f"\n📝 {offer['description']}\n"
        )

    text += (
        f"\n⏱ Delivery: "
        f"<b>{offer['delivery_time']}</b>\n\n"
        "Press <b>Buy Now</b> to continue."
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🛒 Buy Now",
                callback_data=f"buy:{offer_id}",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="offers",
            )
        ],
    ])

    await safe_edit(
        query,
        text,
        keyboard,
    )


async def __get_offer(offer_id):

    from admin import get_offer

    return await get_offer(offer_id)


# ============================================================
# BUY OFFER
# ============================================================

async def buy_offer(
    query,
    context,
    offer_id: int,
):

    offer = await __get_offer(offer_id)

    if not offer or not offer["is_active"]:

        await safe_edit(
            query,
            "❌ This offer is no longer available.",
        )

        return

    balance = await get_balance(
        query.from_user.id
    )

    price = float(offer["price"])

    if balance < price:

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "➕ Deposit",
                    callback_data="deposit",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data=f"offer:{offer_id}",
                )
            ],
        ])

        await safe_edit(
            query,
            (
                "❌ <b>Insufficient Balance</b>\n\n"
                f"Price: <b>৳{price:.2f}</b>\n"
                f"Your balance: "
                f"<b>৳{balance:.2f}</b>\n\n"
                "Please deposit first."
            ),
            keyboard,
        )

        return

    context.user_data["selected_offer"] = offer_id
    context.user_data["state"] = "waiting_uid"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="offers",
            )
        ]
    ])

    await safe_edit(
        query,
        (
            "🎮 <b>Enter Free Fire UID</b>\n\n"
            f"Package: <b>{offer['name']}</b>\n"
            f"Price: <b>৳{price:.2f}</b>\n\n"
            "Send your Free Fire Player UID below."
        ),
        keyboard,
    )


# ============================================================
# UID HANDLER
# ============================================================

async def handle_uid(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    uid = update.message.text.strip()

    if not uid.isdigit():

        await update.message.reply_text(
            "❌ Invalid UID.\n\n"
            "Please send numbers only."
        )

        return

    if len(uid) < 5 or len(uid) > 15:

        await update.message.reply_text(
            "❌ Invalid UID length.\n\n"
            "Please check your Free Fire UID."
        )

        return

    offer_id = context.user_data.get(
        "selected_offer"
    )

    if not offer_id:

        context.user_data.clear()

        await start_handler(
            update,
            context,
        )

        return

    offer = await __get_offer(offer_id)

    if not offer:

        context.user_data.clear()

        await update.message.reply_text(
            "❌ Offer no longer exists."
        )

        return

    context.user_data["uid"] = uid
    context.user_data["state"] = "confirm_order"

    balance = await get_balance(
        update.effective_user.id
    )

    price = float(offer["price"])

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Confirm Order",
                callback_data="confirm_order",
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="offers",
            )
        ],
    ])

    await update.message.reply_text(
        (
            "🛒 <b>Order Confirmation</b>\n\n"
            f"📦 Package: <b>{offer['name']}</b>\n"
            f"💎 Diamonds: <b>{offer['diamonds']}</b>\n"
            f"🎮 UID: <code>{uid}</code>\n"
            f"💰 Price: <b>৳{price:.2f}</b>\n"
            f"💳 Balance after order: "
            f"<b>৳{balance - price:.2f}</b>\n\n"
            "Please verify the UID before confirming."
        ),
        reply_markup=keyboard,
        parse_mode="HTML",
    )


# ============================================================
# CONFIRM ORDER
# ============================================================

async def confirm_order(
    query,
    context,
):

    user_id = query.from_user.id

    offer_id = context.user_data.get(
        "selected_offer"
    )

    uid = context.user_data.get("uid")

    if not offer_id or not uid:

        await safe_edit(
            query,
            "❌ Order session expired. Please try again.",
        )

        return

    offer = await __get_offer(offer_id)

    if not offer:

        await safe_edit(
            query,
            "❌ Offer not found.",
        )

        return

    result = await create_order(
        user_id=user_id,
        offer_id=offer_id,
        offer_name=offer["name"],
        diamonds=offer["diamonds"],
        price=float(offer["price"]),
        uid=uid,
    )

    success, status, data = result

    if not success:

        if status == "INSUFFICIENT_BALANCE":

            text = (
                "❌ <b>Insufficient Balance</b>\n\n"
                f"Required: "
                f"<b>৳{data['required']:.2f}</b>\n"
                f"Balance: "
                f"<b>৳{data['balance']:.2f}</b>"
            )

        else:
            text = (
                "❌ Unable to create order.\n\n"
                "Please try again."
            )

        await safe_edit(
            query,
            text,
        )

        return

    context.user_data.clear()

    order_code = data["order_code"]

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📦 My Orders",
                callback_data="my_orders",
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home",
            )
        ],
    ])

    await safe_edit(
        query,
        (
            "✅ <b>Order Created Successfully!</b>\n\n"
            f"🆔 Order ID: "
            f"<code>{order_code}</code>\n"
            f"📦 Package: <b>{offer['name']}</b>\n"
            f"💎 Diamonds: <b>{offer['diamonds']}</b>\n"
            f"🎮 UID: <code>{uid}</code>\n"
            f"💰 Paid: <b>৳{float(offer['price']):.2f}</b>\n\n"
            "⏳ Status: <b>Pending</b>\n\n"
            "Your order will be processed manually."
        ),
        keyboard,
    )


# ============================================================
# MY ORDERS
# ============================================================

async def my_orders_handler(
    update,
    context,
):

    orders = await get_user_orders(
        update.effective_user.id,
        limit=10,
    )

    if not orders:

        text = (
            "📦 <b>My Orders</b>\n\n"
            "You don't have any orders yet."
        )

    else:

        text = "📦 <b>My Orders</b>\n\n"

        for order in orders:

            status = str(
                order["status"]
            ).upper()

            text += (
                f"🆔 <code>{order['order_code']}</code>\n"
                f"📦 {order['offer_name']}\n"
                f"💰 ৳{float(order['price']):.2f}\n"
                f"🎮 UID: <code>{order['uid']}</code>\n"
                f"📌 {status}\n"
                "──────────────\n"
            )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="home",
            )
        ]
    ])

    await send_text(
        update,
        text,
        keyboard,
    )


# ============================================================
# DEPOSIT
# ============================================================

async def deposit_handler(
    update,
    context,
):

    context.user_data["state"] = "waiting_deposit"

    bkash = await get_setting(
        "bkash_number",
        "",
    )

    nagad = await get_setting(
        "nagad_number",
        "",
    )

    rocket = await get_setting(
        "rocket_number",
        "",
    )

    text = (
        "💳 <b>Deposit</b>\n\n"
        "Send money to one of the available payment methods.\n\n"
    )

    if bkash:
        text += f"📱 bKash: <code>{bkash}</code>\n"

    if nagad:
        text += f"📱 Nagad: <code>{nagad}</code>\n"

    if rocket:
        text += f"📱 Rocket: <code>{rocket}</code>\n"

    text += (
        "\nAfter payment, send your "
        "<b>Transaction ID</b>."
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="home",
            )
        ]
    ])

    await send_text(
        update,
        text,
        keyboard,
    )


# ============================================================
# DEPOSIT TRANSACTION ID
# ============================================================

async def handle_deposit_transaction(
    update,
    context,
):

    transaction_id = update.message.text.strip()

    if len(transaction_id) < 4:

        await update.message.reply_text(
            "❌ Invalid transaction ID."
        )

        return

    context.user_data["deposit_transaction"] = (
        transaction_id
    )

    context.user_data["state"] = (
        "waiting_deposit_amount"
    )

    await update.message.reply_text(
        "💰 Now send the deposit amount.\n\n"
        "Example: <code>100</code>",
        parse_mode="HTML",
    )


# ============================================================
# DEPOSIT AMOUNT
# ============================================================

async def handle_deposit_amount(
    update,
    context,
):

    try:
        amount = float(
            update.message.text.strip()
        )

    except ValueError:

        await update.message.reply_text(
            "❌ Please enter a valid amount."
        )

        return

    if amount <= 0:

        await update.message.reply_text(
            "❌ Amount must be greater than 0."
        )

        return

    transaction_id = context.user_data.get(
        "deposit_transaction"
    )

    if not transaction_id:

        context.user_data.clear()

        await update.message.reply_text(
            "❌ Deposit session expired."
        )

        return

    db = await __import__(
        "database"
    ).get_db()

    now = __import__(
        "datetime"
    ).datetime.now().isoformat()

    await db.execute("""
        INSERT INTO deposits
        (
            user_id,
            amount,
            transaction_id,
            status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, 'pending', ?, ?)
    """, (
        update.effective_user.id,
        amount,
        transaction_id,
        now,
        now,
    ))

    deposit_id = (
        await db.execute(
            "SELECT last_insert_rowid()"
        )
    )

    row = await deposit_id.fetchone()

    await db.commit()
    await db.close()

    deposit_id = row[0]

    context.user_data.clear()

    await update.message.reply_text(
        (
            "✅ <b>Deposit Request Submitted</b>\n\n"
            f"🆔 Request: <code>#{deposit_id}</code>\n"
            f"💰 Amount: <b>৳{amount:.2f}</b>\n"
            f"🧾 TxID: <code>{transaction_id}</code>\n\n"
            "⏳ Admin will review your request."
        ),
        parse_mode="HTML",
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

async def dashboard_handler(
    update,
    context,
):

    user_id = update.effective_user.id

    if not await check_admin(user_id):

        await send_text(
            update,
            "⛔ You are not authorized.",
        )

        return

    stats = await get_dashboard_stats()

    text = (
        "🛠 <b>ADMIN DASHBOARD</b>\n\n"
        f"👥 Users: <b>{stats['users']}</b>\n"
        f"🟢 Active: <b>{stats['active']}</b>\n"
        f"🔴 Banned: <b>{stats['banned']}</b>\n\n"
        f"💳 Deposits: "
        f"<b>৳{stats['deposits']:.2f}</b>\n"
        f"💰 Sales: "
        f"<b>৳{stats['sales']:.2f}</b>\n\n"
        f"📦 Orders: <b>{stats['orders']}</b>\n"
        f"⏳ Pending Orders: "
        f"<b>{stats['pending_orders']}</b>\n"
        f"✅ Completed: "
        f"<b>{stats['completed_orders']}</b>\n"
        f"💳 Pending Deposits: "
        f"<b>{stats['pending_deposits']}</b>\n\n"
        f"💎 Active Offers: "
        f"<b>{stats['offers']}</b>"
    )

    await send_text(
        update,
        text,
        admin_dashboard_keyboard(),
    )


# ============================================================
# ADMIN OFFERS
# ============================================================

async def admin_offers_handler(
    query,
    context,
):

    if not await check_admin(
        query.from_user.id
    ):
        await query.answer(
            "Unauthorized",
            show_alert=True,
        )
        return

    offers = await get_all_offers(
        active_only=False
    )

    keyboard = []

    for offer in offers:

        status = "🟢" if offer["is_active"] else "🔴"

        keyboard.append([
            InlineKeyboardButton(
                (
                    f"{status} "
                    f"{offer['name']} "
                    f"৳{float(offer['price']):.0f}"
                ),
                callback_data=f"aoffer:{offer['id']}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "➕ Add Offer",
            callback_data="offer_add",
        )
    ])

    keyboard.append([
        InlineKeyboardButton(
            "⬅️ Dashboard",
            callback_data="dashboard",
        )
    ])

    await safe_edit(
        query,
        "💎 <b>Offer Management</b>\n\n"
        "Select an offer:",
        InlineKeyboardMarkup(keyboard),
    )


# ============================================================
# ADMIN OFFER DETAILS
# ============================================================

async def admin_offer_details(
    query,
    context,
    offer_id,
):

    offer = await __get_offer(
        offer_id
    )

    if not offer:

        await safe_edit(
            query,
            "❌ Offer not found.",
        )

        return

    status = (
        "🟢 Active"
        if offer["is_active"]
        else "🔴 Disabled"
    )

    text = (
        "💎 <b>Offer Management</b>\n\n"
        f"🆔 ID: <code>{offer['id']}</code>\n"
        f"📦 Name: <b>{offer['name']}</b>\n"
        f"💎 Diamonds: <b>{offer['diamonds']}</b>\n"
        f"💰 Price: <b>৳{float(offer['price']):.2f}</b>\n"
        f"🔘 Button: <b>{offer['button_name']}</b>\n"
        f"📌 Status: <b>{status}</b>\n"
    )

    if offer["description"]:
        text += (
            f"\n📝 {offer['description']}"
        )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✏️ Edit",
                callback_data=f"offer_edit:{offer_id}",
            ),
            InlineKeyboardButton(
                "🗑 Delete",
                callback_data=f"offer_delete:{offer_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                "🔄 Enable/Disable",
                callback_data=f"offer_toggle:{offer_id}",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="admin_offers",
            )
        ],
    ])

    await safe_edit(
        query,
        text,
        keyboard,
    )


# ============================================================
# ADMIN USER SEARCH
# ============================================================

async def admin_users_handler(
    query,
    context,
):

    if not await has_permission(
        query.from_user.id,
        "users",
    ):

        await query.answer(
            "No permission",
            show_alert=True,
        )

        return

    context.user_data["state"] = (
        "admin_search_user"
    )

    await safe_edit(
        query,
        (
            "👥 <b>User Management</b>\n\n"
            "Send Telegram User ID, "
            "username or name to search."
        ),
        InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data="dashboard",
                )
            ]
        ]),
    )


# ============================================================
# ADMIN USER SEARCH RESULT
# ============================================================

async def admin_user_search_result(
    update,
    context,
):

    query_text = update.message.text.strip()

    users = await search_users(
        query_text
    )

    context.user_data["state"] = None

    if not users:

        await update.message.reply_text(
            "❌ No users found."
        )

        return

    keyboard = []

    for user in users:

        name = (
            user["first_name"]
            or user["username"]
            or str(user["user_id"])
        )

        keyboard.append([
            InlineKeyboardButton(
                f"👤 {name} ({user['user_id']})",
                callback_data=f"user:{user['user_id']}",
            )
        ])

    await update.message.reply_text(
        "👥 <b>Search Results</b>",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        ),
        parse_mode="HTML",
    )


# ============================================================
# ADMIN USER DETAILS
# ============================================================

async def admin_user_details(
    query,
    context,
    user_id,
):

    details = await get_user_details(
        user_id
    )

    if not details:

        await safe_edit(
            query,
            "❌ User not found.",
        )

        return

    user = details["user"]

    status = (
        "🔴 BANNED"
        if user["is_banned"]
        else "🟢 ACTIVE"
    )

    text = (
        "👤 <b>User Details</b>\n\n"
        f"🆔 ID: <code>{user['user_id']}</code>\n"
        f"👤 Name: {user['first_name'] or '-'}\n"
        f"🔗 Username: "
        f"@{user['username'] or '-'}\n"
        f"📌 Status: <b>{status}</b>\n\n"
        f"💰 Balance: "
        f"<b>৳{float(user['balance']):.2f}</b>\n"
        f"📦 Orders: <b>{details['orders']}</b>\n"
        f"💳 Deposits: <b>{details['deposits']}</b>\n"
        f"👥 Referrals: <b>{details['referrals']}</b>"
    )

    ban_button = (
        "🔓 Unban"
        if user["is_banned"]
        else "🔨 Ban"
    )

    ban_callback = (
        f"unban:{user_id}"
        if user["is_banned"]
        else f"ban:{user_id}"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Add Balance",
                callback_data=f"addbal:{user_id}",
            ),
            InlineKeyboardButton(
                "➖ Remove",
                callback_data=f"removebal:{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                ban_button,
                callback_data=ban_callback,
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="admin_users",
            )
        ],
    ])

    await safe_edit(
        query,
        text,
        keyboard,
    )


# ============================================================
# BALANCE ADD/REMOVE INPUT
# ============================================================

async def balance_action(
    query,
    context,
    user_id,
    action,
):

    if not await check_admin(
        query.from_user.id
    ):
        return

    context.user_data["state"] = (
        "admin_balance"
    )

    context.user_data["balance_user"] = (
        user_id
    )

    context.user_data["balance_action"] = (
        action
    )

    await safe_edit(
        query,
        (
            f"{'➕' if action == 'add' else '➖'} "
            f"<b>Balance {'Add' if action == 'add' else 'Remove'}</b>\n\n"
            f"User ID: <code>{user_id}</code>\n\n"
            "Send amount:"
        ),
    )


async def handle_admin_balance(
    update,
    context,
):

    try:
        amount = float(
            update.message.text.strip()
        )
    except ValueError:

        await update.message.reply_text(
            "❌ Invalid amount."
        )
        return

    if amount <= 0:

        await update.message.reply_text(
            "❌ Amount must be greater than 0."
        )
        return

    user_id = context.user_data.get(
        "balance_user"
    )

    action = context.user_data.get(
        "balance_action"
    )

    if not user_id or not action:

        context.user_data.clear()

        await update.message.reply_text(
            "❌ Session expired."
        )
        return

    if action == "add":

        success, result = await admin_add_balance(
            update.effective_user.id,
            user_id,
            amount,
        )

    else:

        success, result = await admin_remove_balance(
            update.effective_user.id,
            user_id,
            amount,
        )

    context.user_data.clear()

    if not success:

        await update.message.reply_text(
            f"❌ Failed: <code>{result}</code>",
            parse_mode="HTML",
        )
        return

    balance = await get_balance(
        user_id
    )

    await update.message.reply_text(
        (
            "✅ <b>Balance Updated</b>\n\n"
            f"👤 User: <code>{user_id}</code>\n"
            f"💵 Amount: <b>৳{amount:.2f}</b>\n"
            f"💰 New Balance: "
            f"<b>৳{balance:.2f}</b>"
        ),
        parse_mode="HTML",
    )


# ============================================================
# BAN / UNBAN
# ============================================================

async def ban_user_callback(
    query,
    context,
    user_id,
):

    success, result = await admin_ban_user(
        query.from_user.id,
        user_id,
        "Banned by admin",
    )

    if not success:

        await query.answer(
            str(result),
            show_alert=True,
        )
        return

    await query.answer(
        "User banned.",
        show_alert=True,
    )

    await admin_user_details(
        query,
        context,
        user_id,
    )


async def unban_user_callback(
    query,
    context,
    user_id,
):

    success, result = await admin_unban_user(
        query.from_user.id,
        user_id,
    )

    if not success:

        await query.answer(
            str(result),
            show_alert=True,
        )
        return

    await query.answer(
        "User unbanned.",
        show_alert=True,
    )

    await admin_user_details(
        query,
        context,
        user_id,
    )


# ============================================================
# ADMIN DEPOSITS
# ============================================================

async def admin_deposits_handler(
    query,
    context,
):

    if not await has_permission(
        query.from_user.id,
        "deposits",
    ):
        await query.answer(
            "No permission",
            show_alert=True,
        )
        return

    deposits = await get_pending_deposits()

    if not deposits:

        await safe_edit(
            query,
            (
                "💳 <b>Pending Deposits</b>\n\n"
                "✅ No pending deposits."
            ),
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Dashboard",
                        callback_data="dashboard",
                    )
                ]
            ]),
        )

        return

    keyboard = []

    for deposit in deposits:

        keyboard.append([
            InlineKeyboardButton(
                (
                    f"💳 #{deposit['id']} "
                    f"৳{float(deposit['amount']):.0f}"
                ),
                callback_data=f"deposit_view:{deposit['id']}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "⬅️ Dashboard",
            callback_data="dashboard",
        )
    ])

    await safe_edit(
        query,
        "💳 <b>Pending Deposits</b>\n\n"
        "Select a request:",
        InlineKeyboardMarkup(keyboard),
    )


# ============================================================
# DEPOSIT DETAILS
# ============================================================

async def deposit_details(
    query,
    context,
    deposit_id,
):

    from admin import get_deposit

    deposit = await get_deposit(
        deposit_id
    )

    if not deposit:

        await safe_edit(
            query,
            "❌ Deposit not found.",
        )

        return

    text = (
        "💳 <b>Deposit Request</b>\n\n"
        f"🆔 Request: <code>#{deposit['id']}</code>\n"
        f"👤 User: <code>{deposit['user_id']}</code>\n"
        f"💰 Amount: <b>৳{float(deposit['amount']):.2f}</b>\n"
        f"🧾 TxID: <code>{deposit['transaction_id']}</code>\n"
        f"📌 Status: <b>{deposit['status']}</b>\n"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"dep_approve:{deposit_id}",
            ),
            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"dep_reject:{deposit_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="admin_deposits",
            )
        ],
    ])

    await safe_edit(
        query,
        text,
        keyboard,
    )


# ============================================================
# APPROVE DEPOSIT
# ============================================================

async def approve_deposit_callback(
    query,
    context,
    deposit_id,
):

    success, result, data = await approve_deposit(
        query.from_user.id,
        deposit_id,
    )

    if not success:

        await query.answer(
            str(result),
            show_alert=True,
        )

        return

    await query.answer(
        "Deposit approved.",
        show_alert=True,
    )

    user_id = data["deposit"]["user_id"]

    try:

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "✅ <b>Deposit Approved</b>\n\n"
                f"💰 Amount: "
                f"<b>৳{data['amount']:.2f}</b>\n"
                f"💳 New Balance: "
                f"<b>৳{data['balance']:.2f}</b>"
            ),
            parse_mode="HTML",
        )

    except Exception as exc:
        logger.warning(
            "Could not notify user: %s",
            exc,
        )

    await admin_deposits_handler(
        query,
        context,
    )


# ============================================================
# REJECT DEPOSIT
# ============================================================

async def reject_deposit_callback(
    query,
    context,
    deposit_id,
):

    success, result, data = await reject_deposit(
        query.from_user.id,
        deposit_id,
        "Rejected by admin",
    )

    if not success:

        await query.answer(
            str(result),
            show_alert=True,
        )

        return

    await query.answer(
        "Deposit rejected.",
        show_alert=True,
    )

    try:

        await context.bot.send_message(
            chat_id=data["deposit"]["user_id"],
            text=(
                "❌ <b>Deposit Rejected</b>\n\n"
                f"💰 Amount: "
                f"<b>৳{float(data['deposit']['amount']):.2f}</b>\n\n"
                "Please contact support if you believe "
                "this was a mistake."
            ),
            parse_mode="HTML",
        )

    except Exception:
        pass

    await admin_deposits_handler(
        query,
        context,
    )


# ============================================================
# ADMIN ORDERS
# ============================================================

async def admin_orders_handler(
    query,
    context,
):

    if not await has_permission(
        query.from_user.id,
        "orders",
    ):
        await query.answer(
            "No permission",
            show_alert=True,
        )
        return

    orders = await get_pending_orders(
        limit=30
    )

    if not orders:

        await safe_edit(
            query,
            (
                "📦 <b>Pending Orders</b>\n\n"
                "✅ No pending orders."
            ),
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Dashboard",
                        callback_data="dashboard",
                    )
                ]
            ]),
        )

        return

    keyboard = []

    for order in orders:

        keyboard.append([
            InlineKeyboardButton(
                (
                    f"📦 {order['order_code']} "
                    f"| ৳{float(order['price']):.0f}"
                ),
                callback_data=f"aorder:{order['id']}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "⬅️ Dashboard",
            callback_data="dashboard",
        )
    ])

    await safe_edit(
        query,
        "📦 <b>Pending Orders</b>\n\n"
        "Select an order:",
        InlineKeyboardMarkup(keyboard),
    )


# ============================================================
# ADMIN ORDER DETAILS
# ============================================================

async def admin_order_details(
    query,
    context,
    order_id,
):

    order = await get_order(
        order_id
    )

    if not order:

        await safe_edit(
            query,
            "❌ Order not found.",
        )

        return

    text = (
        "📦 <b>Order Details</b>\n\n"
        f"🆔 Order: "
        f"<code>{order['order_code']}</code>\n"
        f"👤 User: "
        f"<code>{order['user_id']}</code>\n"
        f"📦 Offer: <b>{order['offer_name']}</b>\n"
        f"💎 Diamonds: <b>{order['diamonds']}</b>\n"
        f"💰 Price: <b>৳{float(order['price']):.2f}</b>\n"
        f"🎮 UID: <code>{order['uid']}</code>\n"
        f"📌 Status: <b>{order['status']}</b>"
    )

    keyboard = []

    if order["status"] == "pending":

        keyboard.append([
            InlineKeyboardButton(
                "⚙️ Processing",
                callback_data=f"order_process:{order_id}",
            )
        ])

    if order["status"] in (
        "pending",
        "processing",
    ):

        keyboard.append([
            InlineKeyboardButton(
                "✅ Complete",
                callback_data=f"order_complete:{order_id}",
            ),
            InlineKeyboardButton(
                "❌ Cancel + Refund",
                callback_data=f"order_cancel:{order_id}",
            ),
        ])

    keyboard.append([
        InlineKeyboardButton(
            "⬅️ Back",
            callback_data="admin_orders",
        )
    ])

    await safe_edit(
        query,
        text,
        InlineKeyboardMarkup(keyboard),
    )


# ============================================================
# PROCESS ORDER
# ============================================================

async def process_order_callback(
    query,
    context,
    order_id,
):

    success, result = await process_order(
        order_id,
        query.from_user.id,
    )

    if not success:

        await query.answer(
            str(result),
            show_alert=True,
        )
        return

    order = await get_order(
        order_id
    )

    try:

        await context.bot.send_message(
            chat_id=order["user_id"],
            text=(
                "⚙️ <b>Order Processing</b>\n\n"
                f"🆔 Order: "
                f"<code>{order['order_code']}</code>\n\n"
                "Your order is now being processed."
            ),
            parse_mode="HTML",
        )

    except Exception:
        pass

    await query.answer(
        "Order is processing.",
        show_alert=True,
    )

    await admin_order_details(
        query,
        context,
        order_id,
    )


# ============================================================
# COMPLETE ORDER
# ============================================================

async def complete_order_callback(
    query,
    context,
    order_id,
):

    success, result = await complete_order(
        order_id,
        query.from_user.id,
        "Completed manually",
    )

    if not success:

        await query.answer(
            str(result),
            show_alert=True,
        )
        return

    order = await get_order(
        order_id
    )

    try:

        await context.bot.send_message(
            chat_id=order["user_id"],
            text=(
                "✅ <b>Order Completed</b>\n\n"
                f"🆔 Order: "
                f"<code>{order['order_code']}</code>\n"
                f"📦 {order['offer_name']}\n"
                f"💎 {order['diamonds']}\n"
                f"🎮 UID: <code>{order['uid']}</code>\n\n"
                "Thank you for your order! 🎮"
            ),
            parse_mode="HTML",
        )

    except Exception:
        pass

    await query.answer(
        "Order completed.",
        show_alert=True,
    )

    await admin_orders_handler(
        query,
        context,
    )


# ============================================================
# CANCEL ORDER
# ============================================================

async def cancel_order_callback(
    query,
    context,
    order_id,
):

    success, result = await cancel_order(
        order_id,
        query.from_user.id,
        "Cancelled manually by admin",
    )

    if not success:

        await query.answer(
            str(result),
            show_alert=True,
        )
        return

    order = await get_order(
        order_id
    )

    try:

        await context.bot.send_message(
            chat_id=order["user_id"],
            text=(
                "❌ <b>Order Cancelled</b>\n\n"
                f"🆔 Order: "
                f"<code>{order['order_code']}</code>\n\n"
                f"💰 Refunded: "
                f"<b>৳{float(result['refund']):.2f}</b>\n"
                f"💳 New Balance: "
                f"<b>৳{float(result['balance']):.2f}</b>"
            ),
            parse_mode="HTML",
        )

    except Exception:
        pass

    await query.answer(
        "Order cancelled and refunded.",
        show_alert=True,
    )

    await admin_orders_handler(
        query,
        context,
    )


# ============================================================
# BROADCAST
# ============================================================

async def broadcast_handler(
    query,
    context,
):

    if not await has_permission(
        query.from_user.id,
        "broadcast",
    ):

        await query.answer(
            "No permission",
            show_alert=True,
        )

        return

    context.user_data["state"] = (
        "broadcast_message"
    )

    await safe_edit(
        query,
        (
            "📢 <b>Broadcast</b>\n\n"
            "Send the message you want to broadcast.\n\n"
            "HTML formatting is supported."
        ),
        InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="dashboard",
                )
            ]
        ]),
    )


async def handle_broadcast_message(
    update,
    context,
):

    message = update.message

    if not message.text:

        await update.message.reply_text(
            "❌ Only text broadcast is supported here."
        )

        return

    context.user_data["broadcast_text"] = (
        message.text
    )

    context.user_data["state"] = (
        "broadcast_target"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👥 All Users",
                callback_data="broadcast:all",
            )
        ],
        [
            InlineKeyboardButton(
                "🟢 Active Users",
                callback_data="broadcast:active",
            )
        ],
        [
            InlineKeyboardButton(
                "💳 Depositors",
                callback_data="broadcast:depositors",
            )
        ],
        [
            InlineKeyboardButton(
                "📦 Buyers",
                callback_data="broadcast:buyers",
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="dashboard",
            )
        ],
    ])

    await update.message.reply_text(
        "📢 <b>Select Broadcast Target</b>",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


async def run_broadcast(
    query,
    context,
    target,
):

    message = context.user_data.get(
        "broadcast_text"
    )

    if not message:

        await query.answer(
            "Broadcast session expired.",
            show_alert=True,
        )

        return

    users = await get_broadcast_users(
        target
    )

    await safe_edit(
        query,
        (
            "📢 <b>Broadcast Started</b>\n\n"
            f"🎯 Target: <b>{target}</b>\n"
            f"👥 Users: <b>{len(users)}</b>\n\n"
            "Please wait..."
        ),
    )

    sent = 0
    failed = 0

    for user_id in users:

        try:

            await context.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode="HTML",
            )

            sent += 1

        except Exception:

            failed += 1

        # Telegram flood protection
        await asyncio.sleep(0.05)

    await save_broadcast(
        admin_id=query.from_user.id,
        message=message,
        target=target,
        sent_count=sent,
        failed_count=failed,
    )

    context.user_data.clear()

    await query.message.reply_text(
        (
            "✅ <b>Broadcast Completed</b>\n\n"
            f"🎯 Target: <b>{target}</b>\n"
            f"✅ Sent: <b>{sent}</b>\n"
            f"❌ Failed: <b>{failed}</b>"
        ),
        parse_mode="HTML",
    )


# ============================================================
# CALLBACK ROUTER
# ============================================================

async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    data = query.data or ""

    user_id = query.from_user.id

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    if data == "home":

        context.user_data.clear()

        await safe_edit(
            query,
            (
                "💎 <b>FREE FIRE TOP-UP</b>\n\n"
                "Choose an option below:"
            ),
            main_menu_keyboard(),
        )

        return

    # --------------------------------------------------------
    # OFFERS
    # --------------------------------------------------------

    if data == "offers":

        await offers_handler(
            update,
            context,
        )

        return

    # --------------------------------------------------------
    # BALANCE
    # --------------------------------------------------------

    if data == "balance":

        await balance_handler(
            update,
            context,
        )

        return

    # --------------------------------------------------------
    # DEPOSIT
    # --------------------------------------------------------

    if data == "deposit":

        await deposit_handler(
            update,
            context,
        )

        return

    # --------------------------------------------------------
    # MY ORDERS
    # --------------------------------------------------------

    if data == "my_orders":

        await my_orders_handler(
            update,
            context,
        )

        return

    # --------------------------------------------------------
    # OFFER
    # --------------------------------------------------------

    if data.startswith("offer:"):

        offer_id = int(
            data.split(":", 1)[1]
        )

        await offer_selected(
            query,
            context,
            offer_id,
        )

        return

    # --------------------------------------------------------
    # BUY
    # --------------------------------------------------------

    if data.startswith("buy:"):

        offer_id = int(
            data.split(":", 1)[1]
        )

        await buy_offer(
            query,
            context,
            offer_id,
        )

        return

    # --------------------------------------------------------
    # CONFIRM ORDER
    # --------------------------------------------------------

    if data == "confirm_order":

        await confirm_order(
            query,
            context,
        )

        return

    # ========================================================
    # ADMIN
    # ========================================================

    if data == "dashboard":

        await dashboard_handler(
            update,
            context,
        )

        return

    if not await check_admin(user_id):

        await query.answer(
            "⛔ Admin access required.",
            show_alert=True,
        )

        return

    # --------------------------------------------------------
    # ADMIN OFFERS
    # --------------------------------------------------------

    if data == "admin_offers":

        await admin_offers_handler(
            query,
            context,
        )

        return

    if data.startswith("aoffer:"):

        offer_id = int(
            data.split(":", 1)[1]
        )

        await admin_offer_details(
            query,
            context,
            offer_id,
        )

        return

    if data.startswith("offer_toggle:"):

        offer_id = int(
            data.split(":", 1)[1]
        )

        success, result, _ = await toggle_offer(
            offer_id
        )

        await query.answer(
            result,
            show_alert=True,
        )

        await admin_offer_details(
            query,
            context,
            offer_id,
        )

        return

    if data.startswith("offer_delete:"):

        offer_id = int(
            data.split(":", 1)[1]
        )

        success, result = await delete_offer(
            offer_id
        )

        await query.answer(
            result,
            show_alert=True,
        )

        await admin_offers_handler(
            query,
            context,
        )

        return

    # --------------------------------------------------------
    # USERS
    # --------------------------------------------------------

    if data == "admin_users":

        await admin_users_handler(
            query,
            context,
        )

        return

    if data.startswith("user:"):

        target_id = int(
            data.split(":", 1)[1]
        )

        await admin_user_details(
            query,
            context,
            target_id,
        )

        return

    if data.startswith("addbal:"):

        target_id = int(
            data.split(":", 1)[1]
        )

        await balance_action(
            query,
            context,
            target_id,
            "add",
        )

        return

    if data.startswith("removebal:"):

        target_id = int(
            data.split(":", 1)[1]
        )

        await balance_action(
            query,
            context,
            target_id,
            "remove",
        )

        return

    if data.startswith("ban:"):

        target_id = int(
            data.split(":", 1)[1]
        )

        await ban_user_callback(
            query,
            context,
            target_id,
        )

        return

    if data.startswith("unban:"):

        target_id = int(
            data.split(":", 1)[1]
        )

        await unban_user_callback(
            query,
            context,
            target_id,
        )

        return

    # --------------------------------------------------------
    # DEPOSITS
    # --------------------------------------------------------

    if data == "admin_deposits":

        await admin_deposits_handler(
            query,
            context,
        )

        return

    if data.startswith("deposit_view:"):

        deposit_id = int(
            data.split(":", 1)[1]
        )

        await deposit_details(
            query,
            context,
            deposit_id,
        )

        return

    if data.startswith("dep_approve:"):

        deposit_id = int(
            data.split(":", 1)[1]
        )

        await approve_deposit_callback(
            query,
            context,
            deposit_id,
        )

        return

    if data.startswith("dep_reject:"):

        deposit_id = int(
            data.split(":", 1)[1]
        )

        await reject_deposit_callback(
            query,
            context,
            deposit_id,
        )

        return

    # --------------------------------------------------------
    # ORDERS
    # --------------------------------------------------------

    if data == "admin_orders":

        await admin_orders_handler(
            query,
            context,
        )

        return

    if data.startswith("aorder:"):

        order_id = int(
            data.split(":", 1)[1]
        )

        await admin_order_details(
            query,
            context,
            order_id,
        )

        return

    if data.startswith("order_process:"):

        order_id = int(
            data.split(":", 1)[1]
        )

        await process_order_callback(
            query,
            context,
            order_id,
        )

        return

    if data.startswith("order_complete:"):

        order_id = int(
            data.split(":", 1)[1]
        )

        await complete_order_callback(
            query,
            context,
            order_id,
        )

        return

    if data.startswith("order_cancel:"):

        order_id = int(
            data.split(":", 1)[1]
        )

        await cancel_order_callback(
            query,
            context,
            order_id,
        )

        return

    # --------------------------------------------------------
    # BROADCAST
    # --------------------------------------------------------

    if data == "broadcast":

        await broadcast_handler(
            query,
            context,
        )

        return

    if data.startswith("broadcast:"):

        target = data.split(
            ":",
            1
        )[1]

        await run_broadcast(
            query,
            context,
            target,
        )

        return

    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    await query.answer(
        "Unknown action.",
        show_alert=True,
    )


# ============================================================
# TEXT ROUTER
# ============================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    state = context.user_data.get(
        "state"
    )

    if state == "waiting_uid":

        await handle_uid(
            update,
            context,
        )

        return

    if state == "waiting_deposit":

        await handle_deposit_transaction(
            update,
            context,
        )

        return

    if state == "waiting_deposit_amount":

        await handle_deposit_amount(
            update,
            context,
        )

        return

    if state == "admin_search_user":

        if await check_admin(
            update.effective_user.id
        ):

            await admin_user_search_result(
                update,
                context,
            )

        return

    if state == "admin_balance":

        if await check_admin(
            update.effective_user.id
        ):

            await handle_admin_balance(
                update,
                context,
            )

        return

    if state == "broadcast_message":

        if await check_admin(
            update.effective_user.id
        ):

            await handle_broadcast_message(
                update,
                context,
            )

        return

    # --------------------------------------------------------
    # MAIN TEXT BUTTONS
    # --------------------------------------------------------

    text = (
        update.message.text or ""
    ).strip().lower()

    if text in (
        "💎 offers",
        "offers",
        "💎 diamond offers",
    ):

        await offers_handler(
            update,
            context,
        )

        return

    if text in (
        "💰 balance",
        "balance",
    ):

        await balance_handler(
            update,
            context,
        )

        return

    if text in (
        "📦 my orders",
        "my orders",
    ):

        await my_orders_handler(
            update,
            context,
        )

        return

    if text in (
        "➕ deposit",
        "deposit",
    ):

        await deposit_handler(
            update,
            context,
        )

        return

    await update.message.reply_text(
        "Please choose an option from the menu."
    )


# ============================================================
# COMMANDS
# ============================================================

async def dashboard_command(
    update,
    context,
):

    await dashboard_handler(
        update,
        context,
    )


async def admin_command(
    update,
    context,
):

    await dashboard_handler(
        update,
        context,
    )


async def broadcast_command(
    update,
    context,
):

    if not await has_permission(
        update.effective_user.id,
        "broadcast",
    ):

        await update.message.reply_text(
            "⛔ You don't have permission."
        )

        return

    context.user_data["state"] = (
        "broadcast_message"
    )

    await update.message.reply_text(
        (
            "📢 <b>Broadcast</b>\n\n"
            "Send the message you want to broadcast."
        ),
        parse_mode="HTML",
    )


# ============================================================
# REGISTER HANDLERS
# ============================================================

def register_handlers(application):

    # Commands
    application.add_handler(
        CommandHandler(
            "start",
            start_handler,
        )
    )

    application.add_handler(
        CommandHandler(
            "dashboard",
            dashboard_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "admin",
            admin_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "broadcast",
            broadcast_command,
        )
    )

    # Callback buttons
    application.add_handler(
        CallbackQueryHandler(
            callback_handler
        )
    )

    # Text
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    logger.info(
        "handlers.py registered successfully."
)
