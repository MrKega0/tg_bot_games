import random

from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from datetime import timedelta

from bd import update_bac_record
from constants import BAC


def guess_number():
    number = random.randrange(1000, 9999)
    return number


def check_num(num):
    masiv = [str(i) for i in str(num)]
    for i in range(len(masiv)):
        for j in range(len(masiv)):
            if masiv[i] == masiv[j] and i != j:
                return None
    return masiv


def take_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        num = int(update.effective_message.text)
        print(num)
        if num < 1000 or num > 9999:
            return None
        context.user_data["bac_record"] += 1
        return check_num(num)
    except Exception:
        return BAC


def count_bulls_and_cows(g_sp, u_sp):
    bulls = 0
    cows = 0
    for i in range(len(g_sp)):
        print(g_sp, u_sp)
        if g_sp[i] == u_sp[i]:
            bulls += 1
        for j in range(len(u_sp)):
            if g_sp[i] == u_sp[j] and i != j:
                cows += 1
    return bulls, cows


async def bac(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Угадай четырёхзначное число, если цифра есть в числе, то добавляется корова, если номер числа тоже совпадает, то добавляется бык",
    )
    guess_num = check_num(guess_number())
    while guess_num is None:
        guess_num = check_num(guess_number())
        print(guess_num)
    context.user_data["bac_saved_num"] = guess_num
    context.user_data["bac_record"] = 0
    return BAC


async def bulls_and_cows(update: Update, context: ContextTypes.DEFAULT_TYPE):
    guess_num = context.user_data.get("bac_saved_num")

    user_num = take_input(update, context)
    if not user_num:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Число не входит в диапазон от 1000 до 9999\nИли в числе есть повторяющиеся цифры\nВведите число повторно",
        )
        return BAC

    bulls, cows = count_bulls_and_cows(guess_num, user_num)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Быков: {bulls}\nКоров: {cows}"
    )
    if bulls == 4:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Ты Победил!"
        )
        update_bac_record(update, context.user_data['bac_record'])
        del context.user_data['bac_record']
        del context.user_data["bac_saved_num"]

        for i in context.job_queue.jobs():
            if i.job.name == 'bac_remind':
                i.schedule_removal()

        return await bac(update, context)
    else:
        for i in context.job_queue.jobs():
            if i.job.name == 'bac_remind':
                i.schedule_removal()
        context.job_queue.run_once(remind_to_game, timedelta(seconds=10), chat_id=update.effective_user.id, data={'user_data':context.user_data, 'update':update}, name='bac_remind')

async def remind_to_game(context: ContextTypes.DEFAULT_TYPE):
    #print(context.job.chat_id)
    #print(context.job.data)
    #print(context.user_data)
    await context.bot.send_message(chat_id=context.job.chat_id, text='У вас есть незавершённая игра в быках и коровах', disable_notification=True)
