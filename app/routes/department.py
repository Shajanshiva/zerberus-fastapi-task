from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentResponse
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt_handler import decode_access_token
from app.redis_client import redis_client
import json

router = APIRouter(prefix = "/departments", tags = ["Departments"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#create department
@router.post("/", response_model = DepartmentResponse)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    existing_dept = db.query(Department).filter(Department.name == dept.name).first()
    if existing_dept:
        raise HTTPException(status_code=400, detail="Department already exists")

    new_dept = Department(name = dept.name)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)

    redis_client.delete("departments")

    return new_dept

#get all departments
@router.get("/", response_model = list[DepartmentResponse])
def get_departments(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)

    cached_departments = redis_client.get("departments")

    if cached_departments:
        print("Fetching departments from Redis cache")
        return json.loads(cached_departments)
    
    print("Fetching departments from database")

    departments = db.query(Department).all()

    departments_data = [{"id": dept.id, "name": dept.name} for dept in departments]

    redis_client.set("departments", json.dumps(departments_data), ex=60)

    return departments_data

#get department by id
@router.get("/{dept_id}", response_model = DepartmentResponse)
def get_department(dept_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)

    cache_key = f"department:{dept_id}"
    cached_department = redis_client.get(cache_key)

    if cached_department:
        print(f"Fetching department from Redis cache")
        return json.loads(cached_department)

    print(f"Fetching department from database")

    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    dept_data = {"id": dept.id, "name": dept.name}
    redis_client.set(cache_key, json.dumps(dept_data), ex=60)

    return dept_data

#update department
@router.put("/{dept_id}", response_model = DepartmentResponse)
def update_department(dept_id: int, dept_update: DepartmentCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    dept.name = dept_update.name
    db.commit()
    db.refresh(dept)

    redis_client.delete("departments")
    redis_client.delete(f"department:{dept_id}")

    return dept

#delete department
@router.delete("/{dept_id}")
def delete_department(dept_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db.delete(dept)
    db.commit()

    redis_client.delete("departments")
    redis_client.delete(f"department:{dept_id}")

    return {"detail": "Department deleted successfully"}