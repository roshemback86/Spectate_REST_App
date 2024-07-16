from fastapi import APIRouter, HTTPException
from spectate_rest_app.database import get_db_connection
from spectate_rest_app.schemas import Sport

router = APIRouter()

@router.post("/sport", status_code=201)
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