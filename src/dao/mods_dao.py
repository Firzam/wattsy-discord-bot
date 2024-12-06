from utils.postgres_dao import postgres_instance

class ModsDAO():
    def __init__(self):
        self.conn = postgres_instance.get_connection()
        self.cursor = self.conn.cursor()

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            postgres_instance.release_connection(self.conn)