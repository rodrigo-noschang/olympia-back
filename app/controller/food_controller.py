from app.model.food_model import Food
from flask import jsonify, request, current_app
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2.errors import ForeignKeyViolation, NotNullViolation, InvalidColumnReference, InvalidTextRepresentation

def get_all_food():
    foods = Food.query.all()

    return jsonify(foods)


def add_food(user_id: str):
    try:
        req_data = request.json

        if Food.are_there_extra_keys(req_data):
           raise InvalidColumnReference 

        req_data['user_id'] = user_id

        new_food = Food(**req_data)
        current_app.db.session.add(new_food)
        current_app.db.session.commit()

        return jsonify(new_food)

    except IntegrityError as err:
        if isinstance(err.orig, ForeignKeyViolation):
            return {"msg": "user does not exist"}, 400

        if isinstance(err.orig, NotNullViolation):
            return {"msg": "missing keys"}, 400
        
    except InvalidColumnReference as err:
        return {"msg": "invalid keys in the request"}, 400

    except DataError as err:
        if isinstance(err.orig, InvalidTextRepresentation):
            return {"msg": "invalid data type in the request"}, 400


def update_food(food_id: str):
    try:
        update_data = request.json
        if Food.are_there_extra_keys(update_data):
            raise InvalidColumnReference

        Food.query.filter_by(id=food_id).update(update_data)

        updated_db_food = Food.query.get(food_id)
        current_app.db.session.commit()

        return jsonify(updated_db_food)

    except InvalidColumnReference as err:
        return {"msg": "invalid keys in the request"}, 400
    except DataError as err:
        if isinstance(err.orig, InvalidTextRepresentation):
            return {"msg": "invalid data type in the request or food does not exists"}, 400