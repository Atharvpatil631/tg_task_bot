from telegram import Update
from telegram.ext import ContextTypes
from db import get_task_history
from db import get_task_history

async def show_task_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = await get_task_history(user_id)

    if not tasks:
        await update.message.reply_text("No task history found.")
        return

    message = "📜 Your Task History:\n\n"
    for task in tasks:
        title, category, due_date, status = task
        message += (
            f"📌 {title}\n"
            f"   📂 Category: {category}\n"
            f"   🕒 Due: {due_date}\n"
            f"   ✅ Status: {status}\n\n"
        )

    await update.message.reply_text(message)

