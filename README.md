# HealthSearch

A small FastAPI service to store clinical notes and search them semantically using cosine similarity over embeddings. I kept it simple and easy to run locally.

## Getting started

Requirements
- Python 3.10+

Install and run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export API_TOKEN="secret-token"   # change if you want
uvicorn app.main:app --reload
```

Auth header
```
X-API-Token: <your token>
```
If the env var isn’t set, it defaults to `secret-token`.

## Endpoints

POST /add_note
- Body:
```json
{
  "patient_id": "P001",
  "note": "Patient reports chest pain and shortness of breath."
}
```
- Example:
```bash
curl -s -X POST http://127.0.0.1:8000/add_note \
  -H "Content-Type: application/json" \
  -H "X-API-Token: $API_TOKEN" \
  -d '{"patient_id":"P001","note":"Patient reports chest pain and shortness of breath."}'
```
- Response:
```json
{ "status": "ok", "id": 1 }
```

GET /search_notes?q=...
- Returns the top 3 most similar notes.
- Example:
```bash
curl -s "http://127.0.0.1:8000/search_notes?q=shortness%20of%20breath" \
  -H "X-API-Token: $API_TOKEN"
```
- Sample response:
```json
[
  {
    "patient_id": "P001",
    "note": "Patient reports chest pain and shortness of breath.",
    "score": 0.87
  }
]
```

## Tests
```bash
pytest -q
```
