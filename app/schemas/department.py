from pydantic import BaseModel, Field

class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length = 3, max_length = 25)

class DepartmentResponse(BaseModel):
    id: int
    name : str

    class Config:
        from_attributes = True