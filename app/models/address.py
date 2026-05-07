from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key = True, index = True)
    street = Column(String, nullable = False)
    city = Column(String, nullable = False)
    state = Column(String, nullable = False)
    country = Column(String, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="addresses")