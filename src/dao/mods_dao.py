import psycopg2

from ..utils.dao import db_instance

class ModsDAO():
    def __init__(self):
        self.conn = db_instance.get_connection()
        self.cursor = self.conn.cursor()

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            db_instance.release_connection(self.conn)