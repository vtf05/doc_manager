import os
import uuid
import traceback
import sqlite3
import datetime
import pandas as pd

from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask import send_from_directory, make_response,jsonify

UPLOAD_DIRECTORY = "api_upload_files"

class FileMaster :

    def __init__(self, **kwargs):
        self.connect = sqlite3.connect('database.db')
    
    def get_folder(self, data):
        try :
            query = f'''select level from user where id = {data.get("user_id")}'''
            df = pd.read_sql(query, self.connect)
            if int(df['level'][0]) == 1 :
                query = f'''select name,id,created_at from folder'''
            else :
                query = f'''select name,id,created_at from folder where created_by = {data.get("user_id")}'''
            file_df = pd.read_sql(query, self.connect)
            result = file_df.to_dict('records')
            return result
        except Exception as e :
            print(e)
            traceback.print_exc()
            return 500
    
    def create_folder(self,data):   
        result = {}
        try :
            query = f'''select name from folder where created_by = {data.get("user_id")} and name = '{data.get("name")}' '''
            df = pd.read_sql(query, self.connect)
            if len(df) > 0 :
                return {"message":"folder exist"}
            else :
                query = f'''insert into folder (name, created_by) values( '{data.get("name")}', {data.get("user_id")})'''
                self.connect.execute(query)
                self.connect.commit()
                return {"message":"folder created"}
        except Exception as e :
            print(e)
            traceback.print_exc()
            return 500

    
    def get_files(self,data):
        try :
            query = f'''select level from user where id = {data.get("user_id")}'''
            df = pd.read_sql(query, self.connect)
            print(df.head())
            if int(df['level'][0]) == 1 :
                get_file_query = f'''select * from filetable inner join ( select id as user_id , name from user) as u on u.user_id = filetable.created_by where folder = '{data.get('folder')}' '''
            else :
                get_file_query = f'''select * from filetable inner join ( select id as user_id , name from user) as u on u.user_id = filetable.created_by where folder = '{data.get('folder')}' and created_by = {data.get('id')} '''
            print(get_file_query)
            connect = sqlite3.connect('database.db')
            file_df = pd.read_sql(get_file_query, connect)
            print(file_df)
            result = file_df.to_dict('records')
            return result
        except Exception as e :
            print(e)
            traceback.print_exc()
            return 500

    def get_file(self,data):
        try :
            query = f'''select * from filetable where id = {data.get("file_id")} '''
            df = pd.read_sql(query, self.connect)
            if len(df)>0 :
                base_path =  UPLOAD_DIRECTORY+'/'+ df['path'][0]
                return send_from_directory(base_path,df['filename'][0] , as_attachment=True)
            else :
                return make_response(jsonify({'message' :'file not found'}), 200)

        except Exception as e :
            print(e)
            traceback.print_exc()
            return 500
        
    def delete_file(self,data):
        try :
            query = f'''select * from filetable where id = {data.get("file_id")} '''
            print(query)
            df = pd.read_sql(query, self.connect)
            if len(df)>0 :
                base_path =  UPLOAD_DIRECTORY+'/'+ df['path'][0]
                os.remove(os.path.join(base_path,df['filename'][0]))
                delete_query = f'''delete from filetable where id = {data.get("file_id")} '''
                print(delete_query)
                self.connect.execute(delete_query)
                self.connect.commit()
                return make_response(jsonify({'message' :'file deleted '}), 200)
            else :
                return make_response(jsonify({'message' :'file not found'}), 200)
        except Exception as e :
            print(e)
            traceback.print_exc()
            return 500

    def addfile(self, data):
        result = {}
        try :
            file_name = data.get('file').filename
            file  = data.get("file")
            e_id = uuid.uuid4()
            file_path = f'''{data.get("folder")}/{str(data.get("user_id"))}/{str(e_id)}'''
            path = os.path.join(UPLOAD_DIRECTORY, data.get("folder"))
            os.makedirs(path, exist_ok = True)
            path = os.path.join(path, str(data.get("user_id")))
            os.makedirs(path, exist_ok = True)
            path = os.path.join(path, str(e_id))
            os.makedirs(path, exist_ok = True)
            file.save(os.path.join(path, file_name))
            file_size = os.path.getsize(os.path.join(path, file_name))/1024
            query = f'''insert into filetable (folder, filename, path,size, created_by) values('{data.get("folder")}', '{file_name}', '{file_path}', {file_size}, {data.get("user_id")})'''
            connect = sqlite3.connect('database.db')
            connect.execute(query)
            connect.commit()
            return {"message":"file uploaded"}
        except Exception as e :
            print(e)
            traceback.print_exc()
            return 500

# connect = sqlite3.connect('database.db')
# connect.execute(
#     'CREATE TABLE IF NOT EXISTS user (id integer PRIMARY KEY, name TEXT, \
#     email TEXT, password TEXT, level TEXT)')

# connect.execute(
#     'CREATE TABLE IF NOT EXISTS folder (name TEXT, \
#     created_by int , id integer  PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

# connect.execute(
#     'CREATE TABLE IF NOT EXISTS filetable (filename TEXT, \
#     created_by int , folder text, path text, size int,  id integer PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')


# query = "PRAGMA table_info(filetable); "
# df = pd.read_sql(query, connect)

# connect.execute("drop table filetable")