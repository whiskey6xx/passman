#!/usr/bin/python

import sqlite3
from pmcryptman import *


def db_table_check():
    conn = sqlite3.connect('passman.db')
#create the table with the columns labeled ID, SITE, USER, PASS
    try:
        conn.execute('''CREATE TABLE VAULT
                (ID INT PRIMARY KEY     NOT NULL,
                SITE            TEXT     NOT NULL,
                USER            TEXT     NOT NULL,
                PASS            TEXT     NOT NULL); ''')
        print("Table1 created")
    except:
        print("table1 exist")

    try:
        conn.execute('''CREATE TABLE KS
                (ID INT PRIMARY KEY     NOT NULL,
                KEY            TEXT     NOT NULL,
                SALT           TEXT     NOT NULL); ''')
        print("Table2 created")
    except:
        print("table2 exist")

    conn.close()

    

#retrieve key salt pair
def db_get_ks():
    conn = sqlite3.connect('passman.db')
    cursor = conn.execute("SELECT key, salt FROM KS WHERE id = 1")
    row = cursor.fetchone()
    if row is not None:
        conn.close()
        return row[0], row[1]
    else:
        conn.close()
        return None
    

def db_insert(i, site, user, passw):
#inserting into a table
    try:
        conn = sqlite3.connect('passman.db')
        cursor = conn.cursor()
        sql = "INSERT INTO VAULT (ID, SITE, USER, PASS) VALUES (?, ?, ?, ?)"
        k = db_get_ks()
        passw = encrypt(passw, k[0])
        values = (i, site, user, passw)
        cursor.execute(sql, values)

        conn.commit()
        print("inserted data" + str(passw))
        conn.close()
    except:
        print("ID EXISTS!")
#change to accept input (Complete)




def db_insert_ks(password):
#inserting into a table
    try:
        salt = make_salt()
        ks = create_key(password, salt)
        k = ks
        s = salt
        conn = sqlite3.connect('passman.db')
        cursor = conn.cursor()
        sql = "INSERT INTO KS (ID, KEY, SALT) VALUES (?, ?, ?)"
        values = (1, k, s)
        cursor.execute(sql, values)
        conn.commit()
        print("inserted data")
        conn.close()
    except:
        print("SOMETHING WENT WRONG, TRY AGAIN")

#retrieve the rows
def db_showall():
    conn = sqlite3.connect('passman.db')
    cursor = conn.execute("SELECT id, site, user, pass from VAULT")
    for row in cursor:
        print("ID = ", row[0])
        print("SITE = ", row[1] , "\n")
    conn.close()

#create function to only retrieve the credentials from the selected id
def db_show_password(selected_id):
    conn = sqlite3.connect('passman.db')
    cursor = conn.execute("SELECT pass FROM VAULT WHERE id = ?", (selected_id,))
    row = cursor.fetchone()
    if row is not None:
        k = db_get_ks()
        pw = decrypt(row[0], k[0])
        conn.close()
        
        return pw
        
    else:
        conn.close()
        return None

#updating the passwords
def db_update(i, passw):
    conn = sqlite3.connect('passman.db')
    cursor = conn.cursor()
    sql = "UPDATE VAULT SET PASS = ? WHERE ID = ?"
    k = db_get_ks()
    passw = encrypt(passw, k[0])
    values = (passw, i)
    cursor.execute(sql, values)

    conn.commit()
    print("password changed")
    conn.close()


#deleting an entry
def db_delete(selected_id):
    conn = sqlite3.connect('passman.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM VAULT WHERE id = ?", (selected_id,))
    if cursor.rowcount == 1:
        print(f"Deleted row with ID {selected_id}")
    else:
        print(f"No row found with ID {selected_id}")
    conn.commit()
    conn.close()





