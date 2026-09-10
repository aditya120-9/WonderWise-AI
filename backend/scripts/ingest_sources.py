"""Review and ingest approved web sources.

Add only sources you trust and check their terms before running this script.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag.web_ingest import ingest_urls

SOURCES = {
    # Keep this list explicit so every answer can cite a publisher and URL.
    "https://www.wbtourism.gov.in/": "West Bengal Tourism",
}


if __name__ == "__main__":
    print(f"Indexed {ingest_urls(SOURCES)} web chunks.")