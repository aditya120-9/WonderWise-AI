# WonderWise Knowledge Base

Place approved, dated `.txt`, `.md`, or `.pdf` travel documents here before running ingestion.

Use official tourism boards, transport operators, hotel providers, and other trusted publishers. Prices and availability must include a date and source URL when possible.

The chatbot cannot provide real current prices while this folder is empty. It will deliberately label unsupported prices as not verified.

For web sources, run `python scripts/ingest_sources.py` from `backend`. If a source blocks secure fetching, download the reviewed document manually and place it here; do not disable TLS verification.