import os
from dotenv import load_dotenv

import psycopg2

load_dotenv()

class DAO():
    def __init__(self):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn = 1,
                maxconn = 10,
                host = os.getenv('DATABASE_HOST'),
                database = os.getenv('DATABASE_DB'),
                user = os.getenv('DATABASE_USER'),
                password = os.getenv('DATABASE_PASSWORD')
            )
            self.connection_pool.autocommit = True
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.connection_pool = None

    def get_connection(self):
        if self.connection_pool:
            return self.connection_pool.getconn()
        else:
            raise ConnectionError("No available database connection.")

    def release_connection(self, conn):
        if self.connection_pool:
            self.connection_pool.putconn(conn)

    def close_all_connections(self):
        if self.connection_pool:
            self.connection_pool.closeall()

# Create a singleton instance of Database for use in other modules
db_instance = DAO()