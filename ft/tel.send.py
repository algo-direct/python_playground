import logging
import datetime
import sys
import time
from time import gmtime, strftime
import asyncio
import uuid
import json
import os
from telegram import Update
from telegram.ext import Updater, ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    # level=logging.DEBUG,
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s.%(msecs)03d pid:%(process)d; %(levelname)s: [%(filename)s:%(lineno)s - %(funcName)25s() ] %(message)s",
    datefmt="%Y-%m-%d_%H:%M:%S",
)


def date_to_str(d):
    return d.strftime("%Y-%m-%d_%H:%M:%S.%f")


def now_to_str():
    return date_to_str(datetime.datetime.now())


logging.info(f"start {now_to_str()}")

if __name__ == "__main__":
    token = open("tel_bot_trade_notif.token.txt").read()[:-1]
    application = ApplicationBuilder().token(token).build()
    asyncio.run(application.bot.sendMessage(chat_id='5499947057', text=f"Hello there! {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {sys.argv[1]}"))
    sys.exit(0)
    # pass
    # updater = Updater('5809560751:AAFiEn1Ti6z2v00Lecydny1SNS_owLVYBB4', use_context=False)
    # updater.dispatcher.bot.sendMessage(chat_id='5499947057', text='Hello there!')
    # pass

    #token = open("tel_bot_trade_notif.token.txt").read()[:-1]
    #logging.info(f"######################## token:{token} ####")
    #application = ApplicationBuilder().token(token).build()

    # asyncio.run(
    #     application.bot.sendMessage(
    #         chat_id="5499947057",
    #         text="BOT started! " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     )
    # )
