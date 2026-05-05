from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentResponse

router = APIRouter(prefix = "/departments", tags = ["Departments"])

#create department
@router.post("/", response_model = DepartmentResponse)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    new_dept = Department(name = dept.name)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

#get all departments
@router.get("/", response_model = list[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return departments