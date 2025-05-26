from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import aiosqlite
from telegram import Bot
from db import DB_NAME
import logging
from pytz import timezone

scheduler = AsyncIOScheduler()

async def check_reminders(app_bot: Bot):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT task_id, user_id, title FROM tasks
            WHERE reminder_time IS NOT NULL AND status = 'pending' AND reminder_time <= ?
        """, (now,))
        tasks_to_remind = await cursor.fetchall()

        for task_id, user_id, title in tasks_to_remind:
            try:
                await app_bot.send_message(chat_id=user_id, text=f"🔔 Reminder: *{title}*", parse_mode="Markdown")
                await db.execute("UPDATE tasks SET reminder_time = NULL WHERE task_id = ?", (task_id,))
            except Exception as e:
                logging.warning(f"Failed to send reminder to {user_id}: {e}")

        await db.commit()

def start_scheduler(app_bot: Bot):
    scheduler.add_job(check_reminders, "interval", minutes=1, args=[app_bot])
    scheduler.start()
from db import get_tasks_by_user
from datetime import datetime
from scheduler import schedule_reminder

async def schedule_existing_reminders(bot):
    # Loop through all users and schedule their future reminders
    import aiosqlite
    async with aiosqlite.connect("data/tasks.db") as db:
        async with db.execute("SELECT user_id, title, reminder_time FROM tasks WHERE status='Pending' AND reminder_time IS NOT NULL") as cursor:
            async for row in cursor:
                user_id, title, reminder_time_str = row
                try:
                    remind_at = datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
                    if remind_at > datetime.now():
                        schedule_reminder(bot, user_id, title, remind_at)
                except Exception as e:
                    print(f"⛔ Failed to schedule reminder for task '{title}': {e}")

