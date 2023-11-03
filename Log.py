# Add the import at the beginning of the file
from logger import Logger

class DataPipeline:
    def __init__(self, config_path):
        self.config_handler = ConfigHandler(config_path)
        self.logger = Logger.setup_logging('logs/data_pipeline.log')
        self.logger.info("DataPipeline initialized with configuration.")

    def run(self):
        # ... rest of the run method

        for table_name in tables:
            # ... before query execution
            self.logger.info(f"Fetching data for table: {table_name}")
            # ... after successful data fetching
            self.logger.info(f"Data fetched for table: {table_name}, records: {len(data)}")

            # ... before and after writing JSON file
            self.logger.info(f"Writing data to JSON file: {filename}")
            # ... after successful file staging
            self.logger.info(f"File staged successfully: {filename}")

        # ... rest of the method
