import sqlite3

def create_table():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        address TEXT,
        email TEXT UNIQUE,
        phone TEXT UNIQUE,
        category TEXT DEFAULT 'General',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_interaction DATE
    )''')
    conn.commit()
    conn.close()
