from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
)
from bd import print_bac_records, user_bac_record, print_knb_records, user_knb_record

from bd import create_user
from constants import MAINMENU, RATE


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - вся информация о сообщении
    # update.effective_user - все о пользователе
    # update.effective_message - все о сообщении
    # update.effective_chat - все о диалоге
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет, {update.effective_user.full_name}\nВыбери действие:\n/knb - камень ножницы бумага\n/bac - быки и коровы\n/xo - крестики нолики\n/rate - покажет ваш рекорды и список рекордсменов",
    )
    create_user(update)
    return MAINMENU


async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Камень Ножницы Бумага", callback_data="knb_data")],
        [InlineKeyboardButton("Быки и коровы", callback_data="bnc_data")],
        [InlineKeyboardButton("Крестики нолики", callback_data="xo_data")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите какой рекорд хотите посмотреть",
        reply_markup=markup,
    )
    return RATE


async def rate_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    if query.data == "knb_data":
        keyboard = [
            [InlineKeyboardButton("Мои рекорды", callback_data="knb_user_data")],
            [InlineKeyboardButton("Все рекорды", callback_data="records_data")],
        ]
        text = print_knb_records()

    if query.data == "knb_user_data":
        keyboard = [
            [InlineKeyboardButton("Мои рекорды", callback_data="knb_data")],
            [InlineKeyboardButton("Все рекорды", callback_data="records_data")],
        ]
        text = f'Ваш рекорд: {user_knb_record(update)}'

    elif query.data == "bnc_data":
        keyboard = [
            [InlineKeyboardButton("Мои рекорды", callback_data="bnc_user_data")],
            [InlineKeyboardButton("Все рекорды", callback_data="records_data")],
        ]
        text = print_bac_records()

    elif query.data == "bnc_user_data":
        keyboard = [
            [InlineKeyboardButton("Мои рекорды", callback_data="bnc_data")],
            [InlineKeyboardButton("Все рекорды", callback_data="records_data")],
        ]
        text = f'Ваш рекорд: {user_bac_record(update)}'

    elif query.data == "records_data":
        keyboard = [
        [InlineKeyboardButton("Камень Ножницы Бумага", callback_data="knb_data")],
        [InlineKeyboardButton("Быки и коровы", callback_data="bnc_data")],
        [InlineKeyboardButton("Крестики нолики", callback_data="xo_data")],
        ]
        text = 'Выберите рекорд, который хотите посмотреть'

    elif query.data == "xo_data":
        keyboard = [
            [InlineKeyboardButton("Мои рекорды", callback_data="xo_user_data")],
            [InlineKeyboardButton("Все рекорды", callback_data="records_data")],
        ]
        text = f'Ваш рекорд: xo_data'

    elif query.data == "xo_user_data":
        keyboard = [
            [InlineKeyboardButton("Мои рекорды", callback_data="xo_data")],
            [InlineKeyboardButton("Все рекорды", callback_data="records_data")],
        ]
        text = f'Ваш рекорд: xo_user_data'
        
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=markup)
    return RATE


