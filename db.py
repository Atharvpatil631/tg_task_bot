import aiosqlite
import datetime

DB_NAME = "tasks.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # Create users table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            last_login TIMESTAMP
        )
        """)

        # Create tasks table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            due_date TEXT,
            reminder_time TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)
        await db.commit()

async def add_user(user_id: int, username: str):
    now = datetime.datetime.now().isoformat()
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT OR REPLACE INTO users (user_id, username, last_login)
            VALUES (?, ?, ?)
        """, (user_id, username, now))
        await db.commit()
async def add_task_to_db(user_id, data):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO tasks (user_id, title, description, category, due_date, reminder_time, status)
            VALUES (?, ?, ?, ?, ?, ?, 'pending')
        """, (
            user_id,
            data['title'],
            data['description'],
            data['category'],
            data['due_date'],
            data['reminder_time']
        ))
        await db.commit()
async def get_tasks_by_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT task_id, title, description, category, due_date, reminder_time, status
            FROM tasks
            WHERE user_id = ?
            ORDER BY due_date
        """, (user_id,))
        rows = await cursor.fetchall()
        await cursor.close()
        return rows
async def delete_task(task_id, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM tasks WHERE task_id = ? AND user_id = ?", (task_id, user_id))
        await db.commit()
async def mark_task_done(task_id, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            UPDATE tasks
            SET status = 'Done'
            WHERE task_id = ? AND user_id = ?
        """, (task_id, user_id))
        await db.commit()
async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT DISTINCT user_id FROM tasks")
        rows = await cursor.fetchall()
        return rows
async def get_task_history(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT title, category, due_date, status
            FROM tasks
            WHERE user_id = ?
            ORDER BY due_date
        """, (user_id,))
        rows = await cursor.fetchall()
        return rows
