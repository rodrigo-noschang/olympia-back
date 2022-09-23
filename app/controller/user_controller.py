from flask import jsonify, request, current_app
from app.model.user_model import User
from sqlalchemy.exc import InvalidRequestError, DataError, ProgrammingError, IntegrityError
from psycopg2.errors import UniqueViolation, NotNullViolation

def get_all_users():
    users = User.query.all()
    
    return jsonify(users)


def update_user_info(user_id: str):
    try:
        new_data = request.json
        User.query.filter_by(id=user_id).update(new_data)

        current_app.db.session.commit()

        updated_user = User.query.get(user_id)

        return jsonify(updated_user)

    except InvalidRequestError:
        return {"error": "invalid keys"}, 400
    except DataError:
        return {"error": "invalid data type"}, 400
    except ProgrammingError:
        return {"error": "missing keys"}, 400
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            return {"error": "name or email already exists"}, 403

def create_user():
    try:
        new_user_data = request.json
        invalid_keys = set(new_user_data.keys()) - User.infos
        
        if invalid_keys:
            raise(InvalidRequestError)

        # Check if there already is a user with that name
        existing_user = User.query.filter_by(name=new_user_data['name']).first()
        if existing_user:
            raise UniqueViolation 

        # Check if there already is a user with that email
        existing_user = User.query.filter_by(email=new_user_data['email']).first()
        if existing_user:
            raise UniqueViolation

        new_user = User(**new_user_data)

        session = current_app.db.session
        session.add(new_user)
        session.commit()

        new_user_created = User.query.filter_by(email=new_user.email).first()

        return jsonify(new_user_created)
    except IntegrityError as err:
        if isinstance(err.orig, NotNullViolation):
            return {"msg": "missing name, email or password"}, 400
    except InvalidRequestError as err:
        return {"msg": "invalid keys in the request"}, 400
    except UniqueViolation as err:
        return {"msg": "name or email already exists"}, 400
