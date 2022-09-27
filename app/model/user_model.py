from sqlalchemy import Column, Integer, String, Float
from app.configs.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dataclasses import dataclass
from .food_model import Food
from typing import List

@dataclass
class User(db.Model):
    infos = {'id', 'name', 'email', 'password', 'weight', 'height', 'age', 'gender'}

    id: str
    name: str
    email: str
    password: str
    weight: str
    height: str
    age: str
    gender: str
    foods: List[Food]

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    weight = Column(Float)
    height = Column(Float)
    age = Column(Integer)
    gender = Column(String, nullable = False)
    foods = db.relationship('Food', backref = 'users', cascade = 'all, delete-orphan')
