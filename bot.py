import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with token from @BotFather
CHANNEL_ID = "@ForexPulseFX"        # Your channel username or numeric ID

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
        "🧮 Use /calculator in @ForexPulseFXBot to compute your lot size!"
    ),
    (
        "🌐 **HIGH-IMPACT NEWS ALERT** 🌐\n\n"
        "Major economic data releases can cause sudden volatility spikes in major pairs.\n\n"
        "📅 Check today's high-impact news schedule using /calendar in @ForexPulseFXBot"
    )
]

# Initialize Logger & Bot
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# ---------------------------------------------------------
# CHANNEL BROADCAST FUNCTION
# ---------------------------------------------------------
async def post_to_channel():
    """Selects a random image and message, then posts to the channel."""
    try:
        image_url = random.choice(MARKET_IMAGES)
        caption_text = random.choice(POST_TEMPLATES)
        
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=image_url,
            caption=caption_text
        )
        logging.info("Successfully posted scheduled message to channel.")
    except Exception as e:
        logging.error(f"Failed to post to channel: {e}")

# ---------------------------------------------------------
# BOT COMMAND HANDLERS
# ---------------------------------------------------------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "👋 **Welcome to ForexPulse FX Bot!**\n\n"
        "Your automated trading companion for real-time market updates.\n\n"
        "⚡ Choose a command to get started:\n"
        "/signals - View active trade signals\n"
        "/market - Live market overview\n"
        "/calendar - Economic calendar updates\n"
        "/calculator - Position size calculator\n"
        "/bot - About this bot\n"
        "/vip - Premium membership details\n"
        "/support - Contact support"
    )
    await message.answer(welcome_text)

@dp.message(Command("bot"))
async def cmd_bot(message: types.Message):
    bot_info = (
        "🤖 **About ForexPulse FX Bot**\n\n"
        "I am an automated assistant powering the @ForexPulseFX community.\n\n"
        "• 📊 Automated 30-minute market updates\n"
        "• 📈 Technical analysis & signal notifications\n"
        "• 📅 News & economic event tracking\n"
        "• 🧮 Trading tools & pip calculations"
    )
    await message.answer(bot_info)

@dp.message(Command("signals"))
async def cmd_signals(message: types.Message):
    await message.answer("📊 **Active Signals:** Check @ForexPulseFX for real-time signal entries.")

@dp.message(Command("market"))
async def cmd_market(message: types.Message):
    await message.answer("📈 **Market Overview:** EUR/USD, GBP/USD, and XAU/USD showing active momentum.")

@dp.message(Command("calendar"))
async def cmd_calendar(message: types.Message):
    await message.answer("📅 **Economic Calendar:** High-impact USD news scheduled for today's session.")

@dp.message(Command("calculator"))
async def cmd_calculator(message: types.Message):
    await message.answer("🧮 **Position Calculator:** Reply with your Account Size ($) and Risk (%) to calculate risk.")

@dp.message(Command("vip"))
async def cmd_vip(message: types.Message):
    await message.answer("⭐ **VIP Access:** Unlock institutional signals. Contact admin via /support.")

@dp.message(Command("support"))
async def cmd_support(message: types.Message):
    await message.answer("💬 **Support:** For inquiries, contact @YourAdminUsername.")

# ---------------------------------------------------------
# DEPLOYMENT & LIFECYCLE HOOKS
# ---------------------------------------------------------
async def on_startup():
    logging.info("Bot successfully deployed! Sending initial broadcast...")
    
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
