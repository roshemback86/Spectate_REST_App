from fastapi import APIRouter, HTTPException
from spectate_rest_app.database import get_db_connection
from spectate_rest_app.schemas import Sport
import sqlite3
from spectate_rest_app.services import get_slug
router = APIRouter()


@router.post("/sport", status_code=201)
async def create_sport(sport: Sport):
    '''Create a new sport'''
    if not sport.name:
        raise HTTPException(status_code=400, detail="Name is required")
    slug = get_slug(sport.name)
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

@router.put("/sport/{sport_id}")
async def update_sport(sport_id: int, sport: Sport):
    '''Update a sport'''
    query = """
            UPDATE sport
            SET name = ?, slug = ?, active = ?
            WHERE id = ?
    """
    slug = get_slug(sport.name)
    active = sport.active if sport.active is not None else True
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (sport.name, slug, active, sport_id))
        conn.commit()
        sport_id = cursor.lastrowid
        conn.close()
        return {"id": sport_id}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")