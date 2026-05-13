from fastapi import FastAPI
from app.database import engine, Base, SessionLocal

from app.models import user, department, address
from app.routes import user, department, address, auth

from app.utils.seed import seed_departments

from app.scheduler import scheduler
 

app = FastAPI()

# Base.metadata.create_all(bind = engine)

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
app.include_router(address.router)
app.include_router(auth.router)