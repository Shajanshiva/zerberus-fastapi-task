from pydantic import BaseModel
from app.schemas.department import DepartmentResponse
from app.schemas.address import AddressResponse

class UserCreate(BaseModel):
    # name: str
    first_name: str
    last_name: str
    email: str
    phone: str
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