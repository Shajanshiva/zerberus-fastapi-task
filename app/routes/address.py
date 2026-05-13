from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressResponse
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt_handler import decode_access_token
from app.redis_client import redis_client
import json

router = APIRouter(prefix = "/addresses", tags = ["Addresses"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#create address for a user
@router.post("/users/{user_id}", response_model = AddressResponse)
def create_address_for_user(user_id: int, address: AddressCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")

    new_address = Address(**address.model_dump(), user_id = user_id)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    redis_client.delete(f"user_addresses:{user_id}")
    redis_client.delete(f"user:{user_id}")
    redis_client.delete("users")    

    return new_address

#get all addresses for a user
@router.get("/users/{user_id}", response_model = list[AddressResponse])
def get_addresses_for_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    cache_key = f"user_addresses:{user_id}"
    cached_addresses = redis_client.get(cache_key)

    if cached_addresses:
        print("Fetching addresses from Redis cache")
        return json.loads(cached_addresses)
    print("Fetching addresses from database")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    if not user.addresses:
        raise HTTPException(status_code = 404, detail = "No addresses found for this user")
    
    addresses_data = [{
        "id": address.id,
        "street": address.street,
        "city": address.city,
        "state": address.state,
        "country": address.country,
        "user_id": address.user_id
    } for address in user.addresses]

    redis_client.set(cache_key, json.dumps(addresses_data), ex=60)

    return addresses_data

#get address by id
@router.get("/{address_id}", response_model = AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    cache_key = f"address:{address_id}"
    cached_address = redis_client.get(cache_key)

    if cached_address:
        print("Fetching address from Redis cache")
        return json.loads(cached_address)

    print("Fetching address from database")

    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code = 404, detail = "Address not found")

    address_data = {
        "id": address.id,
        "street": address.street,
        "city": address.city,
        "state": address.state,
        "country": address.country,
        "user_id": address.user_id
    }
    redis_client.set(cache_key, json.dumps(address_data), ex=60)

    return address_data

#update address
@router.put("/{address_id}", response_model = AddressResponse)
def update_address(address_id: int, address_update: AddressCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code = 404, detail = "Address not found")
    
    address.street = address_update.street
    address.city = address_update.city
    address.state = address_update.state
    address.country = address_update.country
    db.commit()
    db.refresh(address)
    redis_client.delete(f"address:{address_id}")
    redis_client.delete(f"user_addresses:{address.user_id}")
    redis_client.delete(f"user:{address.user_id}")
    redis_client.delete("users")
    return address

#delete address
@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decode_access_token(token)
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code = 404, detail = "Address not found")
    
    db.delete(address)
    db.commit()
    redis_client.delete(f"address:{address_id}")
    redis_client.delete(f"user_addresses:{address.user_id}")
    redis_client.delete(f"user:{address.user_id}")
    redis_client.delete("users")
    return {"detail": "Address deleted successfully"}   