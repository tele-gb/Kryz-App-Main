import sqlite3

#-- ISO-8601 format (recommended) for dates - they are stored as text
def init_db():
    conn = sqlite3.connect('SqlliteDB/strava.db')  
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            Runid INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            date TEXT,
            distance INTEGER,
            seconds INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    print("Database and table created (if not already exists)")

if __name__ == "__main__":
    init_db()