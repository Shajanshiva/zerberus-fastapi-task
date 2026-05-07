from pydantic import BaseModel, Field

class AddressCreate(BaseModel):
    street: str = Field(..., min_length=5, max_length=100)
    city: str = Field(..., min_length=2, max_length=50)
    state: str = Field(..., min_length=2, max_length=50)
    country: str = Field(..., min_length=2, max_length=50)
    # user_id: int

class AddressResponse(BaseModel):
    id: int
    street: str
    city: str
    state: str
    country: str
    user_id: int

    class Config:
        from_attributes = True