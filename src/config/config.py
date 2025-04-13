import os
from pathlib import Path
from datetime import date

class Settings:
    DATE = date.today()
    # Paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    DATA_DIR = BASE_DIR / "data"
    DB_PATH = DATA_DIR / "papers_db"
    LOGS_DIR = DATA_DIR / "logs"
    
    # URLs
    HUGGINGFACE_PAPERS_URL = "https://huggingface.co"
    ARXIV_PDF_URL = "https://arxiv.org/pdf/"
    PAPER_DATE = f"/papers/date/{DATE}"
    
    # Model config
    SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
    EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
    
settings = Settings()