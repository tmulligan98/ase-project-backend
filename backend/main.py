from fastapi import FastAPI

from backend.routers import sample_router

API_VERSION_PREFIX = "/api/1"

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "UP"}


app.include_router(sample_router.router, prefix=API_VERSION_PREFIX)
