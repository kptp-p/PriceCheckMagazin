import os
import logging

import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from src.db.models import create_tables
from src.handlers.handlers import router


load_dotenv()


db = Dispatcher()


async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    await create_tables()
    db.include_router(router)
    await db.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Бот остановлен')
        print('Бот остановлен')
