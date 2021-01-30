# this file is used to query the sql database
import os
import sys
dir_current = (os.path.dirname(os.path.realpath(__file__)))
dir_root    = os.path.join(dir_current,"..")
sys.path.append(dir_root)

import mysql.connector
from config import host,user,passwd,database

CONNECTION = None

# connect to the sql database
def connect():
    mydb = mysql.connector.connect(
    host=host,
    user=user,
    passwd=passwd,
    database=database
    )
    CONNECTION = mydb
    return mydb