import psycopg2
from snowflake.connector import connect

class DatabaseManager:
    def __init__(self, pg_config, sf_config):
        self.pg_config = pg_config
        self.sf_config = sf_config

    def get_pg_cursor(self):
        conn = psycopg2.connect(**self.pg_config)
        return conn.cursor()

    def get_sf_cursor(self):
        conn = connect(**self.sf_config)
        return conn.cursor()
