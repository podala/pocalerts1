from config_handler import ConfigHandler
from database_connector import PostgresConnector, SnowflakeConnector
import json
import os

class DataTransformer:
    @staticmethod
    def write_json(data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)

class DataPipeline:
    def __init__(self, config_path):
        self.config_handler = ConfigHandler(config_path)

    def run(self):
        pg_config = self.config_handler.get_postgresql_config()
        sf_config = self.config_handler.get_snowflake_config()
        tables = self.config_handler.get_tables_list()

        pg_conn = PostgresConnector(pg_config)
        sf_conn = SnowflakeConnector(sf_config)

        for table_name in tables:
            query_file_path = self.config_handler.get_query_file_path('fetch_table_data')
            with open(query_file_path, 'r') as query_file:
                query = query_file.read().format(table_name)
            
            data = pg_conn.query_data(query)
            filename = f"{table_name}.json"
            DataTransformer.write_json(data, filename)
            sf_conn.stage_file(filename, sf_config['stage'])

        pg_conn.close()
        sf_conn.close()

if __name__ == "__main__":
    pipeline = DataPipeline('config.yaml')
    pipeline.run()
