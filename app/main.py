from fastapi import FastAPI
from app.database.db import init_db
from app.routers import user
import logging
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    logger.info("Starting up database connection")
    await init_db()

# Include versioned routers
app.include_router(
    user.router,
    prefix="/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "API v1 - Welcome to the User Service"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}
