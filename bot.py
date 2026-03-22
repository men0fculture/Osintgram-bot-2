import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yo! Osintgram bot ready. Use /info <username> 😈")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Target username de, bhai!")
        return
    target = context.args[0]
    cmd = f"python3 main.py {target} --command info"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout if result.stdout else result.stderr
    await update.message.reply_text(output[:4096])

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.run_polling()

if __name__ == "__main__":
    main()
