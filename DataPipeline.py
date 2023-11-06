from config_loader import load_config
from database_manager import DatabaseManager
from data_extractor import DataExtractor
from data_loader import DataLoader

class DataPipeline:
    def __init__(self, config):
        self.db_manager = DatabaseManager(config['postgresql'], config['snowflake'])
        self.extractor = DataExtractor(self.db_manager)
        self.loader = DataLoader(self.db_manager)

    def run(self, query, table_name):
        cursor = self.extractor.fetch_data(query)
        self.loader.load_to_snowflake(cursor, table_name)

if __name__ == "__main__":
    config = load_config()
    pipeline = DataPipeline(config)
    pipeline.run(config['query'], config['table_name'])
