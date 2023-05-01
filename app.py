# using flask_restful
import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

  
# creating the flask app
app = Flask(__name__)
jwtmanager = JWTManager(app)

def register_extensions(app):
    jwtmanager.init_app(app)

# creating an API object
api = Api(app)
app.secret_key = 'av@124'
os.environ['SECRET_KEY'] = 'av@124'


app.config['CORS_ENABLED'] = True

if app.config['CORS_ENABLED'] is True:
    CORS(app, origins=["*"], allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"], supports_credentials=True)
  
# class UploadFile(Resource):

#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('Authorization', location='headers', required=True)
#         parser.add_argument('file', location='files', type=FileStorage, required=True)
#         parser.add_argument('folder', location='form', help='This field cannot be blank', required=True)
#         print(parser.parse_args())

        # Do something with the file, such as save it to diskx`x`

# api.add_resource(UploadFile, '/upload')
  
  
# another resource to calculate the square of a number

  
from ui.user import *
from ui.files import *
# adding the defined resources along with their corresponding urls
api.add_resource(Login, '/login')
api.add_resource(CreateUser, '/createuser')
api.add_resource(UploadFile, '/uploadfile')
api.add_resource(GetFile, '/getfile')
api.add_resource(DeleteFile, '/deletefile')
api.add_resource(GetFiles, '/getfiles')
api.add_resource(CreateFolder, '/createfolder')
api.add_resource(GetFolder, '/getfolder')

  
# driver function
if __name__ == '__main__':
    app.run(debug = True)
