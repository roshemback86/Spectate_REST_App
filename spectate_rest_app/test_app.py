import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from decimal import Decimal

from spectate_rest_app.database import get_db_connection
from spectate_rest_app.main import app
import sqlite3

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE Sport (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT NOT NULL,
        active BOOLEAN NOT NULL
    )
    ''')
    conn.commit()
    cursor.execute('''
    CREATE TABLE Event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT NOT NULL,
        active BOOLEAN NOT NULL,
        type TEXT NOT NULL,
        sport TEXT NOT NULL,
        status TEXT CHECK( status IN ('PENDING', 'STARTED', 'ENDED', 'CANCELLED') ) NOT NULL,
        scheduled_start DATETIME,
        actual_start DATETIME,
        logos TEXT,
        FOREIGN KEY (sport) REFERENCES Sport(name)
    )
    ''')
    conn.commit()
    cursor.execute('''
    CREATE TABLE Selection (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        event TEXT NOT NULL,
        active BOOLEAN NOT NULL,
        price REAL NOT NULL,
        outcome TEXT CHECK( outcome IN ('UNSETTLED', 'VOID', 'LOSE', 'WIN') ) NOT NULL,
        FOREIGN KEY (event) REFERENCES Event(name)
    )
    ''')
    conn.commit()
    conn.close()


def test_create_sport(setup_database):
    response = client.post("/sport", json={"name": "Basketball"})
    assert response.status_code == 201
    assert response.json() == {"id": 1}

    response = client.post("/sport", json={"name": "Football"})
    assert response.status_code == 201
    assert response.json() == {"id": 2}

    response = client.post("/sport", json={"name": "Poker"})
    assert response.status_code == 201
    assert response.json() == {"id": 3}

    response = client.get("/search_sports?name=Basketball")
    assert response.status_code == 200
    assert len(response.json()["sports"]) == 1
    assert response.json()["sports"][0]["name"] == "Basketball"

# Test updating a sport
def test_update_sport():
    response = client.put("/sport/1", json={"name": "Hockey"})
    assert response.status_code == 200
    assert response.json() == {"id": 1}

    response = client.get("/search_sports?name=Hockey")
    assert response.status_code == 200
    assert len(response.json()["sports"]) == 1
    assert response.json()["sports"][0]["name"] == "Hockey"

def test_search_sports():
    response = client.get("/search_sports?name=F%")
    assert response.status_code == 200
    assert len(response.json()["sports"]) == 1
    assert response.json()["sports"][0]["name"] == "Football"

def test_create_event():
    event_data = {
        "name": "Arsenal vs Aston Villa",
        "type": "preplay",
        "sport": "Football",
        "status": "PENDING",
        "scheduled_start": "2024-09-28T09:54:51.139Z"
    }
    response = client.post("/event", json=event_data)
    assert response.status_code == 201
    assert response.json() == {"id": 1}

    response = client.get("/search_events?name=Arsenal vs Aston Villa")
    assert response.status_code == 200
    assert len(response.json()["events"]) == 1
    assert response.json()["events"][0]["name"] == "Arsenal vs Aston Villa"

    event_data = {
        "name": "Arsenal vs Leeds",
        "type": "preplay",
        "sport": "Football",
        "status": "PENDING",
        "scheduled_start": "2024-10-15T12:11:51.139Z"
    }
    response = client.post("/event", json=event_data)
    assert response.status_code == 201
    assert response.json() == {"id": 2}

    response = client.get("/search_events?name=Arsenal vs Leeds")
    assert response.status_code == 200
    assert len(response.json()["events"]) == 1
    assert response.json()["events"][0]["name"] == "Arsenal vs Leeds"


def test_update_event():
    event_data = {
        "name": "Arsenal vs Swansea City",
        "type": "preplay",
        "sport": "Football",
        "status": "CANCELLED",
        "scheduled_start": "2024-10-15T12:11:51.139Z",
    }
    response = client.put("/event/2", json=event_data)
    assert response.status_code == 200
    assert response.json() == {"id": 2}


def test_search_event():
    response = client.get("/search_events?name=Arsenal%")
    assert response.status_code == 200
    assert len(response.json()["events"]) == 2
    assert response.json()["events"][0]["name"] == "Arsenal vs Aston Villa"
    assert response.json()["events"][1]["name"] == "Arsenal vs Swansea City"

def test_create_selection():
    selection_data = {
        "name": "Arsenal wins",
        "event": "Arsenal vs Aston Villa",
        "price": "200.00",
        "outcome": "WIN"
    }
    response = client.post("/selection", json=selection_data)
    assert response.status_code == 201
    assert response.json() == {"id": 1}

    response = client.get("/search_selections?name=Arsenal wins")
    assert response.status_code == 200
    assert len(response.json()["selections"]) == 1
    assert response.json()["selections"][0]["name"] == "Arsenal wins"

def test_update_selection():
    selection_data = {
        "name": "Arsenal lose",
        "event": "Arsenal vs Aston Villa",
        "price": "150.00",
        "outcome": "LOSE"
    }
    response = client.put("/selection/1", json=selection_data)
    assert response.status_code == 200
    assert response.json() == {"id": 1}



def test_search_selection():

    response = client.get("/search_selections?name=Arsenal lose")
    assert response.status_code == 200
    assert len(response.json()["selections"]) == 1
    assert response.json()["selections"][0]["name"] == "Arsenal lose"


def test_drop_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE sport")
    cursor.execute("DROP TABLE event")
    cursor.execute("DROP TABLE selection")

    conn.commit()
    cursor.close()
    conn.close()
