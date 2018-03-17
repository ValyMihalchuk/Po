# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import logging
import os

TOKEN = '487702351:AAF9ZT5I_YCcw7xnju2QLVuW694VZ9f5F70'
PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN)

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hi, pussies!')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://poison-.herokuapp.com/" + TOKEN)
updater.idle()
