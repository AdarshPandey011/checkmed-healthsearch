from pydantic import BaseModel, Field


class AddNoteRequest(BaseModel):
	patient_id: str = Field(min_length=1)
	note: str = Field(min_length=1)


class AddNoteResponse(BaseModel):
	status: str
	id: int


class SearchResult(BaseModel):
	patient_id: str
	note: str
	score: float
