import psycopg2
import snowflake.connector

class PostgresConnector:
    def __init__(self, config):
        self.connection = psycopg2.connect(**config)

    def query_data(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def close(self):
        self.connection.close()

class SnowflakeConnector:
    def __init__(self, config):
        self.connection = snowflake.connector.connect(**config)

    def stage_file(self, file_path, stage_name):
        _, filename = os.path.split(file_path)
        with self.connection.cursor() as cursor:
            cursor.execute(f"PUT file://{file_path} @{stage_name} AUTO_COMPRESS=TRUE OVERWRITE=TRUE")
            cursor.execute(f"COPY INTO {filename} FILE_FORMAT = (TYPE = 'JSON')")

    def close(self):
        self.connection.close()
