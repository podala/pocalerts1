import logging
import json
from nlp_pipeline.config import load_config
from nlp_pipeline.data_loader import read_notes_from_csv
from nlp_pipeline.preprocess import preprocess_text
from nlp_pipeline.search import SemanticSearch, get_search_results
from nlp_pipeline.utils import setup_logging, log_results

def main():
    # Setup logging
    setup_logging()
    
    # Load configuration
    config = load_config()

    # Read notes from CSV
    try:
        notes = read_notes_from_csv(config['csv_file_path'])
        logging.info(f"Successfully read {len(notes)} notes from CSV.")
    except RuntimeError as e:
        logging.error(e)
        return

    # Preprocess notes
    preprocessed_notes = [preprocess_text(note, config['synonyms']) for note in notes]

    # Create semantic search object
    searcher = SemanticSearch(config['pretrained_model'])
    
    # Create embeddings
    embeddings = searcher.create_embeddings(preprocessed_notes)
    logging.info("Embeddings created successfully.")
    
    # Build index
    searcher.build_index(embeddings)
    logging.info("Index built successfully.")

    # Example query
    query = "Need to follow up on eligibility termination."
    preprocessed_query = preprocess_text(query, config['synonyms'])
    
    # Perform search
    indices, distances = searcher.search(preprocessed_query)

    # Get search results
    results = get_search_results(indices, distances, notes)

    # Log and display results
    log_results(results)

    # Output results in JSON format
    results_json = json.dumps(results, indent=2)
    print(results_json)

if __name__ == "__main__":
    main()
