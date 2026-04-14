import sqlite3
from datetime import datetime

DB_PATH = "chat_history.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS history 
                     (user_id TEXT, role TEXT, content TEXT, timestamp TEXT)''')
        conn.commit()

def save_message(user_id, role, content):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO history VALUES (?, ?, ?, ?)", 
                  (user_id, role, content, datetime.now().isoformat()))
        conn.commit()

def get_history(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT role, content FROM history WHERE user_id = ? ORDER BY timestamp ASC", (user_id,))
        return c.fetchall()