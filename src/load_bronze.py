import json
import uuid
from datetime import datetime, timezone


def load_bronze(conn):
    with open("data/chats.json", "r", encoding="utf-8") as f:
        chats = json.load(f)

    rows = []
    now = datetime.now(timezone.utc)
    model_id = str(uuid.uuid4())
    for session in chats:
        customer_id = session["customer_id"]
        session_id = str(uuid.uuid4())
        for msg in session["messages"]:
            rows.append((
                session_id,
                str(uuid.uuid4()),
                customer_id,
                str(uuid.uuid4()),
                model_id,
                msg["timestamp"],
                msg["role"],
                msg["content"],
                now
            ))

    cur = conn.cursor()

    cur.executemany("""
        INSERT INTO bronze_messages (
            session_id,
            message_id,
            user_id,
            ps_message_id,
            model_id,
            timestamp,
            sent_by,
            content,
            ingested_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()