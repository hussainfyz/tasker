import sqlite3
def get_db_file():
    dbpath='C:\\Users\\Admin\\PycharmProjects\\tasker\\tasker.db'
    return dbpath
def connect_db():
    return sqlite3.connect(get_db_file())
