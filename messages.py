# ============================================================
# messages.py
# FREE FIRE DIAMOND TOP-UP BOT
# ============================================================


# ============================================================
# GENERAL
# ============================================================

WELCOME = """
🎮 <b>Welcome to Free Fire Diamond Top-Up Bot!</b>

💎 Buy Free Fire Diamonds easily.
💰 Use your bot balance to place orders.
⚡ Orders are manually processed by our Admin Team.

Choose an option below 👇
"""

MAIN_MENU = """
🎮 <b>FREE FIRE TOP-UP</b>

💰 Your Balance: <code>৳{balance:.2f}</code>

Select an option below 👇
"""


HELP = """
ℹ️ <b>HELP CENTER</b>

💎 <b>Diamond Top-Up</b>
Choose a Diamond offer and place your order using your Free Fire UID.

💰 <b>Deposit</b>
Add balance to your account using the available payment methods.

📦 <b>Orders</b>
Check your previous and current orders.

🎟 <b>Promo Code</b>
Use valid promo codes to receive discounts.

🤝 <b>Referral</b>
Invite friends and earn referral rewards.

📞 <b>Support</b>
Contact our support team if you need help.
"""


SUPPORT = """
📞 <b>SUPPORT</b>

Need help?

Contact our support team:

@YourSupport

Please include your Order ID when contacting support about an order.
"""


# ============================================================
# OFFERS
# ============================================================

OFFERS_TITLE = """
💎 <b>DIAMOND OFFERS</b>

Choose your preferred package:
"""


OFFER_DETAILS = """
💎 <b>{name}</b>

💎 Diamonds: <b>{diamonds}</b>
💰 Price: <b>৳{price:.2f}</b>
⚡ Delivery: <b>{delivery}</b>

📝 {description}

Press <b>Buy Now</b> to continue.
"""


# ============================================================
# BUY
# ============================================================

ASK_UID = """
💎 <b>{offer_name}</b>

💰 Price: <b>৳{price:.2f}</b>

🆔 Please send your <b>Free Fire UID</b>.

Example:
<code>123456789</code>
"""


INVALID_UID = """
❌ <b>Invalid UID</b>

Please send a valid Free Fire UID.
"""


ORDER_CONFIRM = """
📦 <b>ORDER CONFIRMATION</b>

💎 Package: <b>{offer_name}</b>
💎 Diamonds: <b>{diamonds}</b>

🆔 Free Fire UID:
<code>{uid}</code>

💰 Price: <b>৳{price:.2f}</b>

💵 Your Balance:
<code>৳{balance:.2f}</code>

Please confirm your order.
"""


INSUFFICIENT_BALANCE = """
❌ <b>Insufficient Balance</b>

💰 Required: <code>৳{required:.2f}</code>
💵 Your Balance: <code>৳{balance:.2f}</code>

Please deposit more balance and try again.
"""


ORDER_CREATED = """
✅ <b>ORDER CREATED</b>

📦 Order ID:
<code>#{order_code}</code>

💎 Package: <b>{offer_name}</b>
💎 Diamonds: <b>{diamonds}</b>

🆔 UID:
<code>{uid}</code>

💰 Amount: <b>৳{price:.2f}</b>

⏳ Status: <b>Pending</b>

Your order will be manually processed by our Admin Team.
"""


ORDER_COMPLETED = """
🎉 <b>ORDER COMPLETED</b>

📦 Order ID:
<code>#{order_code}</code>

💎 Package: <b>{offer_name}</b>
💎 Diamonds: <b>{diamonds}</b>

🆔 UID:
<code>{uid}</code>

💰 Amount: <b>৳{price:.2f}</b>

✅ Status: <b>Completed</b>

Thank you for using our service! ❤️
"""


ORDER_CANCELLED = """
❌ <b>ORDER CANCELLED</b>

📦 Order ID:
<code>#{order_code}</code>

💎 Package: <b>{offer_name}</b>

💰 Amount: <b>৳{price:.2f}</b>

If the amount was already deducted, it has been returned to your balance.
"""


# ============================================================
# ACCOUNT
# ============================================================

ACCOUNT = """
👤 <b>MY ACCOUNT</b>

🆔 User ID:
<code>{user_id}</code>

👤 Username:
{username}

💰 Balance:
<code>৳{balance:.2f}</code>

💵 Total Deposit:
<code>৳{total_deposit:.2f}</code>

💎 Total Spent:
<code>৳{total_spent:.2f}</code>

🤝 Referrals:
<b>{referrals}</b>

📅 Joined:
{joined_at}
"""


# ============================================================
# DEPOSIT
# ============================================================

DEPOSIT_MENU = """
💰 <b>DEPOSIT BALANCE</b>

Minimum Deposit:
<b>৳{minimum:.2f}</b>

Choose a payment method:
"""


ASK_DEPOSIT_AMOUNT = """
💰 <b>DEPOSIT</b>

Payment Method:
<b>{method}</b>

Please enter the amount you want to deposit.

Minimum:
<b>৳{minimum:.2f}</b>
"""


INVALID_DEPOSIT_AMOUNT = """
❌ Invalid amount.

Please enter a valid amount greater than or equal to:
<b>৳{minimum:.2f}</b>
"""


DEPOSIT_PAYMENT_INFO = """
💰 <b>DEPOSIT PAYMENT</b>

Amount:
<b>৳{amount:.2f}</b>

Method:
<b>{method}</b>

Payment Details:
<code>{payment_details}</code>

After sending the payment, send your Transaction ID.
"""


ASK_TRANSACTION_ID = """
🧾 <b>TRANSACTION ID</b>

Please send your payment Transaction ID.

Example:
<code>ABC123XYZ</code>
"""


DEPOSIT_SUBMITTED = """
✅ <b>DEPOSIT REQUEST SUBMITTED</b>

💵 Amount:
<b>৳{amount:.2f}</b>

💳 Method:
<b>{method}</b>

🧾 Transaction ID:
<code>{transaction_id}</code>

⏳ Status:
<b>Pending</b>

An Admin will review your payment shortly.
"""


DEPOSIT_APPROVED = """
✅ <b>DEPOSIT APPROVED</b>

💰 Amount Added:
<b>৳{amount:.2f}</b>

💳 Method:
<b>{method}</b>

🧾 Transaction ID:
<code>{transaction_id}</code>

💵 Your New Balance:
<b>৳{balance:.2f}</b>

Thank you! ❤️
"""


DEPOSIT_REJECTED = """
❌ <b>DEPOSIT REJECTED</b>

💰 Amount:
<b>৳{amount:.2f}</b>

🧾 Transaction ID:
<code>{transaction_id}</code>

Reason:
{reason}
"""


# ============================================================
# MY ORDERS
# ============================================================

MY_ORDERS = """
📦 <b>MY ORDERS</b>

Choose an order to view its details.
"""


ORDER_DETAILS = """
📦 <b>ORDER DETAILS</b>

Order ID:
<code>#{order_code}</code>

💎 Package:
<b>{offer_name}</b>

💎 Diamonds:
<b>{diamonds}</b>

🆔 UID:
<code>{uid}</code>

💰 Price:
<b>৳{price:.2f}</b>

📊 Status:
<b>{status}</b>

🕐 Created:
{created_at}
"""


# ============================================================
# PROMO
# ============================================================

PROMO_MENU = """
🎟 <b>PROMO CODE</b>

Have a promo code?

Press the button below to enter it.
"""


ASK_PROMO = """
🎟 <b>ENTER PROMO CODE</b>

Please send your promo code.
"""


PROMO_INVALID = """
❌ Invalid or expired promo code.
"""


PROMO_SUCCESS = """
🎉 <b>PROMO CODE APPLIED</b>

🎟 Code:
<code>{code}</code>

💰 Discount:
<b>৳{discount:.2f}</b>
"""


# ============================================================
# REFERRAL
# ============================================================

REFERRAL = """
🤝 <b>REFERRAL PROGRAM</b>

Invite your friends and earn rewards!

👥 Total Referrals:
<b>{count}</b>

💰 Total Referral Earnings:
<b>৳{earnings:.2f}</b>

🔗 Your Referral Link:
<code>{link}</code>

Share your link with your friends! ❤️
"""


# ============================================================
# ADMIN
# ============================================================

ADMIN_ONLY = """
❌ <b>Access Denied</b>

You are not authorized to access the Admin Dashboard.
"""


ADMIN_DASHBOARD = """
👑 <b>ADMIN DASHBOARD</b>

📊 <b>Statistics</b>

👥 Users: <b>{users}</b>
🟢 Active: <b>{active}</b>
🚫 Banned: <b>{banned}</b>

💵 Deposits: <b>৳{deposits:.2f}</b>
💎 Sales: <b>৳{sales:.2f}</b>

📦 Orders: <b>{orders}</b>
⏳ Pending Orders: <b>{pending_orders}</b>

Choose an option below 👇
"""


# ============================================================
# ADMIN OFFER
# ============================================================

ADMIN_OFFERS = """
🎁 <b>OFFER MANAGEMENT</b>

Here you can add, edit, delete and enable/disable Diamond offers.
"""


ADD_OFFER_NAME = """
➕ <b>ADD OFFER</b>

Send the Offer Name.

Example:
<code>310 Diamonds</code>
"""


ADD_OFFER_DIAMONDS = """
💎 Send the Diamond amount.

Example:
<code>310</code>
"""


ADD_OFFER_PRICE = """
💰 Send the Offer Price.

Example:
<code>250</code>
"""


ADD_OFFER_BUTTON = """
🔘 Send the Button Name.

Example:
<code>💎 Buy 310 Diamonds</code>
"""


ADD_OFFER_DESCRIPTION = """
📝 Send the Offer Description.

Example:
<code>Best value package</code>

You can also send:
<code>skip</code>
"""


ADD_OFFER_DELIVERY = """
⚡ Send the Delivery Time.

Example:
<code>1–5 Minutes</code>

Or send:
<code>skip</code>
"""


OFFER_CREATED_ADMIN = """
✅ <b>OFFER CREATED</b>

💎 Name:
<b>{name}</b>

💎 Diamonds:
<b>{diamonds}</b>

💰 Price:
<b>৳{price:.2f}</b>

🔘 Button:
<b>{button}</b>

⚡ Delivery:
<b>{delivery}</b>
"""


DELETE_OFFER_CONFIRM = """
🗑 <b>DELETE OFFER?</b>

💎 {name}
💰 ৳{price:.2f}

This action cannot be undone.
"""


# ============================================================
# ADMIN USERS
# ============================================================

ADMIN_USERS = """
👥 <b>USER MANAGEMENT</b>

Choose an option below.
"""


USER_DETAILS_ADMIN = """
👤 <b>USER DETAILS</b>

🆔 ID:
<code>{user_id}</code>

👤 Username:
{username}

💰 Balance:
<b>৳{balance:.2f}</b>

💵 Total Deposit:
<b>৳{total_deposit:.2f}</b>

💎 Total Spent:
<b>৳{total_spent:.2f}</b>

📦 Orders:
<b>{orders}</b>

🤝 Referrals:
<b>{referrals}</b>

📊 Status:
<b>{status}</b>

📅 Joined:
{joined_at}
"""


ASK_USER_ID = """
🔎 <b>SEARCH USER</b>

Send the Telegram User ID.
"""


ASK_ADD_BALANCE = """
➕ <b>ADD BALANCE</b>

User ID:
<code>{user_id}</code>

Send the amount to add.
"""


ASK_REMOVE_BALANCE = """
➖ <b>REMOVE BALANCE</b>

User ID:
<code>{user_id}</code>

Send the amount to remove.
"""


BALANCE_UPDATED = """
✅ <b>BALANCE UPDATED</b>

👤 User:
<code>{user_id}</code>

💰 Amount:
<b>৳{amount:.2f}</b>

💵 New Balance:
<b>৳{balance:.2f}</b>
"""


USER_BANNED = """
🚫 <b>USER BANNED</b>

User:
<code>{user_id}</code>

Reason:
{reason}
"""


USER_UNBANNED = """
✅ <b>USER UNBANNED</b>

User:
<code>{user_id}</code>

The user can use the bot again.
"""


# ============================================================
# ADMIN DEPOSITS
# ============================================================

ADMIN_DEPOSIT = """
💵 <b>DEPOSIT REQUEST</b>

🆔 User ID:
<code>{user_id}</code>

👤 Username:
{username}

💰 Amount:
<b>৳{amount:.2f}</b>

💳 Method:
<b>{method}</b>

🧾 Transaction ID:
<code>{transaction_id}</code>

📊 Status:
<b>{status}</b>

🕐 Created:
{created_at}
"""


# ============================================================
# ADMIN ORDERS
# ============================================================

ADMIN_ORDER = """
📦 <b>ORDER</b>

Order ID:
<code>#{order_code}</code>

👤 User:
<code>{user_id}</code>

💎 Package:
<b>{offer_name}</b>

💎 Diamonds:
<b>{diamonds}</b>

🆔 UID:
<code>{uid}</code>

💰 Price:
<b>৳{price:.2f}</b>

📊 Status:
<b>{status}</b>

🕐 Created:
{created_at}
"""


ORDER_PROCESSED = """
⚡ <b>ORDER PROCESSING</b>

Order:
<code>#{order_code}</code>

Admin is currently processing this order.
"""


# ============================================================
# BROADCAST
# ============================================================

BROADCAST_MENU = """
📢 <b>BROADCAST</b>

Choose your target audience.
"""


BROADCAST_ASK_MESSAGE = """
📢 <b>BROADCAST MESSAGE</b>

Send the message you want to broadcast.

You can send:
• Text
• Photo
• Video
• Document
"""


BROADCAST_PREVIEW = """
📢 <b>BROADCAST PREVIEW</b>

Target:
<b>{target}</b>

Recipients:
<b>{count}</b>

Do you want to send this message?
"""


BROADCAST_DONE = """
✅ <b>BROADCAST COMPLETED</b>

👥 Target:
<b>{target}</b>

✅ Sent:
<b>{sent}</b>

❌ Failed:
<b>{failed}</b>
"""


# ============================================================
# PROMO ADMIN
# ============================================================

CREATE_PROMO_CODE = """
🎟 <b>CREATE PROMO CODE</b>

Send the Promo Code.

Example:
<code>FF50</code>
"""


CREATE_PROMO_DISCOUNT = """
💰 Send the discount amount.

Example:
<code>50</code>
"""


CREATE_PROMO_MINIMUM = """
🛒 Send the minimum purchase amount.

Example:
<code>300</code>
"""


CREATE_PROMO_USES = """
🔢 Send the maximum number of uses.

Example:
<code>100</code>

For unlimited uses send:
<code>0</code>
"""


CREATE_PROMO_EXPIRY = """
📅 Send the expiry date.

Example:
<code>30-08-2026</code>

For no expiry send:
<code>none</code>
"""


# ============================================================
# ADMIN SETTINGS
# ============================================================

ADMIN_SETTINGS = """
⚙️ <b>BOT SETTINGS</b>

Manage payment methods, deposit settings,
referral system, notifications and maintenance mode.
"""


PAYMENT_SETTINGS = """
💳 <b>PAYMENT SETTINGS</b>

Configure the payment information users see when depositing.
"""


MAINTENANCE_ON = """
🛠 <b>MAINTENANCE MODE ENABLED</b>

Users will temporarily be unable to use the bot.
"""


MAINTENANCE_OFF = """
✅ <b>MAINTENANCE MODE DISABLED</b>

The bot is now available to users.
"""


# ============================================================
# ERRORS
# ============================================================

ERROR_GENERIC = """
❌ Something went wrong.

Please try again later.
"""


USER_BANNED_MESSAGE = """
🚫 <b>You are banned from using this bot.</b>

Reason:
{reason}

Please contact support if you believe this is a mistake.
"""


MAINTENANCE_MESSAGE = """
🛠 <b>BOT UNDER MAINTENANCE</b>

Our service is temporarily unavailable.

Please try again later.
"""


CANCELLED = """
❌ Action cancelled.
"""


NO_OFFERS = """
😔 <b>No offers are currently available.</b>

Please check again later.
"""


NO_ORDERS = """
📦 You don't have any orders yet.
"""


NO_DEPOSITS = """
💵 You don't have any deposit history yet.
"""


NO_USERS = """
👥 No users found.
"""


NO_PENDING_DEPOSITS = """
💵 There are no pending deposit requests.
"""


NO_PENDING_ORDERS = """
📦 There are no pending orders.
"""


# ============================================================
# NEW OFFER NOTIFICATION
# ============================================================

NEW_OFFER_NOTIFICATION = """
🎉 <b>NEW DIAMOND OFFER!</b>

💎 {name}
💎 Diamonds: <b>{diamonds}</b>

💰 Price:
<b>৳{price:.2f}</b>

⚡ Delivery:
<b>{delivery}</b>

🔥 Available now!
"""


# ============================================================
# ADMIN NOTIFICATION
# ============================================================

NEW_ORDER_ADMIN = """
🔔 <b>NEW ORDER RECEIVED</b>

📦 Order:
<code>#{order_code}</code>

👤 User:
<code>{user_id}</code>

💎 Package:
<b>{offer_name}</b>

💎 Diamonds:
<b>{diamonds}</b>

🆔 UID:
<code>{uid}</code>

💰 Amount:
<b>৳{price:.2f}</b>

⏳ Status:
<b>Pending</b>
"""


NEW_DEPOSIT_ADMIN = """
💰 <b>NEW DEPOSIT REQUEST</b>

👤 User:
<code>{user_id}</code>

💵 Amount:
<b>৳{amount:.2f}</b>

💳 Method:
<b>{method}</b>

🧾 TxID:
<code>{transaction_id}</code>

⏳ Waiting for approval.
"""
