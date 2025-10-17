from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine, Base

# Import routers
from app.api import auth, events, games, levels, media, progress, leaderboard

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - Allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(games.router, prefix="/api/games", tags=["Games"])
app.include_router(levels.router, prefix="/api", tags=["Levels"])
app.include_router(media.router, prefix="/api", tags=["Media"])
app.include_router(progress.router, prefix="/api", tags=["Progress"])
app.include_router(leaderboard.router, prefix="/api", tags=["Leaderboard"])


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Utsav Games API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}
