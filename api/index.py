from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from api.api.api_v1.router import router
from api.core.config import settings
from api.models.todo_model import Todo
from api.models.user_model import User

origins = ["*"]

app = FastAPI(
    title="Todo",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def root():
    return {"message": "Hello World, Successfully Deployed!!!"}

@app.on_event("startup")
async def app_init():
    """
        initialize crucial application services
    """
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).Todo
    await init_beanie(
        database=db_client,
        document_models= [
            User,
            Todo
        ]
    )
app.include_router(router, prefix=settings.API_V1_STR)
