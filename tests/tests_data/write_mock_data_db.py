# write_mock_data_db.py
import random
from uuid import uuid4
from datetime import datetime, timedelta
from pathlib import Path
from data.db.main_db import write_entry_to_db
from models.entry_models import EntryRepo

DB_PATH = Path(__file__).parent.parent.parent / "data/db/crowdlens.db"

GROUPS = [
    {
        "topic": "Heavy rain damage",
        "keywords": ["heavy rain", "flooded streets", "property damage", "collapsed wall"]
    },
    {
        "topic": "Fire on 22nd Street",
        "keywords": ["building on fire", "firefighters", "22nd street", "evacuation"]
    },
    {
        "topic": "Power outage in downtown",
        "keywords": ["power outage", "blackout", "downtown", "electric company"]
    },
    {
        "topic": "Road accident near Central Park",
        "keywords": ["car crash", "central park", "ambulance", "traffic jam"]
    },
    {
        "topic": "Protest in City Hall",
        "keywords": ["protest", "city hall", "demonstration", "police presence"]
    }
]


def generate_text(group_keywords: list[str], index: int) -> str:
    base = group_keywords[index % len(group_keywords)]
    return f"{base} observed by residents."


def pick_number(pf_number: int) -> int:
    return random.choice([pf_number, random.randint(0, 4)])


def generate_mock_entry(index: int, pf_number: int) -> EntryRepo:
    group_id = pick_number(pf_number)
    group = GROUPS[group_id]
    text = generate_text(group["keywords"], index)
    return EntryRepo(
        entry_id=str(uuid4()),
        message_id=1000 + index + (group_id * 10),
        user_id=99999,
        username="mock_user_script_50_entries",
        timestamp=datetime.now() - timedelta(minutes=(index + group_id * 10)),
        text=text,
        media_type='text',
        save_flag=False
    )


if __name__ == "__main__":
    preferred_number = random.randint(0, 4)
    for i in range(250):
        mock_entry = generate_mock_entry(i, preferred_number)
        write_entry_to_db(mock_entry)
    print("✅ 50 mock entries inserted (5 groups × 10 entries).")
