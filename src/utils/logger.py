import logging
from src.config import settings

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.LOGS_DIR / "paper_agent.log"),
            logging.StreamHandler()
        ]
    )