import jwt
import os
from werkzeug.datastructures import FileStorage
from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from module.fileMaster import FileMaster
# options={'verify_nbf': False}).get('identity')

def jwt_verification(data):
    try:
        print(data['Authorization'].split(" ")[1])
        # print(jwt.decode('data['Authorization'].split(" ")[1]', os.environ.get('SECRET_KEY'),algorithms='HS256'))) 
        user_id = int(jwt.decode(data['Authorization'].split(" ")[1], os.environ.get('SECRET_KEY'),algorithms='HS256').get('identity'))
        return 200 , user_id
    except jwt.ExpiredSignatureError:
        status = 401
        resp = {'message': 'AUTH.TOKEN_EXPIRED'}
        resp = {'error' : resp }
        return status , resp
    except jwt.InvalidTokenError:
        status = 498
        print("this is invalid token")
        resp = {'message': 'AUTH.TOKEN_INVALID'}
        resp = {'error' : resp }
        return status , resp
    except jwt.InvalidSignatureError:
        status = 401
        resp = {'message': 'AUTH.CREDENTIALS_INVALID'}
        resp = {'error' : resp }
        return status , resp
    except Exception as e :
        print(e)
        status = 498
        resp = {'message': 'AUTH.TOKEN_INVALID'}
        resp = {'error' : resp}
        return status , resp

class UploadFile(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', location='headers', required=True)
        parser.add_argument('file', location='files', type=FileStorage, required=True)
        parser.add_argument('folder',location='form', help='This field cannot be blank', required=True)
        status = 200
        data = parser.parse_args()
        st, user_id = jwt_verification(data)
        if st != 200 :
            return make_response(jsonify(user_id), st)
        f_master = FileMaster()
        data['user_id'] = 1
        resp = f_master.addfile(data=data)
        if type(resp) is int:
            status = 500
            resp = {'message': 'Failed', 'result': []}
            return make_response(jsonify(resp), status)
        else:
            return make_response(jsonify(resp), status)

class GetFile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Authorization', location='headers', required=True)
    parser.add_argument('file_id', help='This field cannot be blank', required=True)
    def post(self):
        status = 200
        data = GetFile.parser.parse_args()
        st, user_id = jwt_verification(data)
        if st != 200 :
            return make_response(jsonify(user_id), st)
        f_master = FileMaster()
        data['user_id'] = user_id
        resp = f_master.get_file(data=data)
        if type(resp) is int:
            status = 500
            resp = {'message': 'Failed', 'result': []}
            return resp
        else:
            return resp

class DeleteFile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Authorization', location='headers', required=True)
    parser.add_argument('file_id', help='This field cannot be blank', required=True)
    def post(self):
        status = 200
        data = DeleteFile.parser.parse_args()
        st, user_id = jwt_verification(data)
        if st != 200 :
            return make_response(jsonify(user_id), st)
        f_master = FileMaster()
        data['user_id'] = user_id
        resp = f_master.delete_file(data=data)
        if type(resp) is int:
            status = 500
            resp = {'message': 'Failed', 'result': []}
            return resp
        else:
            return resp

class GetFiles(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Authorization', location='headers', required=True)
    parser.add_argument('folder', help='This field cannot be blank', required=True)

    def post(self):
        status = 200
        data = GetFiles.parser.parse_args()
        st, user_id = jwt_verification(data)
        if st != 200 :
            return make_response(jsonify(user_id), st)
        f_master = FileMaster()
        data['user_id'] = user_id
        resp = f_master.get_files(data=data)
        if type(resp) is int:
            status = 500
            resp = {'message': 'Failed', 'result': []}
            return make_response(jsonify(resp), status)
        else:
            return make_response(jsonify(resp), status)

class CreateFolder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Authorization', location='headers', required=True)
    parser.add_argument('name', help='This field cannot be blank', required=True)
    
    def post(self):
        status = 200
        data = CreateFolder.parser.parse_args()
        st, user_id = jwt_verification(data)
        if st != 200 :
            return make_response(jsonify(user_id), st)
        f_master = FileMaster()
        data['user_id'] = user_id
        resp = f_master.create_folder(data=data)
        if type(resp) is int:
            status = 500
            resp = {'message': 'Failed', 'result': []}
            return make_response(jsonify(resp), status)
        else:
            return make_response(jsonify(resp), status)


class GetFolder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Authorization', location='headers', required=True)

    def get(self):
        status = 200
        data = GetFolder.parser.parse_args()
        st, user_id = jwt_verification(data)
        if st != 200 :
            return make_response(jsonify(user_id), st)
        f_master = FileMaster()
        data['user_id'] = user_id
        resp = f_master.get_folder(data=data)
        if type(resp) is int:
            status = 500
            resp = {'message': 'Failed', 'result': []}
            return make_response(jsonify(resp), status)
        else:
            return make_response(jsonify(resp), status)
