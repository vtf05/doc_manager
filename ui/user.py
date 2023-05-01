from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from module.userMaster import User



class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', help='This field cannot be blank', required=True)
    parser.add_argument('password', help='This field cannot be blank', required=True)

    def post(self):
        status = 200
        data = Login.parser.parse_args()
        admin = User()
        resp = admin.get_user_by_creds(data=data)
        if type(resp) is int:
            status = 500
            resp = {'message': 'Failed', 'result': []}
            return make_response(jsonify(resp), status)
        else:
            return make_response(jsonify(resp), status)


class CreateUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', help='This field cannot be blank', required=True)
    parser.add_argument('password', help='This field cannot be blank', required=True)
    parser.add_argument('level', help='This field cannot be blank', required=True)
    parser.add_argument('name', help='This field cannot be blank', required=True)
    parser.add_argument('password', help='This field cannot be blank', required=True)

    def post(self):
        status = 200
        data = CreateUser.parser.parse_args()
        admin = User()
        print(data)
        resp = admin.add_user(data=data)
        data['level'] = 1
        if type(resp) is int:
            status = 500
            resp = {'message': 'Failed', 'result': []}
            return make_response(jsonify(resp), status)
        else:
            return make_response(jsonify(resp), status)
    
