from typing import Optional

from fastapi import APIRouter, HTTPException
from spectate_rest_app.database import get_db_connection
from spectate_rest_app.schemas import Sport
import sqlite3
from spectate_rest_app.services import get_slug, sport_is_active

router = APIRouter()


@router.post("/sport", status_code=201)
async def create_sport(sport: Sport):
    """Create a new sport"""
    if not sport.name:
        raise HTTPException(status_code=400, detail="Name is required")
    slug = get_slug(sport.name)
    active = sport_is_active(sport.name)

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
    """Update a sport"""
    query = """
            UPDATE sport
            SET name = ?, slug = ?, active = ?
            WHERE id = ?
    """
    slug = get_slug(sport.name)
    active = False
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (sport.name, slug, active, sport_id))
        conn.commit()
        conn.close()
        return {"id": sport_id}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/search_sports")
async def search_sports(
    name: Optional[str] = None,
    slug: Optional[str] = None,
    active: Optional[bool] = None,
):
    query = "SELECT * FROM sport WHERE 1=1"
    params = []
    if name:
        query += " AND name LIKE ?"
        params.append(name)
    if slug:
        query += " AND slug = ?"
        params.append(slug)
    if active is not None:
        query += " AND active = ?"
        params.append(1 if active else 0)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"sports": [dict(row) for row in rows]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
