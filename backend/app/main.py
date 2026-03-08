from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings

settings = get_settings()


#-- lifespan (startup + shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    #Startup: runs the app starts taking requests
    print(f"Starting {settings.app_name} v{settings.app_version}")
    # Later: DB connection pool, Redis connection will go here
    yield
    #Shutdown: runs when the app is stopping
    print("Shutting down TaskFlow API")
    #Later: close DB pool, close Redis will go here

# -- APP instance--

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A full-featured Team Task Management API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,

)


#-- CORS MIDDLEWARE--
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -- HEALTH CHeck ROUTE--

@app.get("/health", tags=["Health"])
async def health_check():
    return{
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
    }

# -- ROOT--
@app.get("/", tags=["Health"])
async def root():
    return {"message": f"Welcome to {settings.app_name}"}