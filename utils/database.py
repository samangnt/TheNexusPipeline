import sqlite3

def init_database() -> None:
    conn = sqlite3.connect("nexus_pipeline.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            path TEXT UNIQUE,
            status TEXT,
            tags TEXT,
            critique TEXT,
            discovered_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def is_already_processed(path: str) -> bool:
    conn = sqlite3.connect("nexus_pipeline.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM assets WHERE path = ?", (path,))
    result = cursor.fetchone()
    
    conn.close()
    return result is not None

def save_asset(asset) -> None:
    conn = sqlite3.connect("nexus_pipeline.db")
    cursor = conn.cursor()
    
    data = asset.to_dict()
    cursor.execute("""
        INSERT OR REPLACE INTO assets 
        (name, path, status, tags, critique, discovered_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data['name'], data['path'], data['status'], 
          data['tags'], data['critique'], data['discovered_at']))
    
    conn.commit()
    conn.close()