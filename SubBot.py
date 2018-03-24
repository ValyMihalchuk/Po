# Strukov Alexandr


# -*- coding: utf-8 -*-


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date, datetime, timedelta
import logging
import os

import botan

TOKEN = '597287506:AAHji4feYsBmFfjFJAnxhEkROqmAYS1bjjc'
YANDEX_TOKEN = '4bf3b480-3ded-47f3-8544-723485c9b3ab'
PORT = int(os.environ.get('PORT', '8443'))

updater = Updater(TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

lingua_franca = 'en'

translate = {
    'ru': {
        'button': ['Выбранный {}: {}'],
        'language': [['Русский', 'Английский'],
                     ['язык Русский', 'язык Английский'],
                     ['Выберите язык: ']],
        'start': [['чуваки'],
                  ['Привет, {}!\nЯ был создан для того, чтобы Вы не вспоминали,'
                   ' какой сегдоня Саб для, потому что я могу его напечатать (/sub)'],
                  ['Если Вам некомфортно читать русский язык, Вы можете изменить язык']],
        'help': ['Ого, Вам нужна помощь, чтобы разобраться в том, как меня использовать.\n'
                 'Отлично! Вот список того, что я умею:\n{}'],
        'subway': ['И Саб дня сегодня:\n'],
        'unknown': [['Ребятки'],
                    ['{} классно, что Вы пишите мне, но я не могу сделать то, что Вы просите :С\n'
                     'Используйте /help для большей информации']],
        'text': ['Ботва! Я не могу *трогать* Ваш текст - извините!']
    },
    'en': {
        'button': ['Selected {}: {}'],
        'language': [['Russian', 'English'],
                     ['language Russian', 'language English'],
                     ['Choose the language: ']],
        'start': [['pussies'],
                  ["Hi, {}!\nI'm here to help you to know "
                   "the sub of the day, cause I can print it (/sub)"],
                  ["If it's uncomfortable for you to read in English, you can switch the language to Russian"]],
        'help': ['Oh, I see, you need some help in using me.\n'
                 'Brilliant! Here are the things I can:\n{}'],
        'subway': ['And the sub of the day for today is:\n'],
        'unknown': [['Babes'],
                    ["{}, it's cool, you're writing me, but I "
                    "can't do the thing you want me to do :C\nUse /help for more details"]],
        'text': ["Oops! I'm not programmed to *touch* your text, sorry about it!"]
    }
}


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)

    return menu


def button(bot, update):
    global lingua_franca

    query = update.callback_query
    option, choice = query.data.split()
    n = 0

    if option in {'language', 'язык'}:
        if choice in {'English', 'Английский'}:
            lingua_franca = 'en'
            n = 1
        elif choice in {'Russian', 'Русский'}:
            lingua_franca = 'ru'
            n = 0
        option, choice = translate[lingua_franca]['language'][1][n].split()

    bot.edit_message_text(text=translate[lingua_franca]['button'][0].format(option, choice),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def language(bot, update):
    button_list = [
        InlineKeyboardButton(translate[lingua_franca]['language'][0][0], callback_data=translate[lingua_franca]['language'][1][0]),
        InlineKeyboardButton(translate[lingua_franca]['language'][0][1], callback_data=translate[lingua_franca]['language'][1][1])
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

    bot.send_message(chat_id=update.message.chat_id,
                     text=translate[lingua_franca]['language'][2][0],
                     reply_markup=reply_markup)

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'language')


def start(bot, update):
    greeting = '@' + update.message.chat.username if update.message.chat.type in {'private'} else translate[lingua_franca]['start'][0][0]

    bot.send_message(chat_id=update.message.chat_id,
                     text=translate[lingua_franca]['start'][1][0].format(greeting))
    bot.send_message(chat_id=update.message.chat_id,
                     text=translate[lingua_franca]['start'][2][0])

    language(bot, update)

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'start')


def help_bot(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=translate[lingua_franca]['help'][0].format(
                         ''.join([line for line in open('CommandForBot.txt', 'r', encoding='utf-8')])))

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'help')


def subway(bot, update):
    number_of_day = date.weekday(date.today() +
                    timedelta(days=(datetime.today() + timedelta(hours=3)).day > datetime.today().day))
    subs = [sub[:-1:] for sub in open('WeekOfSubs{}.txt'.format(lingua_franca.capitalize()), 'r', encoding='utf-8')][number_of_day]

    bot.send_message(chat_id=update.message.chat_id,
                     text=translate[lingua_franca]['subway'][0] + subs,
                     parse_mode='Markdown',
                     disable_web_page_preview=True)
    bot.send_photo(chat_id=update.message.chat_id,
                   photo=open(fr'Images/{number_of_day}.png', 'rb'))

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'sub')


def time(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=(datetime.today() + timedelta(hours=3)).strftime('%H:%M\n%d %h %Y'))

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'time')


def unknown(bot, update):
    greeting = '@' + update.message.chat.username if update.message.chat.type in {'private'} else translate[lingua_franca]['unknown'][0][0]

    bot.send_message(chat_id=update.message.chat_id,
                     text=translate[lingua_franca]['unknown'][1][0].format(greeting))

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'wrong command')


def text(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=translate[lingua_franca]['text'][0],
                     parse_mode='Markdown')

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'just text')


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


language_handler = CommandHandler('language', language)
dispatcher.add_handler(language_handler)

button_handler = CallbackQueryHandler(button)
dispatcher.add_handler(button_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help_bot)
dispatcher.add_handler(help_handler)

subway_handler = CommandHandler('sub', subway)
dispatcher.add_handler(subway_handler)

time_handler = CommandHandler('time', time)
dispatcher.add_handler(time_handler)

text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(text_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.dispatcher.add_error_handler(error)

 updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
 updater.bot.set_webhook("https://warm-tor-12956.herokuapp.com/" + TOKEN)
 updater.idle()
