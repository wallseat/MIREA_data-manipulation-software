from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.providers import get_session
from app.core.security import create_access_token, verify_password
from app.core.const import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.http_exceptions import credentials_exception
from app.schemas.token import Token
from app.crud.user import crud_user


from .v1 import v1_router

api_router = APIRouter()

api_router.include_router(v1_router, prefix="/v1")


@api_router.post("/token", response_model=Token, tags=["token"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    db_obj = await crud_user.get_by_name(db, name=form_data.username)
    if not db_obj:
        raise credentials_exception

    if not verify_password(form_data.password, db_obj.password_hash):
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_obj.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


__all__ = ["api_router"]
