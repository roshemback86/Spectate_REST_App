from fastapi import FastAPI, HTTPException
import uvicorn
import sqlite3
import httpx
from .schemas import Sport, Event, Selection
# TODO: разобраться с логированием ошибок, в т.ч. по созданию записей в таблах
app = FastAPI()

DATABASE_URL = "app.db"


def get_db_connection():
    conn = sqlite3.connect('app.db')  # Replace with your database file or connection string
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/sport", status_code=201)
async def create_sport(sport: Sport):
    '''Create a new sport'''
    slug = sport.slug if sport.slug is not None else sport.name.lower().replace(" ", "-")
    active = sport.active if sport.active is not None else True

    query = """
        INSERT INTO sport (name, slug, active) 
        VALUES (?, ?, ?)
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (sport.name, slug, active))
        conn.commit()
        sport_id = cursor.lastrowid
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": sport_id}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
