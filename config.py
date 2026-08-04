from pathlib import Path

# ==========================
# Project Paths
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

MANIFEST_PATH = DATA_DIR / "manifest.csv"

VECTOR_DB_DIR = PROJECT_ROOT / "vectordb" / "chroma_db"

# ==========================
# Chunking
# ==========================

CHUNK_SIZE = 700
CHUNK_OVERLAP = 140

# ==========================
# Models
# ==========================

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1"

# ==========================
# Vector Collection Name
# ==========================
COLLECTION_NAME = "legal_cases"