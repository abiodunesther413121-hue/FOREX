import asyncio
import logging
import random
import sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# =========================================================
# CONFIGURATION & CONSTANTS
# =========================================================
BOT_TOKEN = "8950553222:AAFC30wy9e03VIEFiC9u88rg1VptCQuYAZg"
CHANNEL_ID = "@ForexPulseFX"

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Initialize Bot & Dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# =========================================================
# DATABASE SETUP (For tracking stats & logs)
# =========================================================
def init_db():
    conn = sqlite3.connect("forex_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS broadcast_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# =========================================================
# CONTENT POOLS
# =========================================================
MARKET_ASSETS = [
    "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3",
    "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f",
    "https://images.unsplash.com/photo-1642543492481-44e81e3914a7",
    "https://images.unsplash.com/photo-1535320903710-d993d3d77d29"
]

CONTENT_TEMPLATES = [
    (
        "⚡ **FOREXPULSE FX: SESSION MOMENTUM** ⚡\n\n"
        "📊 **Key Pairs Overview:**\n"
        "Monitoring high-volume liquidity zones across EUR/USD and GBP/USD. Patience is your edge in today's session.\n\n"
        "💡 *Rule:* Protect capital first, profits second.\n\n"
        "🤖 Automated feed by @ForexPulseFXBot"
    ),
    (
        "🏆 **GOLD (XAU/USD) INTELLIGENCE** 🏆\n\n"
        "📈 Precious metals reacting to global bond yields and macro sentiment. Keep strict risk boundaries active.\n\n"
        "🔥 Precision entries drop exclusively in @ForexPulseFX!\n\n"
        "⚡ Powered by @ForexPulseFXBot"
    ),
    (
        "📊 **RISK MANAGEMENT BRIEF** 📊\n\n"
        "Professional traders survive by controlling drawdowns:\n"
        "• Max 1-2% risk per position\n"
        "• Never chase a missed candle\n"
        "• Always respect your Stop Loss\n\n"
        "🧮 Use /calculator to size your trades correctly."
    ),
    (
        "🌐 **MACRO ECONOMIC WATCH** 🌐\n\n"
        "High-impact data releases ahead. Watch out for sudden spread widening and volatility spikes.\n\n"
        "📅 Check today's calendar via /calendar"
    )
]

# =========================================================
# KEYBOARD BUILDERS
# =========================================================
def main_menu_markup():
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 Signal Radar", callback_data="menu_signals")
    builder.button(text="📈 Live Prices", callback_data="menu_prices")
    builder.button(text="📅 Econ Calendar", callback_data="menu_calendar")
    builder.button(text="🧮 Calculator", callback_data="menu_calc")
    builder.button(text="⭐ VIP Access", callback_data="menu_vip")
    builder.button(text="🌐 Open Channel", url="https://t.me/ForexPulseFX")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()

# =========================================================
# BROADCAST WORKER (Runs every 30 mins + on startup)
# =========================================================
async def automated_broadcast():
    try:
        photo = random.choice(MARKET_ASSETS)
        caption = random.choice(CONTENT_TEMPLATES)
        
        # Attempt to post with photo
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo,
            caption=caption,
            reply_markup=main_menu_markup()
        )
        
        # Log success in DB
        conn = sqlite3.connect("forex_bot.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO broadcast_logs (timestamp, status) VALUES (?, ?)", 
                       (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "SUCCESS"))
        conn.commit()
        conn.close()
        
        logging.info("Broadcast dispatched successfully to @ForexPulseFX.")
        
    except Exception as e:
        logging.warning(f"Photo broadcast encountered an issue ({e}), falling back to text payload...")
        try:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=caption,
                reply_markup=main_menu_markup()
            )
            logging.info("Text fallback broadcast sent successfully.")
        except Exception as err:
            logging.error(f"Critical Broadcast Failure: {err}")

# =========================================================
# COMMAND HANDLERS
# =========================================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    greeting = (
        f"👋 **Welcome, {message.from_user.first_name}!**\n\n"
        "You are connected to **ForexPulse FX Bot** — your institutional-grade market companion.\n\n"
        "Select an option below to interact:"
    )
    await message.answer(greeting, reply_markup=main_menu_markup())

@dp.message(Command("bot"))
async def cmd_bot(message: types.Message):
    info = (
        "🤖 **System Status: Online**\n\n"
        "• Broadcast Interval: Every 30 Minutes\n"
        "• Target Channel: @ForexPulseFX\n"
        "• Core Engine: Aiogram v3 + APScheduler"
    )
    await message.answer(info, reply_markup=main_menu_markup())

@dp.message(Command("signals"))
async def cmd_signals(message: types.Message):
    sig = (
        "📊 **LIVE SIGNAL FEED**\n\n"
        "💎 **Asset:** XAU/USD (Gold)\n"
        "📌 **Setup:** BUY LIMIT\n"
        "🎯 **Entry Zone:** 2320.00 - 2323.00\n"
        "❌ **Stop Loss:** 2314.00\n"
        "✅ **Take Profit:** 2335.00 / 2350.00"
    )
    await message.answer(sig, reply_markup=main_menu_markup())

@dp.message(Command("market"))
async def cmd_market(message: types.Message):
    prices = (
        "📈 **MARKET SNAPSHOT**\n\n"
        "• **EUR/USD:** 1.0874 (+0.12%)\n"
        "• **GBP/USD:** 1.2745 (-0.05%)\n"
        "• **USD/JPY:** 155.80 (+0.31%)\n"
        "• **XAU/USD:** $2,324.50 (+0.64%)"
    )
    await message.answer(prices, reply_markup=main_menu_markup())

@dp.message(Command("calendar"))
async def cmd_calendar(message: types.Message):
    cal = (
        "📅 **ECONOMIC CALENDAR RADAR**\n\n"
        "🔴 **USD Core Retail Sales**\n"
        "• Impact Level: High\n"
        "• Expected volatility in USD crosses."
    )
    await message.answer(cal, reply_markup=main_menu_markup())

@dp.message(Command("calculator"))
async def cmd_calculator(message: types.Message):
    calc = (
        "🧮 **RISK FORMULA**\n\n"
        "$$\\text{Position Size} = \\frac{\\text{Risk Capital}}{\\text{Stop Loss (pips)} \\times \\text{Pip Value}}$$\n\n"
        "Keep risk strictly controlled."
    )
    await message.answer(calc, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu_markup())

@dp.message(Command("vip"))
async def cmd_vip(message: types.Message):
    vip = (
        "⭐ **VIP MEMBERSHIP ACCESS**\n\n"
        "Unlock real-time institutional feeds and private session rooms. Contact administration to join."
    )
    await message.answer(vip, reply_markup=main_menu_markup())

@dp.message(Command("support"))
async def cmd_support(message: types.Message):
    await message.answer("💬 **Support Desk:** Reach out via channel admins for assistance.", reply_markup=main_menu_markup())

# =========================================================
# INLINE CALLBACK ROUTER
# =========================================================
@dp.callback_query()
async def inline_router(callback: types.CallbackQuery):
    action = callback.data
    if action == "menu_signals":
        await callback.message.answer("📊 Active signal tracking is online. Check channel for real-time entries.")
    elif action == "menu_prices":
        await callback.message.answer("📈 Live quotes are syncing with global feeds.")
    elif action == "menu_calendar":
        await callback.message.answer("📅 High-impact events are monitored 24/7.")
    elif action == "menu_calc":
        await callback.message.answer("🧮 Maintain 1-2% maximum risk parameters.")
    elif action == "menu_vip":
        await callback.message.answer("⭐ Contact administration for VIP channel clearance.")
    await callback.answer()

# =========================================================
# LIFECYCLE MANAGEMENT
# =========================================================
async def on_startup():
    logging.info("Initializing ForexPulse FX Bot core services...")
    
    # 1. Fire immediate post upon successful startup
    await automated_broadcast()
    
    # 2. Register recurring 30-minute scheduler interval
    scheduler.add_job(automated_broadcast, 'interval', minutes=30)
    scheduler.start()
    logging.info("Scheduler successfully linked: Broadcasting every 30 minutes.")

async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
