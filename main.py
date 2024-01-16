from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.routers import anomalies

# Setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# Initialize app
app = FastAPI()
origins = [
    "http://localhost",
]
# Register middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(anomalies.router, tags=["Anomalies Report"])
