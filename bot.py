import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ==========================================
# CONFIGURATION
# ==========================================
# Read token from Railway Environment Variable for security
BOT_TOKEN = os.getenv("BOT_TOKEN", "8950553222:AAFC30wy9e03VIEFiC9u88rg1VptCQuYAZg")
CHANNEL_ID = "@ForexPulse23FX"  # Target Telegram Channel handle

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# High-quality Forex trading photos
MARKET_IMAGES = [
    "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3",
    "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f",
    "https://images.unsplash.com/photo-1642543492481-44e81e3914a7",
    "https://images.unsplash.com/photo-1535320903710-d993d3d77d29",
]

# Market update posts
POST_TEMPLATES = [
    (
        "⚡ **FOREXPULSE FX: MARKET UPDATE** ⚡\n\n"
        "📊 **Session Overview:**\n"
        "Key currency pairs are holding major support/resistance zones. Watch EUR/USD and GBP/USD closely.\n\n"
        "💡 *Trading Rule:* Risk no more than 1-2% per trade.\n\n"
        "🤖 Powered by @ForexPulseFX_Bot"
    ),
    (
        "🏆 **GOLD (XAU/USD) ANALYSIS** 🏆\n\n"
        "📈 Gold prices continue to react to global economic indicators and interest rate expectations.\n\n"
        "🔥 Keep your notifications ON for market signals!\n\n"
        "⚡ Powered by @ForexPulse23FX"
    ),
    (
        "📊 **RISK MANAGEMENT BRIEF** 📊\n\n"
        "Successful trading requires discipline:\n"
        "• Always set a Stop Loss (SL)\n"
        "• Calculate correct position sizes\n"
        "• Protect your account balance\n\n"
        "🧮 Use /calculator in @ForexPulseFX_Bot to calculate position size."
    ),
    (
        "🌐 **ECONOMIC NEWS WATCH** 🌐\n\n"
        "High-impact news can cause market spikes. Stay patient and wait for confirmation before entering.\n\n"
        "📅 Check news schedule via /calendar"
    )
]

# Quick Action Keyboard
def get_channel_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌐 Open Channel", url="https://t.me/ForexPulse23FX")],
        [InlineKeyboardButton("📊 Active Signals", callback_data="signals")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==========================================
# AUTOMATIC BROADCAST FUNCTION
# ==========================================
async def send_broadcast(context: ContextTypes.DEFAULT_TYPE):
    """Sends a photo and post to the channel immediately on startup and every 30 mins."""
    try:
        image_url = random.choice(MARKET_IMAGES)
        caption_text = random.choice(POST_TEMPLATES)

        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=image_url,
            caption=caption_text,
            parse_mode="Markdown",
            reply_markup=get_channel_keyboard()
        )
        logging.info("Successfully published broadcast to channel.")
    except Exception as e:
        logging.error(f"Failed to post broadcast: {e}")

# ==========================================
# BOT COMMAND HANDLERS
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        f"👋 Welcome, {update.effective_user.first_name}!\n\n"
        "ForexPulse FX Bot delivers real-time Forex market updates, trading signals, "
        "currency analytics, and instant trade notifications straight to your Telegram account.\n\n"
        "⚡ Available Commands:\n"
        "/signals - View active signals\n"
        "/market - Live market prices\n"
        "/calendar - Economic calendar\n"
        "/calculator - Position calculator\n"
        "/vip - Premium channel details"
    )
    await update.message.reply_text(welcome_msg, reply_markup=get_channel_keyboard())

async def signals_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 **Active Signals:** Check @ForexPulse23FX for live signal setups!")

async def market_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 **Market Status:** Major pairs holding key technical levels.")

async def calendar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 **Economic Calendar:** High-impact USD news scheduled today.")

async def calculator_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧮 **Calculator:** Position Size = (Account Balance × Risk %) / (SL Pips × Pip Value)")

async def vip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⭐ **VIP Access:** Contact channel admin at @ForexPulse23FX to upgrade.")

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Register Bot Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("signals", signals_command))
    app.add_handler(CommandHandler("market", market_command))
    app.add_handler(CommandHandler("calendar", calendar_command))
    app.add_handler(CommandHandler("calculator", calculator_command))
    app.add_handler(CommandHandler("vip", vip_command))

    # Schedule Post: 
    # 1. 'first=1' makes it post IMMEDIATELY (1 second after startup/deployment)
    # 2. 'interval=1800' repeats it every 1800 seconds (30 minutes)
    app.job_queue.run_repeating(send_broadcast, interval=1800, first=1)

    logging.info("Bot starting up...")
    app.run_polling()

if __name__ == "__main__":
    main()
