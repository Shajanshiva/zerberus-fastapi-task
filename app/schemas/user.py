from pydantic import BaseModel, EmailStr, Field
from app.schemas.department import DepartmentResponse
from app.schemas.address import AddressResponse

class UserCreate(BaseModel):
    # name: str
    first_name: str = Field(..., min_length=3, max_length=25)
    last_name: str = Field(..., min_length=3, max_length=25)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=8)
    department_id: int

class UserResponse(BaseModel):
    id: int
    # name: str
    first_name: str
    last_name: str
    email: str
    phone: str
    department: DepartmentResponse
    addresses: list[AddressResponse] = []

    class Config:
        from_attributes = True

UserResponse.model_rebuild()