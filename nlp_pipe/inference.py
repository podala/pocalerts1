import sys
import os
import json
import logging
from nlp_pipeline.config import load_config
from nlp_pipeline.preprocess import preprocess_text
from nlp_pipeline.search import SemanticSearch, get_search_results
from nlp_pipeline.utils import setup_logging, log_results
from nlp_pipeline.data_loader import read_notes_from_csv

# Add the parent directory of `nlp_pipeline` to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

def perform_inference(query):
    # Setup logging
    setup_logging()

    # Load configuration
    config = load_config()

    # Load the model index
    searcher = SemanticSearch(config['pretrained_model'])
    searcher.load_index(config['model_save_path'])
    logging.info(f"Index loaded from {config['model_save_path']}")

    # Preprocess the query
    preprocessed_query = preprocess_text(query, config['synonyms'])

    # Perform search
    indices, distances = searcher.search(preprocessed_query, k=config['search_results_count'])

    # Read notes from CSV (assuming small enough to fit in memory for inference)
    try:
        notes = []
        for batch in read_notes_from_csv(config['csv_file_path'], chunk_size=config['batch_size']):
            notes.extend(batch)
        logging.info(f"Successfully read {len(notes)} notes from CSV.")
    except Exception as e:
        logging.error(e)
        return []

    # Get search results
    results = get_search_results(indices, distances, notes)

    # Log and display results
    log_results(results)

    # Return results in JSON format
    results_json = json.dumps(results, indent=2)
    return results_json

if __name__ == "__main__":
    # Example keyword
    query = "follow up on eligibility termination"
    results_json = perform_inference(query)
    print(results_json)
