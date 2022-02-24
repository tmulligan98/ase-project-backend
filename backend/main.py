from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from backend.utils import SETTINGS
from backend.database_wrapper import (
    Base,
    ENGINE,
)
from backend.routers import (
    database_wrapper_router,
    external_api_router,
    sample_router,
    authentication_router,
)

from backend.utils import init_logger


API_VERSION_PREFIX = "/api/1"
Base.metadata.drop_all(bind=ENGINE)
Base.metadata.create_all(bind=ENGINE)

app = FastAPI()

# This is really useful...
logger = init_logger()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    DBSessionMiddleware,
    db_url=SETTINGS.database_url,
)


@app.on_event("startup")
async def start_up():
    logger.info("Starting up...")


@app.get("/")
def hello():
    """
    Hello to Server
    """

    # Return body
    return {
        "disasterStatus": True,
        "disasterLocation": {
            "longitude": 0,
            "latitude": 0,
        },
    }


@app.get("/health")
async def health_check():
    return {"status": "UP"}


app.include_router(sample_router.router, prefix=API_VERSION_PREFIX)
app.include_router(external_api_router.router, prefix=API_VERSION_PREFIX)
app.include_router(database_wrapper_router.router, prefix=API_VERSION_PREFIX)
app.include_router(authentication_router.router, prefix=API_VERSION_PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
