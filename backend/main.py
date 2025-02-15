import logging

import uvicorn

from core.config import settings

from api import router as api_router
from create_fast_api_app import create_app

main_app = create_app(
    create_custom_static_urls=False,
)

main_app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
