from fastapi import FastAPI
from backend.routers import sample_router
from fastapi.middleware.cors import CORSMiddleware

API_VERSION_PREFIX = "/api/1"

app = FastAPI()


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
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "UP"}


app.include_router(sample_router.router, prefix=API_VERSION_PREFIX)
