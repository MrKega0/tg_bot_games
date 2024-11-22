from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
)
from bd import print_bac_records, user_bac_record, print_knb_records, user_knb_record

from bd import create_user, get_all_user_ids
from constants import MAINMENU, RATE


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - вся информация о сообщении
    # update.effective_user - все о пользователе
    # update.effective_message - все о сообщении
    # update.effective_chat - все о диалоге
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет, {update.effective_user.full_name}\nВыбери действие:\n/knb - камень, ножницы, бумага\n/bac - быки и коровы\n/xo - крестики нолики\n/rate - покажет ваш рекорды и список рекордсменов",
        disable_notification = True
    )
    # time(20,16, tzinfo=pytz.timezone('Etc/GMT-3')
    #context.user_data['a'] = 30
    #context.job_queue.run_once(remind_to_game, timedelta(seconds=5), chat_id=update.effective_user.id, data={'user_data':context.user_data, 'update':update})
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
        text = 'Ваш рекорд: xo_data'

    elif query.data == "xo_user_data":
        keyboard = [
            [InlineKeyboardButton("Мои рекорды", callback_data="xo_data")],
            [InlineKeyboardButton("Все рекорды", callback_data="records_data")],
        ]
        text = 'Ваш рекорд: xo_user_data'
        
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=markup)
    return RATE

#async def remind_to_game(context: ContextTypes.DEFAULT_TYPE):
#    print(context.job.chat_id)
#    print(context.user_data)

async def reminder_to_play(context: ContextTypes.DEFAULT_TYPE):
    """Рассылает сообщение всем пользователям из базы данных."""
    chat_ids = get_all_user_ids()  # Получаем все chat_id пользователей
    
    for chat_id in chat_ids:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text='Готов к игре? У меня есть для тебя несколько классных игр!',
                disable_notification=True
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {chat_id}: {e}")