import MIREA
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_answer(msg: types.Message):
    await msg.reply('pls enter /rating')

@dp.message_handler(commands=['rating'])
async def start_answer(msg: types.Message):
    await msg.reply('Downloading...')
    await bot.send_message(msg.from_user.id, MIREA.get_my_places())
if __name__ == '__main__':
    executor.start_polling(dp)