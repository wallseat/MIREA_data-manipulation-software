from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import settings

engine = create_async_engine(settings.POSTGRES_DSN)