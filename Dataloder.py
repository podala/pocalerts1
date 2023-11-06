import json
import os
from tempfile import NamedTemporaryFile

class DataLoader:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def row_to_json(self, row, cursor):
        # Convert a database row to a JSON object
        data = {desc[0]: value for desc, value in zip(cursor.description, row)}
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.replace('"', '\\"')  # Escape double-quotes in strings
        return json.dumps(data)

    def stage_file_for_snowflake(self, sf_cursor, file_path, stage_name):
        # Stage the file to Snowflake
        put_command = f"PUT 'file://{file_path}' @{stage_name}"
        sf_cursor.execute(put_command)

    def copy_into_snowflake(self, sf_cursor, stage_name, table_name):
        # Copy the data from the staged file into the Snowflake table
        copy_command = f"COPY INTO {table_name} FROM @{stage_name} FILE_FORMAT = (TYPE = 'JSON')"
        sf_cursor.execute(copy_command)

    def load_to_snowflake(self, cursor, table_name, stage_name, batch_size=5000):
        sf_cursor = self.db_manager.get_sf_cursor()
        rows = cursor.fetchmany(batch_size)
        while rows:
            with NamedTemporaryFile(delete=False, mode='w') as temp_file:
                # Write each row to the temporary file as a JSON object
                for row in rows:
                    temp_file.write(self.row_to_json(row, cursor) + '\n')
                temp_file_path = temp_file.name

            try:
                # Stage the temporary file to Snowflake
                self.stage_file_for_snowflake(sf_cursor, temp_file_path, stage_name)
                # Load the staged data into the Snowflake table
                self.copy_into_snowflake(sf_cursor, stage_name, table_name)
            finally:
                # Remove the temporary file
                os.remove(temp_file_path)

            # Fetch the next batch
            rows = cursor.fetchmany(batch_size)

        sf_cursor.close()
