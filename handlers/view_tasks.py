from telegram import Update
from telegram.ext import ContextTypes
from db import get_tasks_by_user

async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = await get_tasks_by_user(user_id)

    if not tasks:
        await update.message.reply_text("You have no tasks saved! Use /addtask to create one.")
        return

    message = "📋 Your tasks:\n\n"
    for task in tasks:
        task_id, title, description, category, due_date, reminder_time, status = task
        message += f"🔹 *{title}*\n"
        message += f"  Category: {category}\n"
        message += f"  Due: {due_date}\n"
        message += f"  Status: {status}\n"
        if description:
            message += f"  Description: {description}\n"
        message += "\n"

    await update.message.reply_markdown(message)

