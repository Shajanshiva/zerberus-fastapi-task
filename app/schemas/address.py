from pydantic import BaseModel

class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    country: str
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