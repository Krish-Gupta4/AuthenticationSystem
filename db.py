import sqlite3
import os

defaultPath = "./db.sqlite3"

def db_init():
    connection = sqlite3.connect(defaultPath)
    crsr = connection.cursor() 
    sql_command = """CREATE TABLE articles (userID,id,title,body);"""
    crsr.execute(sql_command) 
    connection.commit()
    connection.close()

def save_details(details, table = "articles"):
    connection = sqlite3.connect(defaultPath)
    crsr = connection.cursor()
    val = "("
    for _ in details:
        val+=("?,")
    val = val[:len(val)-1]
    val+=");"
    sql_command = "INSERT INTO "+ table +" VALUES " + val
    crsr.execute(sql_command, tuple(details)) 
    connection.commit() 
    connection.close()

def show_table():
    connection = sqlite3.connect(defaultPath)
    crsr = connection.cursor()
    cmd = "SELECT * FROM articles"
    crsr.execute(cmd)
    ans = crsr.fetchall()
    for i in range(len(ans)):
        ans[i] = list(ans[i])
    connection.close()
    return ans

# db_init()
# show_table()