from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    # name = Column(String, nullable = False)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    email = Column(String, unique = True, index = True)
    phone = Column(String, unique = True, nullable = False)
    department_id = Column(Integer,  ForeignKey("departments.id"))
    department = relationship("Department")   
    addresses = relationship("Address", back_populates="user")