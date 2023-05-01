import sqlite3

def db_setup():
    connect = sqlite3.connect('database.db')
    connect.execute(
        'CREATE TABLE IF NOT EXISTS user (id integer PRIMARY KEY, name TEXT, \
        email TEXT, password TEXT, level TEXT)')
    connect.commit()
    connect.execute(
        'CREATE TABLE IF NOT EXISTS folder (name TEXT, \
        created_by int , id integer  PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    connect.commit()
    connect.execute(
        'CREATE TABLE IF NOT EXISTS filetable (filename TEXT, \
        created_by int , folder text, path text, size int,  id integer PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    connect.commit()