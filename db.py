import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                      (id INTEGER PRIMARY KEY, type TEXT, amount REAL, date TEXT, category TEXT, description TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories
                      (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
    cursor.executescript("""
        INSERT OR IGNORE INTO categories (name) VALUES ('Продукты');
        INSERT OR IGNORE INTO categories (name) VALUES ('Зарплата');
        INSERT OR IGNORE INTO categories (name) VALUES ('Транспорт');
    """)
    conn.commit()
    conn.close()

def add_transaction(type, amount, date, category, description):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (type, amount, date, category, description) VALUES (?, ?, ?, ?, ?)",
                   (type, amount, date, category, description))
    conn.commit()
    conn.close()

def get_balance():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Доход'")
    income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Расход'")
    expenses = cursor.fetchone()[0] or 0
    conn.close()
    return income - expenses

def get_categories():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM categories")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def get_expense_data():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Расход' GROUP BY category")
    data = cursor.fetchall()
    conn.close()
    return data

def get_history():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, type, category, amount, description FROM transactions")
    history = cursor.fetchall()
    conn.close()
    return history