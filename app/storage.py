from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class StoredNote:
	id: int
	patient_id: str
	note: str
	embedding: np.ndarray  # unit-normalized


class InMemoryStore:
	def __init__(self) -> None:
		self._lock = threading.Lock()
		self._items: List[StoredNote] = []
		self._next_id = 1

	def add(self, patient_id: str, note: str, embedding: List[float]) -> int:
		vec = np.array(embedding, dtype=np.float32)
		with self._lock:
			item = StoredNote(id=self._next_id, patient_id=patient_id, note=note, embedding=vec)
			self._items.append(item)
			self._next_id += 1
			return item.id

	def top_k(self, query_vec: List[float], k: int) -> List[Tuple[StoredNote, float]]:
		if not self._items:
			return []
		q = np.array(query_vec, dtype=np.float32)
		# embeddings are already unit normalized; cosine == dot
		scores = [float(np.dot(q, it.embedding)) for it in self._items]
		idx = np.argsort(scores)[::-1]  # descending
		results: List[Tuple[StoredNote, float]] = []
		for i in idx[:k]:
			results.append((self._items[int(i)], scores[int(i)]))
		return results


class NoteRepository:
	"""Thin repository over the chosen persistence layer.

	Abstracting here lets us swap to PostgreSQL/pgvector later without changing
	the calling service/route layers.
	"""

	def __init__(self, backend: InMemoryStore | None = None) -> None:
		self._backend = backend or InMemoryStore()

	def save_note(self, patient_id: str, note: str, embedding: List[float]) -> int:
		return self._backend.add(patient_id=patient_id, note=note, embedding=embedding)

	def search_similar_notes(self, query_vec: List[float], k: int) -> List[Tuple[StoredNote, float]]:
		return self._backend.top_k(query_vec, k)


# Default repository used by the app
store = InMemoryStore()
note_repository = NoteRepository(store)
