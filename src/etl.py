import sqlite3
import json
import uuid
from datetime import datetime, timezone
from .db.init_db import init_db

def etl():
    ############ INIT DB ###############################
    # For POC purposes only. In production never couple DDLs with ETLs. Use a proper migration system.

    conn = sqlite3.connect("output/warehouse.db")
    init_db(conn)

    ############ LOAD RAW DATA INTO BRONZE LAYER DB ####

    with open("data/chats.json", "r", encoding="utf-8") as f:
        chats = json.load(f)

    rows = []
    now = datetime.now(timezone.utc)
    for session in chats:
        customer_id = session["customer_id"]
        for msg in session["messages"]:
            rows.append((
                str(uuid.uuid4()),
                str(uuid.uuid4()),
                str(uuid.uuid4()),
                customer_id,
                str(uuid.uuid4()),
                str(uuid.uuid4()),
                msg["timestamp"],
                msg["role"],
                msg["content"],
                now
            ))

    cur = conn.cursor()

    cur.executemany("""
        INSERT INTO bronze_messages (
            chat_id,
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()

    ############ LOAD GOLD TABLES ######################
    #clean_gold(conn)
    
    ############ ANALYTICS #############################
    #refresh_views(conn)

    conn.close()
