import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('group_bot.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS warnings 
             (user_id INTEGER, chat_id INTEGER, count INTEGER DEFAULT 0, PRIMARY KEY(user_id, chat_id))''')

c.execute('''CREATE TABLE IF NOT EXISTS rules 
             (chat_id INTEGER PRIMARY KEY, rules_text TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS flood 
             (user_id INTEGER, chat_id INTEGER, last_message REAL, count INTEGER)''')

conn.commit()

def add_warning(user_id: int, chat_id: int) -> int:
    c.execute("INSERT OR REPLACE INTO warnings VALUES (?, ?, COALESCE((SELECT count FROM warnings WHERE user_id=? AND chat_id=?),0)+1)", 
              (user_id, chat_id, user_id, chat_id))
    conn.commit()
    return get_warnings(user_id, chat_id)

def get_warnings(user_id: int, chat_id: int) -> int:
    c.execute("SELECT count FROM warnings WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    result = c.fetchone()
    return result[0] if result else 0

def reset_warnings(user_id: int, chat_id: int):
    c.execute("DELETE FROM warnings WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    conn.commit()

def set_rules(chat_id: int, rules: str):
    c.execute("INSERT OR REPLACE INTO rules VALUES (?, ?)", (chat_id, rules))
    conn.commit()

def get_rules(chat_id: int):
    c.execute("SELECT rules_text FROM rules WHERE chat_id=?", (chat_id,))
    result = c.fetchone()
    return result[0] if result else "Grup kuralları tanımlanmamış."
