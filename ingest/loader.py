
import logging
logging.getLogger("pypdf").setLevel(logging.ERROR)

import pandas as pd
from config import MANIFEST_PATH
from config import RAW_DATA_DIR
from langchain_community.document_loaders import TextLoader

def load_documents():
    print("Loading documents...")
    manifest = pd.read_csv(MANIFEST_PATH)

    documents = []

    for _, row in manifest.iterrows():

        pdf_path = RAW_DATA_DIR / row["filename"]

        if not pdf_path.exists():
            print(f"Warning: {row['filename']} not found.")
            continue

        loader = TextLoader(str(pdf_path), encoding="utf-8")
        pages = loader.load()

        for page in pages:

            page.metadata = {
                "source": pdf_path.name,
                "filename": row["filename"],
                "case_name": row["case_name"],
                "citation": row["citation"],
                "decision_date": row["decision_date"],
                "year": row["year"],
                "court": row["court"],
                "court_level": row["court_level"],
                "opinion_type": row["opinion_type"],
                "author": row["author"],
                "status": row["status"],
                "overruled_by": row["overruled_by"],
                "topic": row["topic"],
                "notes": row["notes"],
            }

            documents.append(page)
    print(f"Loaded {len(documents)} pages from {len(manifest)} documents.")
    return documents