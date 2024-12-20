import datetime
import logging
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)

import pytz
from datetime import time
from bd import create_db
from bulls_and_cows import bac, bulls_and_cows
from constants import BAC, KNB, MAINMENU, XO_GAME, RATE
from knb_game import knb, text
from xo_game import x_o_game, xo
from common_func import start, rate, rate_answer, reminder_to_play

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)



if __name__ == "__main__":
    TOKEN = os.getenv('TOKEN')

    application = ApplicationBuilder().token(TOKEN).build()
    conv_hand = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [
                CommandHandler("knb", knb),
                CommandHandler("bac", bac),
                CommandHandler("xo", xo),
                CommandHandler("rate", rate),
            ],
            KNB: [MessageHandler(filters.TEXT & ~filters.COMMAND, text)],
            BAC: [MessageHandler(filters.TEXT & ~filters.COMMAND, bulls_and_cows)],
            XO_GAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, x_o_game)],
            RATE: [CallbackQueryHandler(rate_answer)]
        },
        fallbacks=[
            CommandHandler("start", start),
            CommandHandler("rate", rate)
        ],
    )
    # application.job_queue.run_daily()
    application.job_queue.run_daily(
        reminder_to_play,  # Функция для выполнения
        time=time(hour=12, minute=0, tzinfo=pytz.timezone('Etc/GMT-3'))  # Время рассылки: 12:00
    )

    application.add_handler(conv_hand)

    create_db()
    application.run_polling()
