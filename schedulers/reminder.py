from db import get_tasks_by_user
from datetime import datetime
from telegram import Bot
from db import get_all_users, get_tasks_by_user
from pytz import utc

async def check_reminders(application):
    bot: Bot = application.bot
    now = datetime.now(utc).strftime("%Y-%m-%d %H:%M")

    users = await get_all_users()

    for user_id, in users:
        tasks = await get_tasks_by_user(user_id)

        for task in tasks:
            task_id, title, description, category, due_date, reminder_time, status = task
            if reminder_time and status != 'Done':
                reminder_time_str = reminder_time[:16]  # remove seconds if any
                if reminder_time_str == now:
                    message = f"⏰ Reminder!\nTask: {title}\nDue: {due_date}"
                    try:
                        await bot.send_message(chat_id=user_id, text=message)
                    except Exception as e:
                        print(f"Failed to send reminder to {user_id}: {e}")