from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.api import auth, tasks, websocket
from app.core.config import settings
import os
from app.api.websocket import schema

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A simple task management API with FastAPI and GraphQL - Local Development"
)

# CORS middleware - Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(websocket.router, prefix="/api", tags=["WebSocket"])

# Include GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Serve static files (for frontend)
if os.path.exists("frontend/dist"):
    app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")
    
    @app.get("/")
    def read_index():
        return FileResponse("frontend/dist/index.html")

@app.get("/api")
def read_root():
    return {
        "message": "TaskFlow API - Local Development",
        "docs": "/docs",
        "graphql": "/graphql",
        "database": "SQLite (taskflow.db)"
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "taskflow-api", "environment": "local"}