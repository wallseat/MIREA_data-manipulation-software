from fastapi import FastAPI
from asyncpg.connection import connect

from app.core.settings import settings
from app.api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api")
    
if __name__ == '__main__':
    try:
        import uvicorn
    except ImportError:
        pass
    else:
        uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)