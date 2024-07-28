
import sqlite3

DATABASE_URL = "app.db"
def create_tables():

    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE Sport (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT NOT NULL,
        active BOOLEAN NOT NULL
    )
    ''')
    conn.commit()
    cursor.execute('''
    CREATE TABLE Event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT NOT NULL,
        active BOOLEAN NOT NULL,
        type TEXT NOT NULL,
        sport TEXT NOT NULL,
        status TEXT CHECK( status IN ('PENDING', 'STARTED', 'ENDED', 'CANCELLED') ) NOT NULL,
        scheduled_start DATETIME,
        actual_start DATETIME,
        logos TEXT,
        FOREIGN KEY (sport) REFERENCES Sport(name)
    )
    ''')
    conn.commit()
    cursor.execute('''
    CREATE TABLE Selection (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        event TEXT NOT NULL,
        active BOOLEAN NOT NULL,
        price REAL NOT NULL,
        outcome TEXT CHECK( outcome IN ('UNSETTLED', 'VOID', 'LOSE', 'WIN') ) NOT NULL,
        FOREIGN KEY (event) REFERENCES Event(name)
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()