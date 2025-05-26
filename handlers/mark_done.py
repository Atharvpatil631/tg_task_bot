from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from db import get_tasks_by_user, mark_task_done

async def mark_done_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = await get_tasks_by_user(user_id)

    pending_tasks = [task for task in tasks if task[6] != 'Done']  # task[6] = status

    if not pending_tasks:
        await update.message.reply_text("🎉 All your tasks are already marked as done!")
        return

    buttons = [
        [InlineKeyboardButton(task[1], callback_data=str(task[0]))]  # task[1] = title
        for task in pending_tasks
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("✅ Select a task to mark as done:", reply_markup=keyboard)

async def mark_done_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    task_id = int(query.data)
    user_id = query.from_user.id

    await mark_task_done(task_id, user_id)
    await query.edit_message_text("✅ Task marked as done!")
