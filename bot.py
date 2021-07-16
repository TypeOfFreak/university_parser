import MIREA
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
from dotenv import load_dotenv
load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_answer(msg: types.Message):
    await msg.reply('Hi!')

@dp.message_handler(commands=['rate'])
async def start_answer(msg: types.Message):
    await msg.reply('Downloading...')
    await bot.send_message(msg.from_user.id, MIREA.get_my_places())

if __name__ == '__main__':
    executor.start_polling(dp)