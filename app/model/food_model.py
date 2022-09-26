from app.configs.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, Integer, ForeignKey, Float, String
from dataclasses import dataclass

@dataclass
class Food(db.Model):
    infos = {'name', 'food_weight', 'carbs', 'protein', 'fat', 'meal'}

    def are_there_extra_keys(req_data):
        req_keys = set(req_data.keys())
        extra_keys = req_keys - Food.infos
        return extra_keys

    id: str
    name: str
    food_weight: float
    carbs: float
    protein: float
    fat: float
    meal: int

    __tablename__ = 'foods'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    food_weight = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    protein = Column(Float, nullable = False)
    fat = Column(Float, nullable=False)
    meal = Column(Integer, nullable = False)
    user_id = Column(UUID(as_uuid=True), db.ForeignKey('users.id'))