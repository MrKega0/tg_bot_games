# Создать подключение к бд
import sqlite3
from operator import itemgetter

from telegram import Update


def create_db():
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        wins INTEGER,
                        all_games INTEGER,
                        bac_record INTEGER
                    )
    """)
    conn.commit()
    conn.close()


def create_user(update: Update):
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(f"SELECT id, name FROM users WHERE id = {update.effective_user.id}")
    user = cur.fetchone()  # (24123421,'vova') | None
    if not user:
        cur.execute(
            f'INSERT INTO users VALUES({update.effective_user.id}, "{update.effective_user.first_name}", 0, 0, 1000)'
        )
        conn.commit()
    conn.close()


def update_bac_record(update: Update, new_record):
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(f"SELECT bac_record FROM users WHERE id = {update.effective_user.id}")
    record = cur.fetchone()[0]
    print(record)
    if new_record < record:
        cur.execute(f"UPDATE users SET bac_record={new_record}")
    conn.commit()
    conn.close()


def user_bac_record(update: Update):
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(f"SELECT bac_record FROM users WHERE id = {update.effective_user.id}")
    record = cur.fetchone()[0]
    return record


def print_bac_records() -> str:
    '''
    Возвращает строку с 10ю рекордсменами в Быки и коровы
    '''
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute("SELECT bac_record, name FROM users")
    output_text = ""
    users = cur.fetchall()
    sorted_users = sorted(users, key=itemgetter(0), reverse=True)
    for i in range(len(sorted_users)):
        output_text += f"{sorted_users[i][1]}: {sorted_users[i][0]}\n"
        if i >= 10:
            break
    return output_text


def update_knb_win(update: Update, is_win):
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(
        f"SELECT wins, all_games FROM users WHERE id = {update.effective_user.id}"
    )
    user = cur.fetchone()
    if is_win:
        cur.execute(
            f"UPDATE users SET wins={user[0]+1}, all_games={user[1]+1} WHERE id = {update.effective_user.id}"
        )
    else:
        cur.execute(
            f"UPDATE users SET wins={user[0]}, all_games={user[1]+1} WHERE id = {update.effective_user.id}"
        )
    conn.commit()
    conn.close()

def print_knb_records() -> str:
    '''
    Возвращает строку с 10ю рекордсменами в Камень ножницы бумага
    '''
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute("SELECT wins, name FROM users")
    output_text = ""
    users = cur.fetchall()
    sorted_users = sorted(users, key=itemgetter(0), reverse=False)
    for i in range(len(sorted_users)):
        output_text += f"{sorted_users[i][1]}: {sorted_users[i][0]}\n"
        if i >= 10:
            break
    return output_text

def user_knb_record(update: Update):
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(f"SELECT wins FROM users WHERE id = {update.effective_user.id}")
    record = cur.fetchone()[0]
    return record
