import traceback
import jwt
import os
import sqlite3

from datetime import datetime, timedelta
import pandas as pd
from flask_jwt_extended import (create_access_token, create_refresh_token)


class User :

    def __init__(self, **kwargs):
        self.connect = sqlite3.connect('database.db')
    
    def get_user_by_creds(self, data):
        result = {}
        try :
            query = f'''select * from user where email = '{data.get("email")}' '''
            df = pd.read_sql(query, self.connect)
            if len(df)>0:
                print(df.head())
                if df['password'][0] == data.get("password"):
                    del df['password']
                    token = jwt.encode({
                    'identity': int(df['id'][0]),
                    'exp' : datetime.utcnow() + timedelta(minutes = 30)
                }, os.environ.get('SECRET_KEY'))
                    print(token)
                    expires = timedelta(days=1)
                    df['access_token'] = token
                    return df.to_dict("records")[0]
                else :
                    return {"message" : "incorrect password"}
            else :
                return {"message": "user dosent exist"}
        except Exception as e :
            print(e)
            traceback.print_exc()
            return 500
        
    def add_user(self, data):
        result = {}
        try :

            query = f'''INSERT INTO user (name, email, password,level)
                        VALUES ('{data.get('name')}', '{data.get("email")}', '{data.get("password")}', '{data.get("level")}')'''
            print(query)
            connect = sqlite3.connect('database.db')

            connect.execute(query)
            connect.commit()
            return {"message":"user added"}
        except Exception as e :
            print(e)
            traceback.print_exc()
            return 500
    
# connect = sqlite3.connect('database.db')
# connect.execute(
#     'CREATE TABLE IF NOT EXISTS User (name TEXT, \
#     email TEXT, password TEXT, level TEXT)')

# connect.execute( "INSERT INTO user (name, email, password,level) VALUES ('mynane', 'mail@gmail.com', 'mypass', '1')")
