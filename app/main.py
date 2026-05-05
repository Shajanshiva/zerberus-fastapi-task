from fastapi import FastAPI
from app.database import engine, Base

from app.models import user, department
from app.routes import user, department
 

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get("/")
def root():
    return{"message": "API Running"}

app.include_router(user.router)
app.include_router(department.router)
