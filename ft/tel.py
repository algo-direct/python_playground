import logging
import datetime
import sys
import asyncio
from telegram import Update
from telegram.ext import Updater, ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"%%%%%%%%%%%%%%%%%%%%")
    print(f"chat_id:{update.effective_chat.id}")
    print(f"====================")
    print(f"eff:{update.effective_chat}")
    print(f"====================")
    print(f"update:{update}")
    print(f"####################")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

if __name__ == '__main__':
    #application = ApplicationBuilder().token('5809560751:AAFiEn1Ti6z2v00Lecydny1SNS_owLVYBB4').build()
    #asyncio.run(application.bot.sendMessage(chat_id='5499947057', text='Hello there! ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    #sys.exit(0)
    #pass
    #updater = Updater('5809560751:AAFiEn1Ti6z2v00Lecydny1SNS_owLVYBB4', use_context=False)
    #updater.dispatcher.bot.sendMessage(chat_id='5499947057', text='Hello there!')
    #pass

    application = ApplicationBuilder().token('5809560751:AAFiEn1Ti6z2v00Lecydny1SNS_owLVYBB4').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    start_handler = CommandHandler('s', start)
    application.add_handler(start_handler)
    
    application.run_polling()
