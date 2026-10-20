import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
BOT_TOKEN = "8950553222:AAFC30wy9e03VIEFiC9u88rg1VptCQuYAZg"
CHANNEL_ID = "@ForexPulseFX"  # Your target Telegram channel

# Public Forex / Financial Trading Stock Images
MARKET_IMAGES = [
    "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3",
    "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f",
    "https://images.unsplash.com/photo-1642543492481-44e81e3914a7",
    "https://images.unsplash.com/photo-1535320903710-d993d3d77d29",
]

# Rotating Channel Content Templates
POST_TEMPLATES = [
    (
        "⚡ **FOREXPULSE FX MARKET UPDATE** ⚡\n\n"
        "📊 **EUR/USD & GBP/USD Dynamics:**\n"
        "The FX markets are showing strong momentum. Maintain strict risk management and watch key support/resistance zones.\n\n"
        "💡 *Tip:* Never risk more than 1-2% per trade.\n\n"
        "🤖 Automated updates by @ForexPulseFXBot"
    ),
    (
        "🏆 **GOLD (XAU/USD) ANALYSIS** 🏆\n\n"
        "📈 Gold prices continue to react to global economic indicators and interest rate expectations.\n\n"
        "🔥 Keep your notifications ON for precision signal entries!\n\n"
        "⚡ Powered by @ForexPulseFX"
    ),
    (
        "📊 **DAILY RISK MANAGEMENT CHECK** 📊\n\n"
        "Success in Forex is 20% strategy and 80% discipline:\n"
        "• Always set a Stop Loss (SL)\n"
        "• Stick to your Lot Size calculation\n"
        "• Protect your capital first\n\n"
        "🧮 Use /calculator to compute your lot size!"
    ),
    (
        "🌐 **HIGH-IMPACT NEWS ALERT** 🌐\n\n"
        "Major economic data releases can cause sudden volatility spikes in major pairs.\n\n"
        "📅 Check today's high-impact news schedule using /calendar"
    )
]

# Initialize Logger & Bot
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# ---------------------------------------------------------
# KEYBOARD BUILDERS
# ---------------------------------------------------------
def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 Active Signals", callback_data="btn_signals")
    builder.button(text="📈 Market Prices", callback_data="btn_market")
    builder.button(text="📅 Econ Calendar", callback_data="btn_calendar")
    builder.button(text="🧮 Calculator", callback_data="btn_calc")
    builder.button(text="⭐ VIP Access", callback_data="btn_vip")
    builder.button(text="🌐 Visit Channel", url="https://t.me/ForexPulseFX")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()

# ---------------------------------------------------------
# CHANNEL BROADCAST FUNCTION (Every 30 Mins + On Startup)
# ---------------------------------------------------------
async def post_to_channel():
    """Selects a random image and message, then posts to the channel securely."""
    try:
        image_url = random.choice(MARKET_IMAGES)
        caption_text = random.choice(POST_TEMPLATES)
        
        # Try posting with image first
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=image_url,
            caption=caption_text,
            reply_markup=get_main_menu_keyboard()
        )
        logging.info("Successfully posted scheduled message (with photo) to channel.")
    except Exception as e:
        logging.warning(f"Photo post failed ({e}), falling back to text-only post...")
        try:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=caption_text,
                reply_markup=get_main_menu_keyboard()
            )
            logging.info("Successfully posted scheduled message (text-only) to channel.")
        except Exception as err:
            logging.error(f"Critical broadcast error: {err}")

# ---------------------------------------------------------
# BOT COMMAND HANDLERS
# ---------------------------------------------------------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        f"👋 **Welcome, {message.from_user.first_name}!**\n\n"
        "Welcome to **ForexPulse FX Bot** — your automated trading companion for real-time market intelligence.\n\n"
        "⚡ Choose an option below to navigate:"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard())

@dp.message(Command("bot"))
async def cmd_bot(message: types.Message):
    bot_info = (
        "🤖 **About ForexPulse FX Bot**\n\n"
        "I am an automated assistant powering the @ForexPulseFX community.\n\n"
        "• 📊 Automated market updates every 30 minutes\n"
        "• 📈 Technical analysis & instant signal alerts\n"
        "• 📅 News & economic event tracking\n"
        "• 🧮 Trading tools & risk calculation"
    )
    await message.answer(bot_info, reply_markup=get_main_menu_keyboard())

@dp.message(Command("signals"))
async def cmd_signals(message: types.Message):
    signals_text = (
        "📊 **ACTIVE SIGNAL RADAR**\n\n"
        "💎 **Pair:** XAU/USD (Gold)\n"
        "📌 **Type:** BUY LIMIT\n"
        "🎯 **Entry Zone:** 2320.00 - 2323.00\n"
        "❌ **Stop Loss:** 2314.00\n"
        "✅ **Take Profit:** 2335.00 / 2350.00\n\n"
        "⚠️ *Manage risk accordingly. Check @ForexPulseFX for updates.*"
    )
    await message.answer(signals_text, reply_markup=get_main_menu_keyboard())

@dp.message(Command("market"))
async def cmd_market(message: types.Message):
    market_text = (
        "📈 **LIVE MARKET OVERVIEW**\n\n"
        "• **EUR/USD:** 1.0874 (+0.12%)\n"
        "• **GBP/USD:** 1.2745 (-0.05%)\n"
        "• **USD/JPY:** 155.80 (+0.31%)\n"
        "• **XAU/USD (Gold):** $2,324.50 (+0.64%)\n\n"
        "🔄 *Prices update dynamically during active trading sessions.*"
    )
    await message.answer(market_text, reply_markup=get_main_menu_keyboard())

@dp.message(Command("calendar"))
async def cmd_calendar(message: types.Message):
    calendar_text = (
        "📅 **TODAY'S HIGH-IMPACT NEWS**\n\n"
        "🔴 **USD - Core Retail Sales (m/m)**\n"
        "• Impact: High\n"
        "• Forecast: 0.2% | Previous: 0.1%\n\n"
        "🔴 **EUR - ECB Monetary Policy Meeting**\n"
        "• Impact: High\n"
        "• Watch out for sudden volatility spikes across major pairs."
    )
    await message.answer(calendar_text, reply_markup=get_main_menu_keyboard())

@dp.message(Command("calculator"))
async def cmd_calculator(message: types.Message):
    calc_text = (
        "🧮 **POSITION SIZE CALCULATOR GUIDE**\n\n"
        "To calculate your lot size manually:\n"
        "$$\\text{Lot Size} = \\frac{\\text{Account Balance} \\times \\text{Risk %}}{\\text{Stop Loss (pips)} \\times \\text{Pip Value}}$$\n\n"
        "Keep your risk between 1% to 2% per trade to ensure account longevity."
    )
    await message.answer(calc_text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu_keyboard())

@dp.message(Command("vip"))
async def cmd_vip(message: types.Message):
    vip_text = (
        "⭐ **FOREXPULSE VIP MEMBERSHIP**\n\n"
        "Unlock institutional-grade advantages:\n"
        "• 90%+ Accuracy Scalping Signals\n"
        "• Direct mentorship & live trading rooms\n"
        "• Automated webhook alerts\n\n"
        "💬 Contact admin to secure your slot."
    )
    await message.answer(vip_text, reply_markup=get_main_menu_keyboard())

@dp.message(Command("support"))
async def cmd_support(message: types.Message):
    await message.answer("💬 **Support Desk:** For assistance, reach out directly to channel administration.", reply_markup=get_main_menu_keyboard())

# ---------------------------------------------------------
# CALLBACK QUERY HANDLERS (Inline Buttons)
# ---------------------------------------------------------
@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    data = callback.data
    if data == "btn_signals":
        await callback.message.answer("📊 **Active Signals:** XAU/USD Buy Limit active. Check channel for full breakdowns.")
    elif data == "btn_market":
        await callback.message.answer("📈 **Market Status:** Major pairs holding steady above key support levels.")
    elif data == "btn_calendar":
        await callback.message.answer("📅 **Calendar:** High-impact USD news scheduled for today's NY session.")
    elif data == "btn_calc":
        await callback.message.answer("🧮 **Calculator Rule:** Risk max 2% per position to maintain healthy drawdown limits.")
    elif data == "btn_vip":
        await callback.message.answer("⭐ **VIP Access:** Message administration to upgrade your plan.")
    await callback.answer()

# ---------------------------------------------------------
# DEPLOYMENT & LIFECYCLE HOOKS
# ---------------------------------------------------------
async def on_startup():
    logging.info("Bot successfully deployed with updated modules! Sending initial broadcast...")
    
    # 1. Immediate post right after deployment
    await post_to_channel()
    
    # 2. Schedule recurrent posts every 30 minutes
    scheduler.add_job(post_to_channel, 'interval', minutes=30)
    scheduler.start()

async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
