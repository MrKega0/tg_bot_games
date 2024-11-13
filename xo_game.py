from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
)

from constants import XO_GAME


async def xo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Классические крестики - нолики, введи цифру куда хочешь поставить крестик или нолик",
    )

    context.user_data["xo_saved_data"] = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=render_xo(context.user_data["xo_saved_data"]),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    return XO_GAME


def render_xo(data: list):
    text = ""

    for i in data:
        text += "----------\n"
        text += " | ".join(i)
        text += "\n"

    print(text)
    return f"`{text}`"


def take_input_xo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data["xo_saved_data"]
    num = update.message.text
    if num == "X" or num == "O":
        return None
    for i in user_data:
        for j in i:
            if num == j:
                return j
    return None


def change_xo_data(num, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data["xo_saved_data"]
    x = 0
    o = 0
    for i in data:
        x += i.count("X")
        o += i.count("O")
    print(x, o)
    if x > o:
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == num:
                    data[i][j] = "O"
    else:
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == num:
                    data[i][j] = "X"
    context.user_data["xo_saved_data"] = data


def check_xo_win(data: set):
    draw = True
    if data[0][0] == data[1][1] and data[0][0] == data[2][2]:
        return data[0][0]
    elif data[0][2] == data[1][1] and data[0][2] == data[2][0]:
        return data[0][2]
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                draw = False
            if data[i].count(data[i][j]) == 3:
                return data[i][j]
            if data[i][j] == data[i - 1][j] and data[i][j] == data[i - 2][j]:
                return data[i][j]
    if draw:
        return "draw"
    else:
        return None


async def x_o_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    changed_num = take_input_xo(update, context)
    if not changed_num:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Введите число"
        )
        return XO_GAME
    change_xo_data(changed_num, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=render_xo(context.user_data["xo_saved_data"]),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    continuation = check_xo_win(context.user_data["xo_saved_data"])
    if continuation == "draw":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Ничья")
        del context.user_data["xo_saved_data"]
        return await xo(update, context)
    elif continuation == "X" or continuation == "O":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Победили {continuation}"
        )
        return await xo(update, context)
