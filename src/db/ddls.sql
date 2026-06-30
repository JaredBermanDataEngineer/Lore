CREATE TABLE IF NOT EXISTS bronze_messages(
    session_id TEXT,
    message_id TEXT,
    user_id TEXT,
    ps_message_id TEXT,
    model_id TEXT,
    timestamp TIMESTAMP,
    sent_by TEXT,
    content TEXT,
    ingested_at DATETIME
);


CREATE TABLE IF NOT EXISTS gold_messages(
    session_id TEXT,
    message_id TEXT,
    user_id TEXT,
    ps_message_id TEXT,
    model_id TEXT,
    timestamp TIMESTAMP,
    sent_by TEXT,
    content TEXT,
    ingested_at DATETIME,
    message_sentiment TEXT,
    session_sentiment TEXT,

    PRIMARY KEY (session_id, message_id)
);
