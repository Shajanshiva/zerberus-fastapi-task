from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.department import Department
from app.models.address import Address
from app.redis_client import redis_client

import json

def sync_user_cache():
    db: Session = SessionLocal()
    try:
        print("Syncing user cache from database...")
        users = db.query(User).all()
        user_data = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "department": {
                    "id": user.department.id,
                    "name": user.department.name
                    } if user.department else None,
                "addresses": [
                    {
                        "id": address.id,  
                        "street": address.street,
                        "city": address.city,
                        "state": address.state,
                        "country": address.country,
                        "user_id": address.user_id
                    } for address in user.addresses
        ]
            } for user in users
        ]
        redis_client.set("users", json.dumps(user_data),ex=60)
        print("User cache synced successfully.", flush=True)

    finally:
        db.close()

    
def sync_department_cache():
    db: Session = SessionLocal()
    try:
        print("Syncing department cache from database...")
        departments = db.query(Department).all()
        department_data = [
            {
                "id": dept.id,
                "name": dept.name
            } for dept in departments
        ]
        redis_client.set("departments", json.dumps(department_data),ex=60)
        print("Department cache synced successfully.", flush=True)

    finally:
        db.close()

    
def sync_address_cache():
    db: Session = SessionLocal()
    try:
        print("Syncing address cache from database...")
        addresses = db.query(Address).all()
        address_data = [
            {
                "id": address.id,
                "street": address.street,
                "city": address.city,
                "state": address.state,
                "country": address.country,
                "user_id": address.user_id
            } for address in addresses
        ]
        redis_client.set("addresses", json.dumps(address_data),ex=60)
        print("Address cache synced successfully.", flush=True)

    finally:
        db.close()

scheduler = BackgroundScheduler()

scheduler.add_job(sync_user_cache, 'interval', seconds=60)
scheduler.add_job(sync_department_cache, 'interval', seconds=60)
scheduler.add_job(sync_address_cache, 'interval', seconds=60)

scheduler.start()