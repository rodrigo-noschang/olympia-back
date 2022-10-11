from app.exc.exc import NonAuthenticated, SessionExpired
from app.model.food_model import Food
from flask import jsonify, request, current_app
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm.exc import UnmappedInstanceError
from psycopg2.errors import ForeignKeyViolation, NotNullViolation, InvalidColumnReference, InvalidTextRepresentation
from .token_required_controller import token_required

def get_all_food():
    foods = Food.query.order_by(Food.name).all()

    return jsonify(foods)

def get_food_by_id(food_id: str):
    try:
        food = Food.query.filter_by(id = food_id).first()

        if not food:
            return {"msg": "Alimento não encontrado"}, 404

        return jsonify(food)
    except DataError as err:
        if isinstance(err.orig, InvalidTextRepresentation):
            return {"msg": "Alimento não encontrado"}, 404


def delete_food(food_id: str):
    try:
        food = Food.query.get(food_id)

        current_app.db.session.delete(food)
        current_app.db.session.commit()

        return jsonify(food), 201
    
    except UnmappedInstanceError:
        return {"msg": "Alimento não encontrado"}, 404



def add_food(user_id: str):
    try:
        req_data = request.json

        token_required()

        if Food.are_there_extra_keys(req_data):
           raise InvalidColumnReference 

        req_data['user_id'] = user_id

        new_food = Food(**req_data)
        current_app.db.session.add(new_food)
        current_app.db.session.commit()

        return jsonify(new_food)

    except IntegrityError as err:
        if isinstance(err.orig, ForeignKeyViolation):
            return {"msg": "Usuário não encontrado"}, 400
        if isinstance(err.orig, NotNullViolation):
            return {"msg": "Chave(s) faltando na requisição"}, 400
        
    except InvalidColumnReference as err:
        return {"msg": "Chave(s) inválida(s) na requisição"}, 400
    except DataError as err:
        if isinstance(err.orig, InvalidTextRepresentation):
            return {"msg": "Tipo de dado inválido na requisição"}, 400

    except NonAuthenticated as err:
        return {"msg": "Precisa estar logado"}, 401
    except SessionExpired as err:
        return {"msg": "Sessão expirada"}, 400


def update_food(food_id: str):
    try:
        token_required()

        update_data = request.json
        if Food.are_there_extra_keys(update_data):
            raise InvalidColumnReference

        Food.query.filter_by(id=food_id).update(update_data)

        updated_db_food = Food.query.get(food_id)
        current_app.db.session.commit()

        return jsonify(updated_db_food)

    except InvalidColumnReference as err:
        return {"msg": "Chave(s) inválida(s) na requisição"}, 400
    except DataError as err:
        if isinstance(err.orig, InvalidTextRepresentation):
            return {"msg": "Tipo de dado inválido na requisição ou alimento não existe"}, 400
    except NonAuthenticated as err:
        return {"msg": "Precisa estar logado"}, 401
    except SessionExpired as err:
        return {"msg": "Sessão expirada"}, 400