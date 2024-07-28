from typing import Optional

from fastapi import APIRouter, HTTPException
from spectate_rest_app.database import get_db_connection
from spectate_rest_app.schemas import Selection
from spectate_rest_app.consts import OutcomeEnum
import sqlite3

from decimal import Decimal

from spectate_rest_app.services import update_event_is_active

router = APIRouter()


@router.post("/selection", status_code=201)
async def create_selection(selection: Selection):
    """Create a new selection"""
    if (
        not selection.name
        or not selection.event
        or not selection.price
        or not selection.outcome
    ):
        raise HTTPException(
            status_code=400, detail="Required fields: name, event, price, outcome"
        )
    active = True if selection.active else False
    selection.price = Decimal(selection.price)
    query = """
        INSERT INTO selection (name, event, active, price, outcome) 
        VALUES (?, ?, ?, ?, ?)
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            query,
            (
                selection.name,
                selection.event,
                active,
                float(selection.price),
                selection.outcome,
            ),
        )
        conn.commit()
        selection_id = cursor.lastrowid
        conn.close()
        update_event_is_active(selection.event)
        return {"id": selection_id}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.put("/selection/{selection_id}")
async def update_selection(selection_id: int, selection: Selection):
    if (
        not selection.name
        or not selection.event
        or not selection.price
        or not selection.outcome
    ):
        raise HTTPException(
            status_code=400, detail="Required fields: name, event, price, outcome"
        )
    query = """
        UPDATE selection 
        SET name = ?, event = ?, active = ?, price = ?, outcome = ?
        WHERE id = ?
    """

    selection.price = Decimal(selection.price)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            query,
            (
                selection.name,
                selection.event,
                selection.active,
                str(selection.price),
                selection.outcome,
                selection_id,
            ),
        )
        conn.commit()
        conn.close()
        update_event_is_active(selection.event)
        return {"id": selection_id}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/search_selections")
async def search_selections(
    name: Optional[str] = None,
    event: Optional[str] = None,
    active: Optional[bool] = None,
    outcome: Optional[OutcomeEnum] = None,
):
    query = "SELECT * FROM selection WHERE 1=1"
    params = []
    if name:
        query += " AND name LIKE ?"
        params.append(name)
    if event:
        query += " AND event LIKE ?"
        params.append(event)
    if active is not None:
        query += " AND active = ?"
        params.append(1 if active else 0)
    if outcome:
        query += " AND outcome = ?"
        params.append(outcome.value)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"selections": [dict(row) for row in rows]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
