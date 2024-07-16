from fastapi import APIRouter, HTTPException
from spectate_rest_app.database import get_db_connection
from spectate_rest_app.schemas import Event
import httpx
from typing import List

router = APIRouter()


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

@router.post("/event", status_code=201)
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