import hashlib
import math
from typing import List
import numpy as np


# Small, deterministic embedding so the service works without heavy models.
# Produces a unit-normalized vector so cosine similarity is just a dot product.
EMBEDDING_DIM = 384


def _text_to_seed(text: str) -> int:
	# Stable seed from sha256(text)
	digest = hashlib.sha256(text.encode("utf-8")).digest()
	# Use first 8 bytes as integer seed
	return int.from_bytes(digest[:8], byteorder="big", signed=False)


def generate_note_embedding(text: str) -> List[float]:
	"""Return a deterministic, unit-normalized embedding for a note.

	This mock keeps the app lightweight and easily swappable for a real model
	like sentence-transformers later without changing call sites.
	"""
	if not text or not text.strip():
		return [0.0] * EMBEDDING_DIM
	seed = _text_to_seed(text.strip().lower())
	rng = np.random.default_rng(seed)
	vec = rng.normal(loc=0.0, scale=1.0, size=EMBEDDING_DIM).astype(np.float32)
	norm = np.linalg.norm(vec)
	if norm == 0.0 or math.isclose(norm, 0.0):
		return [0.0] * EMBEDDING_DIM
	vec = vec / norm
	return vec.tolist()


# Backwards compatibility alias (tests/routes may import embed_text)
embed_text = generate_note_embedding
