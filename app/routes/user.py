from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.auth.auth import hash_password
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt_handler import decode_access_token

router = APIRouter(prefix = "/users", tags = ["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#create user
@router.post("/", response_model = UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    decode_access_token(token)

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_data = user.model_dump()   
    
    user_data["password"] = hash_password(user.password)    

    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_with_dept = db.query(User).filter(User.id == new_user.id).first()
    return user_with_dept  

#get all users
@router.get("/", response_model = list[UserResponse])
def get_users(db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    users = db.query(User).all()
    return users

#get user by id
@router.get("/{user_id}", response_model = UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user

#update user
@router.put("/{user_id}", response_model = UserResponse)
def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    user.first_name = user_update.first_name
    user.last_name = user_update.last_name
    user.email = user_update.email
    user.phone = user_update.phone
    user.department_id = user_update.department_id
    db.commit()
    db.refresh(user)
    return user

#delete user
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
    
    