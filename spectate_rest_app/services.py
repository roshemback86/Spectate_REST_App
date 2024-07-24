import httpx
from typing import List
from spectate_rest_app.database import get_db_connection
import sqlite3
from fastapi import HTTPException

async def fetch_logos(teams: List[str]) -> str:
    logos = []
    async with httpx.AsyncClient() as client:
        for team in teams:
            try:
                response = await client.get(
                    f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team}"
                )
                response.raise_for_status()
                data = response.json()
                logo = data["teams"][0]["strBadge"] if data["teams"] else ""
                logos.append(logo)
            except Exception as e:
                logos.append("")
                print(f"Error fetching logo for team {team}: {e}")
    return "|".join(logos) if any(logos) else None


def get_slug(slug: str) -> str:
    return slug.lower().replace(" ", "-")


def sport_is_active(sport_name: str) -> bool:
    """
    Check if any event of this sport is active
    """
    query = "SELECT * FROM event WHERE sport = ? AND active = ?"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (sport_name, True))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return True if rows else False
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def update_sport_is_active(sport_name: str):
    """
    Update the active status of sport if any event is active.
    """
    active = sport_is_active(sport_name)
    query = "UPDATE sport SET active = ? WHERE name = ?"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (active, sport_name))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


def event_is_active(event_name: str) -> bool:
    """
    Check if any selection of this event is active
    """
    query = "SELECT * FROM selection WHERE event = ? AND active = ?"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (event_name, True))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return True if rows else False
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def update_event_is_active(event_name: str):
    """
    Update the active status of event if any selection is active.
    """
    active = event_is_active(event_name)
    query = "UPDATE event SET active = ? WHERE name = ?"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (active, event_name))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")