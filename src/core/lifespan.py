from contextlib import asynccontextmanager

from src.core.logger import setup_logger
from src.core.db import db
from src.core.http_client import http
from src.core.executor import executor


@asynccontextmanager
async def lifespan(app):
    setup_logger()

    http.init()

    db.init()

    executor.init()

    yield

    await http.aclose()

    db.dispose()

    executor.shutdown()
