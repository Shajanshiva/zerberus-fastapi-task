from fastapi import FastAPI
from app.database import engine, Base, SessionLocal

from app.models import user, department
from app.routes import user, department

from app.utils.seed import seed_departments
 

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        seed_departments(db)
    finally:
        db.close()

@app.get("/")
def root():
    return{"message": "API Running"}

app.include_router(user.router)
app.include_router(department.router)
