from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.types import ParseMode

import wikipedia

from config import TOKEN


language = 'en'

with open('text.txt', 'r', encoding='UTF-8') as f:
    lines = f.read().split('\n\n\n')
    en, ru = lines
    en = en.split('\n')
    ru = ru.split('\n')

    start_en = ''
    start_ru = ''
    for i in range(3, 5, 2):
        start_en += en[i]
        start_ru += ru[i]

    help_en = ''
    help_ru = ''
    for i in '\n'.join(en[7:]):
        help_en += i
    for i in '\n'.join(ru[7:]):
        help_ru += i

with open('language.txt', 'r', encoding='UTF-8') as f:
    language = f.read()

wikipedia.set_lang(language)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    start = start_ru
    if language == 'en':
        start = start_en

    await message.reply(start)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    help = help_ru
    if language == 'en':
        help = help_en

    await message.reply(help)

@dp.message_handler(commands=['switchLang'])
async def switch_language(message: types.Message):
    lang = {'ru': 'en', 'en': 'ru'}[language]
    with open('language.txt', 'w', encoding='UTF-8') as f:
        f.write(lang)

    if lang == 'ru':
        lang = 'en'
        msg = 'Done! Please, refresh the bot to apply changes'
    else:
        lang = 'ru'
        msg = 'Готово! Пожалуйста, обновите бота, чтобы применить изменения'

    await message.reply(msg)


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

@dp.message_handler(commands=['title'])
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
