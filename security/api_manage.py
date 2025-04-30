from fastapi import HTTPException, Request, Security
from fastapi.security.api_key import APIKeyHeader
from typing import Optional

_API_KEY = "1234567890"  # Define your API key
_API_KEY_NAME = "TEST_KEY"  # The header key for the API key
api_key_header = APIKeyHeader(name=_API_KEY_NAME)

# Dependency to check API key
def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key != _API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized. Invalid API key.",
        )
    return api_key
