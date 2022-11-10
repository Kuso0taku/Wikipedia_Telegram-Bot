from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.message):
    await message.reply('Привет!\nИспользуй /help')

@dp.message_handler(commands=['help'])
async def help(message: types.message):
    await message.reply('Это бот, который ищет информацию в wikipedia и отправляет ее сюда текстовым сообщением.')


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
