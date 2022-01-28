from fastapi import FastAPI
from backend.routers import external_api_router, sample_router
from backend.utils import init_logger

API_VERSION_PREFIX = "/api/1"

app = FastAPI()
logger = init_logger()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "UP"}


app.include_router(sample_router.router, prefix=API_VERSION_PREFIX)
app.include_router(external_api_router.router, prefix=API_VERSION_PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
