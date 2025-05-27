# Personal To-Do List Telegram Bot

A friendly Telegram bot to help you manage your tasks with reminders, categories, and history — all powered by Python and SQLite.

## Features

- Create, view, and remove tasks
- Categorize tasks (Work, Personal, Misc)
- Set deadlines and reminders with notifications
- View task history including completed tasks
- SQLite database for persistence
- Simple reminder scheduler
- 
## Tech Stack

- Python 3.11.5
- [python-telegram-bot](https://python-telegram-bot.org/) library
- SQLite for data persistence
- Asyncio for async operations and scheduling
## Installation

python -m venv venv

.venv\Scripts\activate

pip install -r requirements.txt

git clone https://github.com/yourusername/tg-task-bot.git

cd tg-task-bot

## Usage

Use these commands inside Telegram:

/start - Welcome message

/addtask - Add a new task (follow prompts)

/viewtasks - View your pending tasks

/removetask - Remove a task

/done - Mark task as done

/history - View all your tasks, including completed ones

## Contributing

Feel free to open issues or submit pull requests to improve the bot.

## License

This project is licensed under the MIT License.
