import sqlite3

def init_db():
    conn = sqlite3.connect('SqlliteDB/takeaway.db')  
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS spendings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            location TEXT,
            cost REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database and table created (if not already exists)")

if __name__ == "__main__":
    init_db()