import sqlite3
import os


class SQLiteClient:
    def __init__(self, db_name):
        if os.getenv('TESTING') == 'true':
            db_path = ':memory:'
        else:
            db_path = os.path.join('/data', db_name)
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()

    def get_client(self):
        return self.cursor


class NoteDB:
    def __init__(self, db_name):
        self.client = SQLiteClient(db_name)
        # self.client.execute_query('DROP TABLE IF EXISTS notes')
        self.client.execute_query('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, email TEXT, data TEXT)')

    def insert(self, email, data):
        self.client.execute_query('INSERT INTO notes (email, data) VALUES (?, ?)', (email, data))

    def fetch_all(self):
        return self.client.fetch_all('SELECT * FROM notes')

    def delete_all(self):
        self.client.execute_query('DELETE FROM notes')

    def delete_single(self, id):
        self.client.execute_query('DELETE FROM notes WHERE id = ?', (id))

    def close(self):
        self.client.close()
