import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "extracted_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            doc_type TEXT,
            fields_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_to_db(filename: str, doc_type: str, fields: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO documents (filename, doc_type, fields_json)
        VALUES (?, ?, ?)
    """, (filename, doc_type, json.dumps(fields)))

    conn.commit()
    conn.close()
