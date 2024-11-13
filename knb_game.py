import random

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
)

from bd import update_knb_win
from constants import KNB


async def knb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Камень", "Ножницы", "Бумага"]]

    markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, input_field_placeholder="Выбирай"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выбери кем будешь ходить",
        reply_markup=markup,
    )
    return KNB


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text

    is_win = False
    rand = random.randrange(2)
    mas = ["Камень", "Ножницы", "Бумага"]
    if text == "Камень" and mas[rand] == "Ножницы":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Я выбрал {mas[rand]}\n Ты выиграл"
        )
        is_win = True
    elif text == "Бумага" and mas[rand] == "Камень":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Я выбрал {mas[rand]}\n Ты выиграл"
        )
        is_win = True
    elif text == "Ножницы" and mas[rand] == "Бумага":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Я выбрал {mas[rand]}\n Ты выиграл"
        )
        is_win = True
    elif text == mas[rand]:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Я выбрал {mas[rand]}\n Ничья"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Я выбрал {mas[rand]}\n Ты проиграл"
        )

    update_knb_win(update, is_win)
    return await knb(update, context)
