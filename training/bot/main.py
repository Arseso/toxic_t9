import asyncio
import logging
import os
import sys
from os import getenv

import psycopg2 as pg
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Bot token can be obtained via https://t.me/BotFather


# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Приветствую! \nТы в боте добавления фраз в датасет токсичной нейросети.  "
                         f"Твоя задача: написать максимально связное предложение, но в то же время с максимальной концентрацией ненормативной лексики.\n"
                         f"Есть только одно правило: использовать только буквы и знаки препинания, а то автор заебется чистить базу, а он этого не хочет :) \n"
                         f"А если серьезно, буду супер рад, если ты напишешь хотя-бы 5-10 предложений\n\n"
                         f"Можешь писать прямо следующим сообщением, и кстати, чем длиннее предложение, тем автор выше прыгает от радости, заранее благодарю.")


cur = None


def append_to_db(text):
    cur.execute(f"INSERT INTO data (sequence) VALUES ('{text}')")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        append_to_db(message.text)
        await message.answer("Обнял приподнял")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("наебка")


async def main() -> None:
    global cur

    TOKEN = os.getenv("BOT_TOKEN")

    conn = pg.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"))
    conn.autocommit = True
    cur = conn.cursor()

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
