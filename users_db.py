import sqlite3

def create_users_table():
    conn = sqlite3.connect('users_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('users_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password, email)
        VALUES (?, ?, ?)
    ''', (username, password))
    conn.commit()
    conn.close()
  