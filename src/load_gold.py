import sqlite3

from transformers import pipeline

# Load the classification pipeline with the specified model
# pipe = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")


def load_gold(conn):
    conn.row_factory = sqlite3.Row 
    cur = conn.cursor()

    cur.execute("""
        SELECT
            *
        FROM bronze_messages bm
        WHERE bm.sent_by = 'user'
    """)

    msg_rows = cur.fetchall()

    msgs = [row["content"] for row in msg_rows]
    message_sentiments = pipe(msgs)
    message_sentiments = [sentiment["label"] for sentiment in message_sentiments]

    for message_sentiment, row in zip(message_sentiments, msg_rows):

        cur.execute("""
            INSERT INTO gold_messages (
                session_id,
                message_id,
                user_id,
                ps_message_id,
                model_id,
                timestamp,
                sent_by,
                content,
                ingested_at,
                message_sentiment
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["session_id"],
            row["message_id"],
            row["user_id"],
            row["ps_message_id"],
            row["model_id"],
            row["timestamp"],
            row["sent_by"],
            row["content"],
            row["ingested_at"],
            message_sentiment
        ))

    cur.execute("""
        SELECT
            session_id,
            GROUP_CONCAT(content, ' ') AS chat
        FROM (
            SELECT
                session_id,
                content
            FROM bronze_messages
            ORDER BY session_id, timestamp 
        )
        GROUP BY session_id;
    """)

    sess_rows = cur.fetchall()

    msgs = [row["chat"] for row in sess_rows]
    sess_sentiments = pipe(msgs)
    sess_sentiments = [sentiment["label"] for sentiment in sess_sentiments]

    updates = [
    (sess_sentiment, sess_row["session_id"]) for sess_sentiment, sess_row in zip(sess_sentiments, sess_rows)
    ]

    cur.executemany("""
        UPDATE gold_messages
        SET session_sentiment = ?
        WHERE session_id = ?
    """, updates
    )

    conn.commit()