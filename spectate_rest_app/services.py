
import httpx
from typing import List

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


def get_slug(slug: str) -> str:
    return slug if slug is not None else slug.lower().replace(" ", "-")