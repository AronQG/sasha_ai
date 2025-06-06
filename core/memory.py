import sqlite3
import datetime

class Memory:
    def __init__(self, db_path="memory_pro.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT,
                    user TEXT,
                    value TEXT,
                    extra TEXT,
                    timestamp TEXT,
                    media_path TEXT
                )
            ''')

    def log_event(self, event_type, user, value, extra="", media_path=None, timestamp=None):
        if not timestamp:
            timestamp = datetime.datetime.now().isoformat()
        with self.conn:
            self.conn.execute(
                "INSERT INTO events (event_type, user, value, extra, timestamp, media_path) VALUES (?, ?, ?, ?, ?, ?)",
                (event_type, user, value, extra, timestamp, media_path)
            )

    def get_events(self, event_type=None, user=None, start_time=None, end_time=None):
        query = "SELECT * FROM events WHERE 1=1"
        params = []
        if event_type:
            query += " AND event_type=?"
            params.append(event_type)
        if user:
            query += " AND user=?"
            params.append(user)
        if start_time:
            query += " AND timestamp>=?"
            params.append(start_time)
        if end_time:
            query += " AND timestamp<=?"
            params.append(end_time)
        query += " ORDER BY timestamp DESC"
        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()
