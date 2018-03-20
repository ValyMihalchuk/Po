from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import date, datetime, timedelta
import logging
import os

TOKEN = '597287506:AAHji4feYsBmFfjFJAnxhEkROqmAYS1bjjc'
PORT = int(os.environ.get('PORT', '8443'))

updater = Updater(TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    greeting = '@' + update.message.chat.username if update.message.chat.type in {'private'} else 'pussies'
    bot.send_message(chat_id=update.message.chat_id, text='Hi, {}!\nI`m here to help you to know '
                     'the sub of the day, cause I can print it (/sub)'.format(greeting))


def help_bot(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Oh, I see, you need some help in using me.\n'
                          'Brilliant! Here are the things I can:\n{}'.
                     format(''.join([line for line in open('CommandForBot.txt', 'r', encoding='utf-8')])))


def subway(bot, update):
    subs = [sub[:-1:] for sub in open('WeekOfSubs.txt', 'r', encoding='utf-8')]
    bot.send_message(chat_id=update.message.chat_id,
                     text='And the sub of the day for today is:\n' + subs[date.weekday(date.today() + timedelta(hours=3))],
                     parse_mode=Markdown)


def time(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=(datetime.today() + timedelta(hours=3)).strftime('%H:%M\n%d %h %Y'))


def unknown(bot, update):
    greeting = '@' + update.message.chat.username if update.message.chat.type in {'private'} else 'Babes'
    bot.send_message(chat_id=update.message.chat_id,
                     text='{}, it`s cool, you`re writing me, but I '
                     'can`t do the thing you want me to do :C\nUse /help for more details'.format(greeting))


def text(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Oops! I`m not programmed to "touch" your text, sorry about it!')


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help_bot)
dispatcher.add_handler(help_handler)

subway_handler = CommandHandler('sub', subway)
dispatcher.add_handler(subway_handler)

time_handler = CommandHandler('time', time)
dispatcher.add_handler(time_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(text_handler)


updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://warm-tor-12956.herokuapp.com/" + TOKEN)
updater.idle()
