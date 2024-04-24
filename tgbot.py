import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from main import consume_link

# Load .env and get the value of "TOKEN"
load_dotenv()
TOKEN = os.getenv("TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):
    
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>!")
    await bot.send_message(message.from_user.id,f"Я Споти-Яндекс бот. \n\nПришли мне ссылку на трек на Яндекс музыке (вида https://music.yandex.ru/album/1111111/track/1111111), а я пришлю тебе ссылку на этот трек в Спотифае. \n\nИли наоборот - пришли мне ссылку на трек в Спотифае и я постараюсь найти его в Яндексе 😏\n\n<tg-spoiler>Если мне не удастся найти трек (например, потому что в Яндекс музыке нет зарубежных релизов последних лет), я постараюсь найти альбом или артиста.</tg-spoiler>")
    
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Принял, ищу 👀")
    given_link = message.text

    try:
        new_link = consume_link(given_link)
        await message.answer(f"{new_link}")
    except:
        await message.answer(f"К сожалению, не найдено. Либо песни нет на этом стриминге, либо мы не смогли ее найти(")

async def main() -> None:

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Don't need pending updates so drop them:
    await bot.delete_webhook(drop_pending_updates=True)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())