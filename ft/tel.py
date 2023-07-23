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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"%%%%%%%%%%%%%%%%%%%%")
    print(f"chat_id:{update.effective_chat.id}")
    print(f"====================")
    print(f"eff:{update.effective_chat}")
    print(f"====================")
    print(f"update:{update}")
    print(f"####################")
    print(f"update.message.text:{update.message.text}")
    print(f"####################")

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"I'm a bot, please talk to me! {update.message.text}"
    )


DEFAULT_TIMEOUT = "3650d"


def get_result_str(cmd_id):
    exit_code_file_path = os.path.join(os.getcwd(), "cmd_runner", "output", f"{cmd_id}_exit_code.txt")
    stdout_file_path = os.path.join(os.getcwd(), "cmd_runner", "output", f"{cmd_id}_stdout.txt")
    stderr_file_path = os.path.join(os.getcwd(), "cmd_runner", "output", f"{cmd_id}_stderr.txt")
    result_str = ""
    if os.path.exists(stdout_file_path):
        if os.path.exists(exit_code_file_path):
            result = {}
            result["exit_code"] = open(exit_code_file_path).read()
            if result["exit_code"] != "0":
                result["stdout"] = open(stdout_file_path).read()
                result["stderr"] = open(stderr_file_path).read()
                result_str = json.dumps(result, indent=2)
            else:
                result_str = open(stdout_file_path).read()
            if not result_str:
                result_str = f"Exit code: {result['exit_code']}"
        else:
            result_str = open(stdout_file_path).read()
    else:
        result_str = "nothing in stdout"
    return result_str


async def run_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"####################")
    logging.info(f"update.message.text:{update.message.text}")
    logging.info(f"####################")
    input_str = update.message.text[3:]
    input_tokens = input_str[: input_str.find("cmd:")]
    cmd_str = input_str[input_str.find("cmd:") + 4 :]
    logging.info(f"input_str:{input_str}")
    logging.info(f"input_tokens:{input_tokens}")
    input_tokens = input_tokens.split(":")
    logging.info(f"input_tokens:{input_tokens}")
    timeout = DEFAULT_TIMEOUT
    for t in input_tokens:
        if not t:
            continue
        t = t.split("=")
        if len(t) < 2:
            continue
        if t[0] == "timeout":
            timeout = t[1]
    cmd_id = now_to_str()
    cmd = {"timeout": timeout, "cmd_id": cmd_id, "command": cmd_str}
    cmd_json = json.dumps(cmd, indent=2)
    logging.info(f"cmd: {cmd_json}")
    cmd_file_name = f"cmd_runner/todo/{cmd_id}.json"
    cmd_file = open(cmd_file_name, "w")
    cmd_file.write(cmd_json)
    cmd_file.close()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Wrote {cmd_file_name} file! {update.message.text}, \n json:{cmd_json}",
    )
    

    exit_code_file_path = os.path.join(os.getcwd(), "cmd_runner", "output", f"{cmd_id}_exit_code.txt")
    logging.info(f"exit_code_file_path: {exit_code_file_path}")
    if time == DEFAULT_TIMEOUT:
        slp = 10
        logging.info(f"no timeout provided, running for max {slp} seconds")
        time.sleep(slp)
    else:
        start_time = datetime.datetime.now()
        while True:
            end_time = datetime.datetime.now()
            elapsed = end_time - start_time
            if elapsed > datetime.timedelta(minutes=1):
                logging.warn(f"command ran for more than 1 minute")
                break
            time.sleep(0.2)
            if os.path.exists(exit_code_file_path):
                logging.info("Found exit code file")
                time.sleep(0.4)
                break
    result_str = get_result_str(cmd_id)
    logging.info(f"result_str: {result_str}")
    if len(result_str) > 4096:
        logging.info(f"too big msg: {len(result_str)}")
    while len(result_str) > 0:
        logging.info(f"remaining result size: {len(result_str)}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{result_str[:4096]}")
        result_str = result_str[4096:]

    # await context.bot.send_message( 10.17.143.157
    #     chat_id=update.effective_chat.id, text=f"I'm a bot, please talk to me! {update.message.text}"
    # )


if __name__ == "__main__":
    # application = ApplicationBuilder().token('5809560751:AAFiEn1Ti6z2v00Lecydny1SNS_owLVYBB4').build()
    # asyncio.run(application.bot.sendMessage(chat_id='5499947057', text='Hello there! ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # sys.exit(0)
    # pass
    # updater = Updater('5809560751:AAFiEn1Ti6z2v00Lecydny1SNS_owLVYBB4', use_context=False)
    # updater.dispatcher.bot.sendMessage(chat_id='5499947057', text='Hello there!')
    # pass

    token = open("tel_bot_trade_notif.token.txt").read()[:-1]
    #logging.info(f"######################## token:{token} ####")
    application = ApplicationBuilder().token(token).build()

    # asyncio.run(
    #     application.bot.sendMessage(
    #         chat_id="5499947057",
    #         text="BOT started! " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     )
    # )
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    start_handler = CommandHandler("s", start)
    application.add_handler(start_handler)
    run_cmd_handler = CommandHandler("c", run_cmd)
    application.add_handler(run_cmd_handler)

    # application.start()

    application.run_polling(timeout=60)
    # while True:
    #     logging.debug("tick")
    #     time.sleep(10)

    # Update(
    #     message=Message(
    #         channel_chat_created=False,
    #         chat=Chat(first_name='Ashish', id=5499947057, last_name='Tyagi', type=<ChatType.PRIVATE>),
    #             date=datetime.datetime(2023, 7, 23, 4, 45, 55, tzinfo=datetime.timezone.utc),
    #             delete_chat_photo=False,
    #             entities=(MessageEntity(length=2, offset=0, type=<MessageEntityType.BOT_COMMAND>),),
    #             from_user=User(first_name='Ashish', id=5499947057, is_bot=False, language_code='en', last_name='Tyagi'),
    #             group_chat_created=False,
    #             message_id=52,
    #             supergroup_chat_created=False,
    #             text='/s'), update_id=556840398)
# ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDj2lB82NnW3MkyEq5vk7U41+RPW3mvyxU2HO6GPvxGoofAlYcHw1Sj/vLmNURvKrl/7iFTs9dSL2ZfBxEh4xYw3YH3NDHdReZJprkr4wniki8Ob8Ak7Pk+I653ajBq4Mtk2smcShxjNPohm8IClHalR48G/WkLco6yyX2eZlIxkGap8Ko0unN6PpkiWy0dH/zOOWhB1ybxrSFrE+jRK6Gk2lEXCNRzwKSLv1Fo6RfBmAeW8OJK6k5HimzWMAl6J91uvr5VlWJqK6dvu3ihNuyrOh3nR+NRfw0S6XmORHvSDO3twa32k87IV1e+Yg0zBs89z4Qy2vAVG0Q9avHyuk3hq/aBdOMrxZo4IBNxpX6T8qXJKX32xvYPh7WLpMRKVsvOcPaCKIKxYCCGQyIoS1dNclOI57ZJ6gR2M3pLprcg8vjNQAULfiQlO6DR8doyF38cgXGKem6Hvc95aNUP83Bjrq+pkv+bq6/vofnVVmM2uevUPvuebGk4aLb35MfGo+E= invaeg_bm_1@invaeg-bm-1-Compaq-Presario-C700
