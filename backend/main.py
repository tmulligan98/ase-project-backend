from fastapi import FastAPI
from backend.routers import external_api_router, sample_router
from backend.utils import init_logger
from fastapi.middleware.cors import CORSMiddleware

API_VERSION_PREFIX = "/api/1"

app = FastAPI()
logger = init_logger()


origins = ["http://localhost:3000", "localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello_world():
    return {"Disaster Status": "", "Disaster Location": ""}


@app.get("/health")
async def health_check():
    return {"status": "UP"}


app.include_router(sample_router.router, prefix=API_VERSION_PREFIX)
app.include_router(external_api_router.router, prefix=API_VERSION_PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
