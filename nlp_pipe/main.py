import sys
import os
import logging
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from nlp_pipeline.config import load_config
from nlp_pipeline.data_loader import read_notes_from_csv
from nlp_pipeline.preprocess import preprocess_text
from nlp_pipeline.search import SemanticSearch, get_search_results
from nlp_pipeline.utils import setup_logging, log_results

# Add the parent directory of `nlp_pipeline` to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

def process_batch(batch, config):
    # Preprocess notes
    preprocessed_notes = [preprocess_text(note, config['synonyms']) for note in batch]

    # Create embeddings
    searcher = SemanticSearch(config['pretrained_model'])
    embeddings = searcher.create_embeddings(preprocessed_notes)
    logging.info(f"Created embeddings for batch of size {len(preprocessed_notes)}")
    return embeddings

def main():
    # Setup logging
    setup_logging()

    # Load configuration
    config = load_config()

    # Initialize semantic search object
    searcher = SemanticSearch(config['pretrained_model'])

    # Read notes and process in batches
    embedding_dim = None
    all_embeddings = []

    with ProcessPoolExecutor(max_workers=config['num_workers']) as executor:
        futures = []
        try:
            for batch in read_notes_from_csv(config['csv_file_path'], chunk_size=config['batch_size']):
                futures.append(executor.submit(process_batch, batch, config))
            
            for future in as_completed(futures):
                embeddings = future.result()
                all_embeddings.append(embeddings)

                if embedding_dim is None:
                    embedding_dim = embeddings.shape[1]
                    searcher.build_index(embedding_dim)
                
                # Add embeddings to the index
                searcher.add_to_index(embeddings)
                logging.info(f"Added batch embeddings to index")

        except Exception as e:
            logging.error(e)
            return

    # Save the model index
    searcher.save_index(config['model_save_path'])
    logging.info(f"Index saved to {config['model_save_path']}")

if __name__ == "__main__":
    main()
