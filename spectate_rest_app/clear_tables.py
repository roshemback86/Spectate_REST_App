import sqlite3

DATABASE_URL = "app.db"

def clear_tables():

    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS sport")
    cursor.execute("DROP TABLE IF EXISTS event")
    cursor.execute("DROP TABLE IF EXISTS selection")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    clear_tables()