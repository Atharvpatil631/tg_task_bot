from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
import asyncio
from db import get_tasks_by_user
from datetime import datetime

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.start()

def schedule_reminder(bot: Bot, chat_id: int, task_title: str, remind_at: datetime):
    scheduler.add_job(
        send_reminder,
        'date',
        run_date=remind_at,
        args=[bot, chat_id, task_title],
        id=f"{chat_id}_{task_title}_{remind_at}"
    )

async def send_reminder(bot: Bot, chat_id: int, task_title: str):
    await bot.send_message(chat_id=chat_id, text=f"🔔 Reminder: '{task_title}' is due soon!")


