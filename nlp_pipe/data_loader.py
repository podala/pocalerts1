import pandas as pd
import logging

def read_notes_from_csv(file_path, chunk_size=1000):
    try:
        chunks = pd.read_csv(file_path, chunksize=chunk_size)
        for chunk in chunks:
            yield chunk['notes'].tolist()
    except FileNotFoundError:
        logging.error(f"CSV file not found at path: {file_path}")
        raise
    except pd.errors.EmptyDataError:
        logging.error(f"CSV file at path {file_path} is empty.")
        raise
    except pd.errors.ParserError:
        logging.error(f"Error parsing CSV file at path: {file_path}")
        raise
