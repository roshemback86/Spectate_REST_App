from fastapi import APIRouter, HTTPException
from spectate_rest_app.database import get_db_connection
from spectate_rest_app.schemas import Event
from spectate_rest_app.services import get_slug, fetch_logos
import sqlite3
router = APIRouter()


@router.post("/event", status_code=201)
async def create_event(event: Event):
    '''Create a new event'''
    if not event.name or not event.type or not event.sport or not event.status or not event.scheduled_start:
        raise HTTPException(status_code=400, detail="Required fields: name, type, sport, status, scheduled_start")

    slug = get_slug(event.name)
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


@router.put("/event/{event_id}")
async def update_event(event_id: int, event: Event):
    '''Update an event'''

    query = """
        UPDATE event
        SET name = ?, slug = ?, active = ?, type = ?, sport = ?, status = ?, scheduled_start = ?, actual_start = ?, logos = ?
        WHERE id = ?
    """
    if not event.name or not event.type or not event.sport or not event.status or not event.scheduled_start:
        raise HTTPException(status_code=400, detail="Required fields: name, type, sport, status, scheduled_start")

    slug = get_slug(event.name)
    active = event.active if event.active is not None else True
    teams = [team.strip() for team in event.name.split("vs")]
    logos = await fetch_logos(teams)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (event.name, slug, active, event.type, event.sport, event.status, event.scheduled_start.isoformat(),
              event.actual_start.isoformat() if event.actual_start else None, logos, event_id))
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()
        return {"id": event_id}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")