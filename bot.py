import asyncio
from telegram.ext import Application, CommandHandler, ConversationHandler,CallbackQueryHandler ,MessageHandler, filters

from handlers.start import start_command
from handlers.add_task import (
    start_add_task,
    get_title,
    get_description,
    get_category,
    get_due_date,
    get_reminder,
    cancel
)
from db import init_db
from handlers.view_tasks import view_tasks
from handlers.remove_task import remove_task_start, remove_task_confirm
from handlers.mark_done import mark_done_start, mark_done_confirm
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from schedulers.reminder import check_reminders
from pytz import utc
from handlers.history import show_task_history
from handlers.history import show_task_history

BOT_TOKEN = "7622588651:AAGMzrNe6uuxMGlki7V5Nktm3bRn7ZsPTeQ"  # <-- Put your bot token here


async def run_bot():
    # Initialize DB
    await init_db()

    # Create the Telegram application
    app = Application.builder().token(BOT_TOKEN).build()

    # Add /start command handler
    app.add_handler(CommandHandler("start", start_command))

    # Create the conversation handler for /addtask
    add_task_conv = ConversationHandler(
        entry_points=[CommandHandler("addtask", start_add_task)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_description)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_category)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_due_date)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reminder)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    # Add the conversation handler to the app
    app.add_handler(add_task_conv)
    app.add_handler(CommandHandler("viewtasks", view_tasks))
    app.add_handler(CommandHandler("removetask", remove_task_start))
    app.add_handler(CallbackQueryHandler(remove_task_confirm))
    app.add_handler(CommandHandler("done", mark_done_start))
    app.add_handler(CallbackQueryHandler(mark_done_confirm))
    app.add_handler(CommandHandler("history", show_task_history))
    app.add_handler(CommandHandler("history", show_task_history))

        # Set up the scheduler
    scheduler = AsyncIOScheduler(timezone=utc)
    scheduler.add_job(check_reminders, "interval", minutes=1, args=[app])
    scheduler.start()
    
    print("✅ Bot is running...")

    # Start the bot properly
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # Keep bot running
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            print("⚠️ Event loop already running, scheduling bot...")
            loop.create_task(run_bot())
        else:
            loop.run_until_complete(run_bot())
    except RuntimeError:
        asyncio.run(run_bot())
