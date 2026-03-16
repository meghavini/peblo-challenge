from fastapi import FastAPI
from app.database import engine, Base
from app.routes import ingest_routes, quiz_routes, student_routes

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Content Ingestion + Adaptive Quiz Engine")

app.include_router(ingest_routes.router)
app.include_router(quiz_routes.router)
app.include_router(student_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Adaptive Quiz Engine API"}
