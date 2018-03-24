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


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)

    return menu


def button(bot, update):
    query = update.callback_query
    option, choice = query.data.split()

    apology = "Sorry, it was a joke, due to the fact, that I can't fix some bugs in translating );"

    bot.edit_message_text(text=apology if option == 'language' else "Chosen {}: {}".format(option, choice),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def language(bot, update):
    button_list = [
        InlineKeyboardButton('Russian', callback_data='language Russian'),
        InlineKeyboardButton('English', callback_data='language English')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

    bot.send_message(chat_id=update.message.chat_id,
                     text='Choose the language: ',
                     reply_markup=reply_markup)

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'language')


def start(bot, update):
    greeting = '@' + update.message.chat.username if update.message.chat.type in {'private'} else 'pussies'

    bot.send_message(chat_id=update.message.chat_id,
                     text="Hi, {}!\nI'm here to help you to know "
                          "the sub of the day, cause I can print it (/sub)".format(greeting))
    bot.send_message(chat_id=update.message.chat_id,
                     text="If it's uncomfortable for you to read in English, "
                          "you can switch the language to Russian")

    language(bot, update)

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'start')


def help_bot(bot, update):
    comands = [line for line in open('CommandForBot.txt', 'r', encoding='utf-8')]
    bot.send_message(chat_id=update.message.chat_id,
                     text='Oh, I see, you need some help in using me.\n'
                          'Brilliant! Here are the things I can:\n{}'.format(''.join(comands)))

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'help')


def subway(bot, update):
    number_of_day = date.weekday(date.today() +
                    timedelta(days=(datetime.today() + timedelta(hours=3)).day > datetime.today().day))
    subs = [sub[:-1:] for sub in open('WeekOfSubsEn.txt', 'r', encoding='utf-8')][number_of_day]

    bot.send_message(chat_id=update.message.chat_id,
                     text='And the sub of the day for today is:\n' + subs,
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
    greeting = '@' + update.message.chat.username if update.message.chat.type in {'private'} else 'Babes'

    bot.send_message(chat_id=update.message.chat_id,
                     text="{}, it's cool, you're writing me, but I can't do the thing"
                          " you want me to do :C\nUse /help for more details".format(greeting))

    botan.track(YANDEX_TOKEN, update.message.chat.id, update.message, 'wrong command')


def text(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Oops! I'm not programmed to *touch* your text, sorry about it!",
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

updater.start_polling()

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://warm-tor-12956.herokuapp.com/" + TOKEN)
updater.idle()
