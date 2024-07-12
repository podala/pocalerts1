import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_results(results):
    for result in results:
        logging.info(f"Note: {result['note']}, Distance: {result['distance']}")
