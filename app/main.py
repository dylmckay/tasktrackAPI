import logging
import sys

from fastapi import FastAPI
from routers.task import router

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = FastAPI(title="TaskTrackAPI")

app.include_router(router)
