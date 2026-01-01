import sqlite3

from utils.config import config


class SqliteDAO():
    def __init__(self):
        self.con = sqlite3.connect("wattsy.db")
        
        # Verify if tables are created
        tables = self.con.cursor("SELECT name FROM sqlite_master WHERE type='table'")

        if(tables.fetchone() is None):
            self.con.cursor("CREATE TABLE casino(user_id, credits, join_timestamp, leave_timestamp)")
            print("Casino table created")

    def get_connection(self):
        return self.con

# Create a singleton instance of Database for use in other modules
sqlite_instance = SqliteDAO()