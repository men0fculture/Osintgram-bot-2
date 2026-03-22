#!/usr/bin/env python3
import os
import subprocess
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not set")
    raise ValueError("TELEGRAM_BOT_TOKEN missing")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 **Osintgram Bot Ready**\n\n"
        "Commands:\n"
        "/info <username> - Get target info\n"
        "/followers <username> - Get followers list\n"
        "/followings <username> - Get followings list\n"
        "/photos <username> - Download target photos\n"
        "/help - Show this",
        parse_mode='Markdown'
    )

async def run_command(update: Update, context: ContextTypes.DEFAULT_TYPE, cmd_name: str):
    if not context.args:
        await update.message.reply_text("Give me a target username, bhai!\nExample: /info zuck")
        return
    target = context.args[0]
    cmd = f"python3 main.py {target} --command {cmd_name}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
        output = result.stdout if result.stdout else result.stderr
        if not output:
            output = "No output or error."
        if len(output) > 4000:
            output = output[:4000] + "\n\n... (truncated)"
        await update.message.reply_text(output)
    except subprocess.TimeoutExpired:
        await update.message.reply_text("Command timed out (90s). Try again later.")
    except Exception as e:
        logger.exception("Error in command")
        await update.message.reply_text(f"Error: {str(e)[:200]}")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await run_command(update, context, "info")

async def followers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await run_command(update, context, "followers")

async def followings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await run_command(update, context, "followings")

async def photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await run_command(update, context, "photos")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("followers", followers))
    app.add_handler(CommandHandler("followings", followings))
    app.add_handler(CommandHandler("photos", photos))
    logger.info("Bot started polling...")
    app.run_polling()

if __name__ == "__main__":
    main()ain__":
    main()
