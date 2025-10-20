# HealthSearch (FastAPI)

A small FastAPI service that stores clinical notes and supports semantic-like search using embedding vectors and cosine similarity.

This focuses on correctness, simplicity, and production-minded basics (auth, validation, clear errors) without over-engineering.

## Setup

### Requirements
- Python 3.10+
- pip

### Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run
```bash
export API_TOKEN="secret-token"  # change this
uvicorn app.main:app --reload
```

Server runs at `http://127.0.0.1:8000`.

### Auth
Use the header:
```
X-API-Token: <your token>
```
If `API_TOKEN` env var is unset, the default is `secret-token`.

## API

### POST /add_note
Store a note for a patient and its embedding.

Request body:
```json
{
  "patient_id": "P001",
  "note": "Patient reports chest pain and shortness of breath."
}
```

Curl example:
```bash
curl -s -X POST http://127.0.0.1:8000/add_note \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $API_TOKEN" \
  -d '{"patient_id":"P001","note":"Patient reports chest pain and shortness of breath."}'
```

Response:
```json
{ "status": "ok", "id": 1 }
```

### GET /search_notes?q=...
Return top 3 most similar notes by cosine similarity.

Example:
```bash
curl -s "http://127.0.0.1:8000/search_notes?q=shortness%20of%20breath" \
  -H "X-API-Token: $API_TOKEN" | jq
```

Response:
```json
[
  {
    "patient_id": "P001",
    "note": "Patient reports chest pain and shortness of breath.",
    "score": 0.87
  }
]
```

## Design Decisions
- Minimal dependencies: uses a deterministic, seed-based embedding to avoid heavy model downloads. Easy to swap later.
- In-memory store with a simple lock. Keeps code small and easy to reason about.
- Clear validation and HTTP errors (400 for bad input, 401 for bad/missing token).
- Static token header `X-API-Token` read from env for simplicity.

### Trade-offs
- Mock embeddings mean semantic quality is limited. For production, plug in `sentence-transformers` or a hosted vector DB.
- In-memory data is ephemeral; a restart wipes data. For persistence, PostgreSQL with `pgvector` would be the next step.

## Tests
Run tests:
```bash
pytest -q
```

## Project Metadata
- Estimated time: ~2 hours
- Bonus: Minimal tests added; Dockerfile included
- Known limitations: In-memory store, mock embeddings
- Possible improvements: Real embedding model, persistence (Postgres + pgvector), pagination, tracing/metrics

## Notes
Variable names are kept straightforward and human-written. No unnecessary abstractions.
