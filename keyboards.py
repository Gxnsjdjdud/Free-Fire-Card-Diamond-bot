# ============================================================
# keyboards.py
# FREE FIRE DIAMOND TOP-UP BOT
# ============================================================

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


# ============================================================
# USER MAIN MENU
# ============================================================

def main_menu_keyboard():

    keyboard = [
        [
            InlineKeyboardButton("💎 Diamond Top-Up", callback_data="offers"),
            InlineKeyboardButton("🎁 Special Offers", callback_data="special_offers"),
        ],
        [
            InlineKeyboardButton("💰 Deposit", callback_data="deposit"),
            InlineKeyboardButton("👤 My Account", callback_data="account"),
        ],
        [
            InlineKeyboardButton("📦 My Orders", callback_data="my_orders"),
            InlineKeyboardButton("🎟 Promo Code", callback_data="promo"),
        ],
        [
            InlineKeyboardButton("🤝 Referral", callback_data="referral"),
            InlineKeyboardButton("📞 Support", callback_data="support"),
        ],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# BACK BUTTON
# ============================================================

def back_button(callback_data="main_menu"):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data=callback_data
            )
        ]
    ])


# ============================================================
# OFFER LIST
# ============================================================

def offers_keyboard(offers):

    keyboard = []

    for offer in offers:

        keyboard.append([
            InlineKeyboardButton(
                offer["button_name"],
                callback_data=f"offer:{offer['id']}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "🔙 Main Menu",
            callback_data="main_menu"
        )
    ])

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# OFFER DETAILS
# ============================================================

def offer_details_keyboard(offer_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💎 Buy Now",
                callback_data=f"buy:{offer_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back to Offers",
                callback_data="offers"
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 Main Menu",
                callback_data="main_menu"
            )
        ],
    ])


# ============================================================
# CONFIRM ORDER
# ============================================================

def confirm_order_keyboard(offer_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Confirm Order",
                callback_data=f"confirm_order:{offer_id}"
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="offers"
            ),
        ]
    ])


# ============================================================
# USER ACCOUNT
# ============================================================

def account_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💵 Balance History",
                callback_data="balance_history"
            )
        ],
        [
            InlineKeyboardButton(
                "📦 My Orders",
                callback_data="my_orders"
            ),
            InlineKeyboardButton(
                "💵 My Deposits",
                callback_data="my_deposits"
            ),
        ],
        [
            InlineKeyboardButton(
                "🤝 Referral",
                callback_data="referral"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Main Menu",
                callback_data="main_menu"
            )
        ],
    ])


# ============================================================
# DEPOSIT METHODS
# ============================================================

def deposit_methods_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💳 bKash",
                callback_data="deposit_method:bkash"
            ),
            InlineKeyboardButton(
                "💳 Nagad",
                callback_data="deposit_method:nagad"
            ),
        ],
        [
            InlineKeyboardButton(
                "💳 Rocket",
                callback_data="deposit_method:rocket"
            ),
            InlineKeyboardButton(
                "₿ Binance",
                callback_data="deposit_method:binance"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="main_menu"
            )
        ],
    ])


# ============================================================
# DEPOSIT CONFIRM
# ============================================================

def deposit_confirm_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Submit Deposit",
                callback_data="deposit_submit"
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="main_menu"
            ),
        ]
    ])


# ============================================================
# ORDER STATUS
# ============================================================

def order_status_keyboard(order_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔄 Refresh",
                callback_data=f"order_refresh:{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 My Orders",
                callback_data="my_orders"
            ),
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="main_menu"
            ),
        ],
    ])


# ============================================================
# PROMO
# ============================================================

def promo_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎟 Enter Promo Code",
                callback_data="enter_promo"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Main Menu",
                callback_data="main_menu"
            )
        ],
    ])


# ============================================================
# REFERRAL
# ============================================================

def referral_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📤 Share Referral",
                switch_inline_query="Join our Free Fire Top-Up Bot!"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Main Menu",
                callback_data="main_menu"
            )
        ],
    ])


# ============================================================
# SUPPORT
# ============================================================

def support_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📞 Contact Support",
                url="https://t.me/YourSupport"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Main Menu",
                callback_data="main_menu"
            )
        ],
    ])


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "🎁 Manage Offers",
                callback_data="admin:offers"
            )
        ],

        [
            InlineKeyboardButton(
                "➕ Add Offer",
                callback_data="admin:add_offer"
            ),
            InlineKeyboardButton(
                "📋 All Offers",
                callback_data="admin:all_offers"
            ),
        ],

        [
            InlineKeyboardButton(
                "👥 Users",
                callback_data="admin:users"
            ),
            InlineKeyboardButton(
                "🔎 Search User",
                callback_data="admin:search_user"
            ),
        ],

        [
            InlineKeyboardButton(
                "💵 Deposits",
                callback_data="admin:deposits"
            ),
            InlineKeyboardButton(
                "📦 Orders",
                callback_data="admin:orders"
            ),
        ],

        [
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="admin:broadcast"
            ),
            InlineKeyboardButton(
                "🎟 Promo Codes",
                callback_data="admin:promo"
            ),
        ],

        [
            InlineKeyboardButton(
                "📊 Statistics",
                callback_data="admin:stats"
            ),
            InlineKeyboardButton(
                "⚙️ Settings",
                callback_data="admin:settings"
            ),
        ],

        [
            InlineKeyboardButton(
                "🛡️ Admin Management",
                callback_data="admin:admins"
            )
        ],

        [
            InlineKeyboardButton(
                "📜 Admin Logs",
                callback_data="admin:logs"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# ADMIN OFFER MANAGEMENT
# ============================================================

def admin_offer_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Add Offer",
                callback_data="admin:add_offer"
            )
        ],
        [
            InlineKeyboardButton(
                "✏️ Edit Offer",
                callback_data="admin:edit_offer"
            ),
            InlineKeyboardButton(
                "🗑 Delete Offer",
                callback_data="admin:delete_offer"
            ),
        ],
        [
            InlineKeyboardButton(
                "📋 All Offers",
                callback_data="admin:all_offers"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Dashboard",
                callback_data="admin:dashboard"
            )
        ],
    ])


# ============================================================
# ADMIN OFFER ACTIONS
# ============================================================

def admin_offer_actions(offer_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✏️ Edit",
                callback_data=f"admin:edit_offer:{offer_id}"
            ),
            InlineKeyboardButton(
                "🗑 Delete",
                callback_data=f"admin:delete_offer:{offer_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔄 Enable/Disable",
                callback_data=f"admin:toggle_offer:{offer_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Offers",
                callback_data="admin:offers"
            )
        ],
    ])


# ============================================================
# DELETE CONFIRM
# ============================================================

def confirm_delete_offer_keyboard(offer_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Yes, Delete",
                callback_data=f"admin:confirm_delete:{offer_id}"
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="admin:offers"
            ),
        ]
    ])


# ============================================================
# ADMIN USER MANAGEMENT
# ============================================================

def admin_users_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📋 All Users",
                callback_data="admin:all_users"
            )
        ],
        [
            InlineKeyboardButton(
                "🔎 Search User",
                callback_data="admin:search_user"
            )
        ],
        [
            InlineKeyboardButton(
                "🚫 Banned Users",
                callback_data="admin:banned_users"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Dashboard",
                callback_data="admin:dashboard"
            )
        ],
    ])


# ============================================================
# ADMIN USER ACTIONS
# ============================================================

def admin_user_actions(user_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Add Balance",
                callback_data=f"admin:add_balance:{user_id}"
            ),
            InlineKeyboardButton(
                "➖ Remove Balance",
                callback_data=f"admin:remove_balance:{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                "📦 Orders",
                callback_data=f"admin:user_orders:{user_id}"
            ),
            InlineKeyboardButton(
                "💵 Deposits",
                callback_data=f"admin:user_deposits:{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                "🚫 Ban User",
                callback_data=f"admin:ban:{user_id}"
            ),
            InlineKeyboardButton(
                "📩 Message",
                callback_data=f"admin:message_user:{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔙 Users",
                callback_data="admin:users"
            )
        ],
    ])


# ============================================================
# BAN CONFIRM
# ============================================================

def confirm_ban_keyboard(user_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🚫 Confirm Ban",
                callback_data=f"admin:confirm_ban:{user_id}"
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data=f"admin:user:{user_id}"
            ),
        ]
    ])


# ============================================================
# UNBAN
# ============================================================

def unban_keyboard(user_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Unban User",
                callback_data=f"admin:unban:{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Users",
                callback_data="admin:users"
            )
        ],
    ])


# ============================================================
# ADMIN DEPOSITS
# ============================================================

def admin_deposits_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📥 Pending",
                callback_data="admin:pending_deposits"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Approved",
                callback_data="admin:approved_deposits"
            ),
            InlineKeyboardButton(
                "❌ Rejected",
                callback_data="admin:rejected_deposits"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔙 Dashboard",
                callback_data="admin:dashboard"
            )
        ],
    ])


# ============================================================
# DEPOSIT ACTIONS
# ============================================================

def deposit_action_keyboard(deposit_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"admin:approve_deposit:{deposit_id}"
            ),
            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"admin:reject_deposit:{deposit_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                "👤 User",
                callback_data=f"admin:deposit_user:{deposit_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Deposits",
                callback_data="admin:deposits"
            )
        ],
    ])


# ============================================================
# ADMIN ORDERS
# ============================================================

def admin_orders_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⏳ Pending",
                callback_data="admin:pending_orders"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Completed",
                callback_data="admin:completed_orders"
            ),
            InlineKeyboardButton(
                "❌ Cancelled",
                callback_data="admin:cancelled_orders"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔎 Search Order",
                callback_data="admin:search_order"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Dashboard",
                callback_data="admin:dashboard"
            )
        ],
    ])


# ============================================================
# ADMIN ORDER ACTIONS
# ============================================================

def admin_order_actions(order_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⚡ Process",
                callback_data=f"admin:process_order:{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Complete",
                callback_data=f"admin:complete_order:{order_id}"
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data=f"admin:cancel_order:{order_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                "👤 User",
                callback_data=f"admin:order_user:{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Orders",
                callback_data="admin:orders"
            )
        ],
    ])


# ============================================================
# BROADCAST
# ============================================================

def broadcast_target_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👥 All Users",
                callback_data="broadcast:all"
            )
        ],
        [
            InlineKeyboardButton(
                "🟢 Active Users",
                callback_data="broadcast:active"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Depositors",
                callback_data="broadcast:depositors"
            ),
            InlineKeyboardButton(
                "💎 Buyers",
                callback_data="broadcast:buyers"
            ),
        ],
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="admin:dashboard"
            )
        ],
    ])


# ============================================================
# BROADCAST CONFIRM
# ============================================================

def broadcast_confirm_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 Send",
                callback_data="broadcast:confirm"
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="admin:dashboard"
            ),
        ]
    ])


# ============================================================
# PROMO ADMIN
# ============================================================

def admin_promo_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Create Promo",
                callback_data="admin:create_promo"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 All Promo Codes",
                callback_data="admin:all_promo"
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 Delete Promo",
                callback_data="admin:delete_promo"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Dashboard",
                callback_data="admin:dashboard"
            )
        ],
    ])


# ============================================================
# ADMIN SETTINGS
# ============================================================

def admin_settings_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💳 Payment Methods",
                callback_data="admin:payment_settings"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Deposit Settings",
                callback_data="admin:deposit_settings"
            ),
            InlineKeyboardButton(
                "🤝 Referral Settings",
                callback_data="admin:referral_settings"
            ),
        ],
        [
            InlineKeyboardButton(
                "📢 Notification Settings",
                callback_data="admin:notification_settings"
            )
        ],
        [
            InlineKeyboardButton(
                "🛠 Maintenance Mode",
                callback_data="admin:maintenance"
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Support",
                callback_data="admin:support_settings"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Dashboard",
                callback_data="admin:dashboard"
            )
        ],
    ])


# ============================================================
# PAYMENT SETTINGS
# ============================================================

def payment_settings_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💳 Edit bKash",
                callback_data="admin:edit_bkash"
            ),
            InlineKeyboardButton(
                "💳 Edit Nagad",
                callback_data="admin:edit_nagad"
            ),
        ],
        [
            InlineKeyboardButton(
                "💳 Edit Rocket",
                callback_data="admin:edit_rocket"
            ),
            InlineKeyboardButton(
                "₿ Edit Binance",
                callback_data="admin:edit_binance"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔙 Settings",
                callback_data="admin:settings"
            )
        ],
    ])


# ============================================================
# ADMIN MANAGEMENT
# ============================================================

def admin_management_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Add Admin",
                callback_data="admin:add_admin"
            ),
            InlineKeyboardButton(
                "➖ Remove Admin",
                callback_data="admin:remove_admin"
            ),
        ],
        [
            InlineKeyboardButton(
                "📋 Admin List",
                callback_data="admin:admin_list"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Dashboard",
                callback_data="admin:dashboard"
            )
        ],
    ])


# ============================================================
# PAGINATION
# ============================================================

def pagination_keyboard(
    prefix,
    page,
    has_previous=True,
    has_next=True
):

    buttons = []

    if has_previous:
        buttons.append(
            InlineKeyboardButton(
                "⬅️ Previous",
                callback_data=f"{prefix}:page:{page - 1}"
            )
        )

    if has_next:
        buttons.append(
            InlineKeyboardButton(
                "Next ➡️",
                callback_data=f"{prefix}:page:{page + 1}"
            )
        )

    keyboard = []

    if buttons:
        keyboard.append(buttons)

    keyboard.append([
        InlineKeyboardButton(
            "🔙 Back",
            callback_data="admin:dashboard"
        )
    ])

    return InlineKeyboardMarkup(keyboard)
