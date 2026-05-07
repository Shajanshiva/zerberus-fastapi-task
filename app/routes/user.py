from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix = "/users", tags = ["Users"])

#create user
@router.post("/", response_model = UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_with_dept = db.query(User).filter(User.id == new_user.id).first()
    return user_with_dept  

#get all users
@router.get("/", response_model = list[UserResponse])
def get_users(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return users

#get user by id
@router.get("/{user_id}", response_model = UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user
    