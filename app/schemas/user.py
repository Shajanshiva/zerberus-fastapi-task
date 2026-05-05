from pydantic import BaseModel
from app.schemas.department import DepartmentResponse

class UserCreate(BaseModel):
    name: str
    email: str
    department_id: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    department: DepartmentResponse

    class config:
        from_attributes = True

UserResponse.model_rebuild()