from fastapi import FastAPI, HTTPException
import uvicorn
import sqlite3
import httpx
from typing import List, Optional
import requests
from decimal import Decimal
# from spectate_rest_app.services import get_logos
from .schemas import Sport, Event, Selection
# TODO: разобраться с логированием ошибок, в т.ч. по созданию записей в таблах

app = FastAPI()

DATABASE_URL = "app.db"

async def fetch_logos(teams: List[str]) -> str:
    logos = []
    async with httpx.AsyncClient() as client:
        for team in teams:
            try:
                response = await client.get(f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team}")
                response.raise_for_status()
                data = response.json()
                logo = data['teams'][0]['strBadge'] if data['teams'] else ""
                logos.append(logo)
            except Exception as e:
                logos.append("")
                print(f"Error fetching logo for team {team}: {e}")
    return "|".join(logos) if any(logos) else None


def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/sport", status_code=201)
async def create_sport(sport: Sport):
    '''Create a new sport'''
    if not sport.name:
        raise HTTPException(status_code=400, detail="Name is required")
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


@app.post("/event", status_code=201)
async def create_event(event: Event):
    '''Create a new event'''
    if not event.name or not event.type or not event.sport or not event.status or not event.scheduled_start:
        raise HTTPException(status_code=400, detail="Required fields: name, type, sport, status, scheduled_start")

    slug = event.slug if event.slug is not None else event.name.lower().replace(" ", "-")
    active = event.active if event.active is not None else True
    teams = [team.strip() for team in event.name.split("vs")]
    logos = await fetch_logos(teams)

    query = """
        INSERT INTO event (name, slug, active, type, sport, status, scheduled_start, actual_start, logos) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (
            event.name, slug, active, event.type, event.sport, event.status,
            event.scheduled_start.isoformat(),
            event.actual_start.isoformat() if event.actual_start else None,
            logos
        ))
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"id": event_id}


@app.post("/create_selection")
async def create_selection(selection: Selection):
    '''Create a new selection'''
    if not selection.name or not selection.event or not selection.price or not selection.outcome:
        raise HTTPException(status_code=400, detail="Required fields: name, event, price, outcome")

    active = True if selection.active else False
    selection.price = Decimal(selection.price)
    query = """
        INSERT INTO selection (name, event, active, price, outcome) 
        VALUES (?, ?, ?, ?, ?)
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (
            selection.name, selection.event, active, float(selection.price), selection.outcome
        ))
        conn.commit()
        selection_id = cursor.lastrowid
        conn.close()
        return {"id": selection_id}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
