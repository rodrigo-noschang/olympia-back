from flask import Blueprint
from app.controller.food_controller import get_all_food, add_food, update_food

bp = Blueprint('bp_food', __name__, url_prefix='/food')

bp.get('')(get_all_food)
bp.post('/<string:user_id>')(add_food)
bp.patch('/<string:food_id>')(update_food)