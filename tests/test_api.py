import os
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(autouse=True)
def set_token_env(monkeypatch):
	monkeypatch.setenv("API_TOKEN", "test-token")
	yield


def get_client():
	return TestClient(app)


def test_health():
	client = get_client()
	r = client.get("/health")
	assert r.status_code == 200
	assert r.json()["status"] == "ok"


def test_add_note_requires_auth():
	client = get_client()
	r = client.post("/add_note", json={"patient_id": "P001", "note": "n"})
	assert r.status_code == 401


def test_add_note_and_search_flow():
	client = get_client()
	headers = {"X-API-Token": "test-token"}
	payload = {"patient_id": "P001", "note": "Patient reports chest pain and shortness of breath."}
	r = client.post("/add_note", headers=headers, json=payload)
	assert r.status_code == 200
	assert r.json()["status"] == "ok"

	r2 = client.get("/search_notes", headers=headers, params={"q": "shortness of breath"})
	assert r2.status_code == 200
	body = r2.json()
	assert isinstance(body, list)
	assert len(body) >= 1
	assert body[0]["patient_id"] == "P001"
