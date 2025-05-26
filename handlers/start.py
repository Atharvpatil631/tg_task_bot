from telegram import Update
from telegram.ext import ContextTypes
from db import add_user

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await add_user(user.id, user.username or "unknown")

    await update.message.reply_text(
        f"👋 Hello {user.first_name}! Welcome to your Personal To-Do List Bot.\n\n"
        "You can use this bot to manage your daily tasks and set reminders.\n\n"
        "Try using /addtask to add a new task!"
    )
