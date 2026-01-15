import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "proposals.db"

def save_memory(client, text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS memory (client TEXT, data TEXT)"
    )
    c.execute(
        "INSERT INTO memory VALUES (?, ?)",
        (client, text)
    )
    conn.commit()
    conn.close()

def load_memory(client):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS memory (client TEXT, data TEXT)"
    )
    c.execute(
        "SELECT data FROM memory WHERE client=?",
        (client,)
    )
    rows = c.fetchall()
    conn.close()
    return rows
