from http import HTTPStatus
from flask import request
from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)

from utils import check_password
from models.user import User

black_list = set()


class RevokeResource(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']

        black_list.add(jti)

        return {'message': 'Succesfully logged out'}, HTTPStatus.OK


class TokenResource(Resource):

    def post(self):
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        print(email, password)
        user = User.get_by_email(email=email)
        print(check_password(password, user.password), user.id)
        if not user or not check_password(password, user.password):
            print('burdayim', type(jsonify({'message': 'username or password is incorrect'})))
            return make_response(jsonify({'message': 'username or password is incorrect'}), HTTPStatus.UNAUTHORIZED)

        #if user.is_active is False:
            #return {'message': 'The user account is not activated yet'}, HTTPStatus.FORBIDDEN

        print('hoppallaa')
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return make_response(jsonify({'access_token': access_token, 'refresh_token': refresh_token}), HTTPStatus.OK)


class RefreshResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()

        access_token = create_access_token(identity=current_user, fresh=False)

        return make_response(jsonify({'access_token': access_token}), HTTPStatus.OK)
