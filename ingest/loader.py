
import logging
logging.getLogger("pypdf").setLevel(logging.ERROR)

import pandas as pd
from config import MANIFEST_PATH
from config import RAW_DATA_DIR
from langchain_community.document_loaders import PyPDFLoader

def load_documents():
    print("Loading documents...")
    manifest = pd.read_csv(MANIFEST_PATH)

    documents = []

    for _, row in manifest.iterrows():

        pdf_path = RAW_DATA_DIR / row["filename"]

        if not pdf_path.exists():
            print(f"Warning: {row['filename']} not found.")
            continue

        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()

        for page in pages:

            page.metadata = {
                "source": pdf_path.name,
                "page": page.metadata["page"],
                "total_pages": page.metadata["total_pages"],
                "case_name": row["case_name"],
                "decision_date": row["decision_date"],
                "court_level": row["court_level"],
                "docket_number": row["docket_number"],
                "status": row["status"],
                "superseded_by": row["superseded_by"],
            }

            documents.append(page)
    print(f"Loaded {len(documents)} pages from {len(manifest)} documents.")
    return documents