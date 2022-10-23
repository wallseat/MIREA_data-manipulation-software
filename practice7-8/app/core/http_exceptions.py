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


user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
    headers=DEFAULT_HEADERS,
)

user_already_exists_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User already exists",
    headers=DEFAULT_HEADERS,
)

group_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Group not found",
    headers=DEFAULT_HEADERS,
)

organization_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Organization not found",
    headers=DEFAULT_HEADERS,
)

organization_already_exists_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Organization already exists",
    headers=DEFAULT_HEADERS,
)

contact_person_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Contact person not found",
    headers=DEFAULT_HEADERS,
)

contact_person_already_exists_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Contact person already exists",
    headers=DEFAULT_HEADERS,
)
