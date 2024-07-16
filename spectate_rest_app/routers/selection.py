from fastapi import APIRouter, HTTPException
from spectate_rest_app.database import get_db_connection
from spectate_rest_app.schemas import Selection
import sqlite3

from decimal import Decimal

router = APIRouter()

@router.post("/create_selection")
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