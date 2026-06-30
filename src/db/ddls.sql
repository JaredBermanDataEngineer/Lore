CREATE TABLE IF NOT EXISTS bronze_messages(
    chat_id TEXT,
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
    chat_id TEXT,
    session_id TEXT,
    message_id TEXT,
    customer_id TEXT,
    ps_message_id TEXT,
    model_id TEXT,
    timestamp TIMESTAMP,
    sent_by TEXT,
    message_sentiment TEXT,
    session_sentiment TEXT,
    chat_sentiment TEXT,
    message_topic TEXT
);
