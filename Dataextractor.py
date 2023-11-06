class DataExtractor:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def fetch_data(self, query):
        cursor = self.db_manager.get_pg_cursor()
        cursor.execute(query)
        return cursor
