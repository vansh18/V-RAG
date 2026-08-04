"""
Auto-generates manifest.csv from whatever PDFs are actually sitting in
data/raw/ — no need to rename files to match a predefined list.

Fixed version: uses langchain_openai's ChatOpenAI correctly (.invoke(),
not .messages.create() — that was the Anthropic SDK's syntax, and mixing
the two is what caused the AttributeError).

Requirements:
    pip install pypdf langchain-openai python-dotenv

.env file should contain:
    OPENAI_API_KEY=your_key_here

Run:
    python manifest_builder.py
"""

import csv
import glob
import json
import os

from pypdf import PdfReader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

RAW_DIR = r"C:/Users/ASUS/OneDrive/Desktop/V-RAG/data/raw"
MANIFEST_PATH = r"C:\Users\ASUS\OneDrive\Desktop\V-RAG\data\manifest.csv"

# temperature=0 for deterministic extraction — you don't want creative
# guessing on case names and dates
client = ChatOpenAI(model="gpt-4o-mini", temperature=0)

EXTRACTION_PROMPT = """You are extracting metadata from the first page(s) of a US court opinion PDF.

Return ONLY a JSON object (no markdown fences, no preamble) with these fields:
{{
  "case_name": "short form, e.g. 'Grutter v. Bollinger'",
  "decision_date": "YYYY-MM-DD, or null if not determinable",
  "court_level": "one of: us_supreme_court, circuit_court, district_court, state_supreme_court, other",
  "docket_number": "as printed, or null"
}}

If you cannot confidently determine a field, use null for it. Do not guess.

Document text:
---
{text}
---"""


def extract_first_pages_text(pdf_path, max_pages=2):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages[:max_pages]:
        text += page.extract_text() or ""
    return text[:4000]  # first page is plenty; cap to keep the call cheap


def extract_metadata(text):
    prompt = EXTRACTION_PROMPT.format(text=text)
    response = client.invoke(prompt)          # <-- was client.messages.create(...)
    raw = response.content.strip()             # <-- was response.content[0].text
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"  WARNING: could not parse model output as JSON: {raw[:200]!r}")
        return {"case_name": None, "decision_date": None,
                "court_level": None, "docket_number": None}


def main():
    pdf_paths = sorted(glob.glob(os.path.join(RAW_DIR, "*.pdf")))
    if not pdf_paths:
        print(f"No PDFs found in {RAW_DIR} — check the path.")
        return

    rows = []
    for path in pdf_paths:
        filename = os.path.basename(path)
        print(f"Processing {filename} ...")
        try:
            text = extract_first_pages_text(path)
            if not text.strip():
                print("  WARNING: no extractable text (likely a scanned/image PDF) — skipping")
                meta = {"case_name": None, "decision_date": None,
                        "court_level": None, "docket_number": None}
            else:
                meta = extract_metadata(text)
        except Exception as e:
            print(f"  FAILED: {e}")
            meta = {"case_name": None, "decision_date": None,
                     "court_level": None, "docket_number": None}

        rows.append({
            "filename": filename,
            "case_name": meta.get("case_name") or "REVIEW MANUALLY",
            "decision_date": meta.get("decision_date") or "",
            "court_level": meta.get("court_level") or "",
            "docket_number": meta.get("docket_number") or "",
            "status": "unknown",       # fill in by hand — see note below
            "superseded_by": "",       # fill in by hand
        })
        print(f"  -> {meta.get('case_name')} ({meta.get('decision_date')})")

    with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "filename", "case_name", "decision_date", "court_level",
            "docket_number", "status", "superseded_by"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {MANIFEST_PATH}")
    print("Next: open the CSV and fill in 'status' + 'superseded_by' by hand")
    print("for the cases you know are landmark overruling events (SFFA, Grutter,")
    print("Hopwood, etc). Leave the rest as 'unknown' — that's fine, it just")
    print("means the prosecutor agent won't have supersession info for those.")


if __name__ == "__main__":
    main()