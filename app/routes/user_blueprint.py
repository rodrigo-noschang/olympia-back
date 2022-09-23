from flask import Blueprint
from app.controller.user_controller import get_all_users, update_user_info, create_user

bp = Blueprint("bp_user", __name__, url_prefix = '/user')
bp.get('')(get_all_users)
bp.patch('/<string:user_id>')(update_user_info)
bp.post('')(create_user)