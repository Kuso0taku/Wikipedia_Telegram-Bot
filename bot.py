from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.types import ParseMode

import wikipedia

from config import TOKEN


language = "ru"
wikipedia.set_lang(language)

with open('text.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()[1:]
    help = ''
    for line in lines:
        help += line

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nИспользуй /help')

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(help)

@dp.message_handler(commands=['summary'])
async def wikipedia_summary_command(message: types.Message):
    await bot.send_message(message.from_user.id, wikipedia.page(message.text[9:]).summary, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['sentence'])
async def wikipedia_summary_command(message: types.Message):
    msg = message.text.split()[0]
    num = msg[1]
    theme = ' '.join(msg[2:])
    await bot.send_message(message.from_user.id, wikipedia.summary(theme, sentences=num), parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['search'])
async def wikipedia_summary_command(message: types.Message):
    await bot.send_message(message.from_user.id, [i for i in wikipedia.search(message.text[8:])], parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['search'])
async def wikipedia_summary_command(message: types.Message):
    await bot.send_message(message.from_user.id, wikipedia.page(message.text[9:]).title, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['content'])
async def wikipedia_summary_command(message: types.Message):
    await bot.send_message(message.from_user.id, wikipedia.page(message.text[9:]).content, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['references'])
async def wikipedia_summary_command(message: types.Message):
    await bot.send_message(message.from_user.id, wikipedia.page(message.text[9:]).references, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['links'])
async def wikipedia_summary_command(message: types.Message):
    await bot.send_message(message.from_user.id, wikipedia.page(message.text[9:]).links, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, wikipedia.summary(msg.text, sentences=3), parse_mode=ParseMode.MARKDOWN)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
