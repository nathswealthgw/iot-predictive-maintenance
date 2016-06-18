from fastapi import FastAPI

from app.api.routes import router
from app.config import get_settings
from app.utils.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title=settings.service_name, version="1.0.0")
app.include_router(router)
