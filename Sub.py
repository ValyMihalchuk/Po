# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import logging

import Config

updater = Updater(token=Config.token)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hi, pussies!')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
