from fastapi import HTTPException, status

DEFAULT_HEADERS = {"WWW-Authenticate": "Bearer"}

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers=DEFAULT_HEADERS,
)

permission_denied_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied",
    headers=DEFAULT_HEADERS,
)

x_not_found_exception_factory = lambda x: HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"{x} not found",
    headers=DEFAULT_HEADERS,
)

x_already_exists_exception_factory = lambda x: HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=f"{x} already exists",
    headers=DEFAULT_HEADERS,
)
