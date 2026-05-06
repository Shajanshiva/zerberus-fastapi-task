from sqlalchemy.orm import Session
from app.models.department import Department

def seed_departments(db:Session):
    default_departments = ["HR", "Engineering", "Sales", "Marketing"]

    for dept_name in default_departments:
        existing_dept = db.query(Department).filter(Department.name == dept_name).first()
        if not existing_dept:
            new_dept = Department(name = dept_name)
            db.add(new_dept)
    db.commit()