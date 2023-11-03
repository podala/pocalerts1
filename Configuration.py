import yaml

class ConfigHandler:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)

    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def get_postgresql_config(self):
        return self.config['postgresql']

    def get_snowflake_config(self):
        return self.config['snowflake']

    def get_tables_list(self):
        return self.config['tables']

    def get_query_file_path(self, key):
        return self.config['query_files'][key]
