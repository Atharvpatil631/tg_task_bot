from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
from db import add_task_to_db

# States
TITLE, DESCRIPTION, CATEGORY, DUE_DATE, REMINDER = range(5)

async def start_add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 What’s the task title?")
    return TITLE

async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['title'] = update.message.text
    await update.message.reply_text("📄 Enter a short description (or type 'skip'):")
    return DESCRIPTION

async def get_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    desc = update.message.text
    context.user_data['description'] = "" if desc.lower() == "skip" else desc
    reply_markup = ReplyKeyboardMarkup([["Work", "Personal", "Misc"]], one_time_keyboard=True)
    await update.message.reply_text("📂 Choose a category:", reply_markup=reply_markup)
    return CATEGORY

async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['category'] = update.message.text
    await update.message.reply_text("⏰ Due date? (Format: YYYY-MM-DD HH:MM)")
    return DUE_DATE

async def get_due_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['due_date'] = update.message.text
    await update.message.reply_text("⏳ Reminder time? (same format or type 'skip'):")
    return REMINDER

async def get_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reminder = update.message.text
    context.user_data['reminder_time'] = None if reminder.lower() == "skip" else reminder

    # Save to DB
    user = update.effective_user
    await add_task_to_db(user.id, context.user_data)

    await update.message.reply_text("✅ Task saved successfully!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Task creation cancelled.")
    return ConversationHandler.END

