from typing import Optional
from fastapi import status

class CustomException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: Optional[str] = "INTERNAL SERVER ERROR"

