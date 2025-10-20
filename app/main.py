from typing import List
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.auth import require_token
from app.embeddings import generate_note_embedding
from app.schemas import AddNoteRequest, AddNoteResponse, SearchResult
from app.storage import note_repository


app = FastAPI(title="HealthSearch", version="1.0.0")


@app.get("/health")
async def health() -> dict:
	"""Simple liveness probe."""
	return {"status": "ok"}


@app.post("/add_note", response_model=AddNoteResponse)
async def add_note(payload: AddNoteRequest, _: None = Depends(require_token)) -> AddNoteResponse:
	"""Accept a clinical note, embed it, and store for search."""
	patient_id = payload.patient_id.strip()
	note = payload.note.strip()
	if not patient_id or not note:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="patient_id and note are required")

	vec = generate_note_embedding(note)
	note_id = note_repository.save_note(patient_id=patient_id, note=note, embedding=vec)
	return AddNoteResponse(status="ok", id=note_id)


@app.get("/search_notes", response_model=List[SearchResult])
async def search_notes(q: str = Query(min_length=1), _: None = Depends(require_token)) -> List[SearchResult]:
	"""Embed the query and return top 3 most similar notes by cosine similarity."""
	query = q.strip()
	if not query:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="q is required")
	q_vec = generate_note_embedding(query)
	results = note_repository.search_similar_notes(q_vec, k=3)
	return [SearchResult(patient_id=it.patient_id, note=it.note, score=float(score)) for it, score in results]


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
	# Ensure consistent JSON structure
	return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
