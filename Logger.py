import logging
from config import LOG_FILE

# Configure Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_query(query, execution_time, cost, tokens_used):
    """
    Logs SQL query execution details.
    """
    logging.info(
        f"Query: {query} | Execution Time: {execution_time}s | Cost: ${cost} | Tokens Used: {tokens_used}"
    )
