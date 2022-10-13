from flask import Blueprint
from app.controller.food_controller import delete_multiple_food, get_all_food, get_food_by_id, delete_food, delete_multiple_food, add_food, update_food, update_multiple_foods

bp = Blueprint('bp_food', __name__, url_prefix='/food')

bp.get('')(get_all_food)
bp.get('/<string:food_id>')(get_food_by_id)
bp.delete('/<string:food_id>')(delete_food)
bp.delete('/<int:meal_number>')(delete_multiple_food)
bp.post('/<string:user_id>')(add_food)
bp.patch('/<string:food_id>')(update_food)
bp.patch('/<int:meal_number>')(update_multiple_foods)