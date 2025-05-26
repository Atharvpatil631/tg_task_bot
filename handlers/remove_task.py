from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from db import get_tasks_by_user, delete_task

async def remove_task_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = await get_tasks_by_user(user_id)

    if not tasks:
        await update.message.reply_text("You have no tasks to remove!")
        return

    buttons = [
        [InlineKeyboardButton(task[1], callback_data=str(task[0]))]  # task[0]=task_id, task[1]=title
        for task in tasks
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Select a task to remove:", reply_markup=keyboard)

async def remove_task_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    task_id = int(query.data)
    user_id = query.from_user.id

    await delete_task(task_id, user_id)
    await query.edit_message_text("✅ Task removed successfully!")

