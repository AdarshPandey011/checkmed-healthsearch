import os
from typing import Optional
from fastapi import Header, HTTPException, status


def get_api_token() -> str:
	# Default token keeps local setup simple; override via env
	return os.getenv("API_TOKEN", "secret-token")


def require_token(x_api_token: Optional[str] = Header(default=None, alias="X-API-Token")) -> None:
	expected = get_api_token()
	if not x_api_token or x_api_token != expected:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid or missing API token",
		)
