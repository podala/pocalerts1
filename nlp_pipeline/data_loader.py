import pandas as pd

def read_notes_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df['notes'].tolist()
    except Exception as e:
        raise RuntimeError(f"Error reading CSV file: {e}")
