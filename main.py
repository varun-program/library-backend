from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routes import router

app = FastAPI(
    title="Library Management System API",
    version="1.0"
)

# Create database tables automatically
Base.metadata.create_all(bind=engine)

# CORS configuration
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


# Root route for testing
@app.get("/")
def home():
    return {"message": "Library Management API Running"}
