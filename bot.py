from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.types import ParseMode

import wikipedia

from config import TOKEN


language = 'en'
wikipedia.set_lang(language)

with open('text.txt', 'r', encoding='UTF-8') as f:
    lines = f.read().split('\n\n\n')
    en, ru = lines
    line, num = en, -1
    if language == 'ru':
        line, num = ru, len(line) + 1
    line = line.split('\n')

    start = '\n'.join(line[3+num:5+num])

    help = '\n'.join(line[7+num:19+num])

    wrong = line[21+num]

#with open('language.txt', 'r', encoding='UTF-8') as f:
#    language = f.read()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(start)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(help)

#@dp.message_handler(commands=['switchLang'])
#async def switch_language(message: types.Message):
#    lang = {'ru': 'en', 'en': 'ru'}[language]
#    with open('language.txt', 'w', encoding='UTF-8') as f:
#        f.write(lang)

#    if lang == 'ru':
 #       lang = 'en'
#        msg = 'Done! Please, refresh the bot to apply changes'
 #   else:
 #       lang = 'ru'
 #       msg = 'Готово! Пожалуйста, обновите бота, чтобы применить изменения'

 #   await message.reply(msg)


@dp.message_handler(commands=['summary'])
async def wikipedia_summary_command(message: types.Message):
    command = wikipedia.page(message.text[9:]).summary
    try:
        answer = command
    except:
        answer = wrong
    await bot.send_message(message.from_user.id, answer, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['sentence'])
async def wikipedia_summary_command(message: types.Message):
    msg = message.text.split()[0]
    num = msg[1]
    theme = ' '.join(msg[2:])
    command = wikipedia.summary(theme, sentences=num)
    try:
        answer = command
    except:
        answer = wrong
    await bot.send_message(message.from_user.id, answer, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['search'])
async def wikipedia_summary_command(message: types.Message):
    command = [i for i in wikipedia.search(message.text[8:])]
    try:
        answer = command
    except:
        answer = wrong
    await bot.send_message(message.from_user.id, answer, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['title'])
async def wikipedia_summary_command(message: types.Message):
    command = wikipedia.page(message.text[7:]).title
    try:
        answer = command
    except:
        answer = wrong
    await bot.send_message(message.from_user.id, answer, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['content'])
async def wikipedia_summary_command(message: types.Message):
    command = wikipedia.page(message.text[9:]).content
    try:
        answer = command
    except:
        answer = wrong
    await bot.send_message(message.from_user.id, answer, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['references'])
async def wikipedia_summary_command(message: types.Message):
    command = wikipedia.page(message.text[12:]).references
    try:
        answer = command
    except:
        answer = wrong
    await bot.send_message(message.from_user.id, answer, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['links'])
async def wikipedia_summary_command(message: types.Message):
    command = wikipedia.page(message.text[7:]).links
    try:
        answer = command
    except:
        answer = wrong
    await bot.send_message(message.from_user.id, answer, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    command = wikipedia.summary(msg.text, sentences=3)
    try:
        answer = command
    except:
        answer = wrong
    await bot.send_message(msg.from_user.id, answer, parse_mode=ParseMode.MARKDOWN)

def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
