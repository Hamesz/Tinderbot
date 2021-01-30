from tinderbot.database.database_connector import connect
from datetime import datetime
import mysql.connector
import logging
import tinderbot.Logger
import string
import os
import sys


# dir_current = (os.path.dirname(os.path.realpath(__file__)))
# dir_root    = os.path.join(dir_current,"..")
# sys.path.append(dir_root)

logger = logging.getLogger("Logger")

def add_user(uid,name,age,bio,classification,pictures_path_relative):
    """ Add a user to the sql database

        Args:
            uid (string): unique identifier for each user
            name (string): name of the user
            age (int): age of the user
            bio (string): bio of the user
            classification (int): classification of the user (1 = attractive)
            pictures_path_relative (string): relatve picture path for the user

        Returns
            success (bool): true if successfully added
    """
    # query sql database to update it
    connection = connect()
    mycursor = connection.cursor()
    # remove non-ascii
    printable = set(string.printable)
    bio=str("".join(filter(lambda x: x in printable, bio)))

    # add new user to database
    add_query = "INSERT INTO user (create_time, uid, name, age, classification, bio, pictures) VALUES ('{}', '{}', '{}', '{}', '{}','{}','{}');".format(datetime.now(),uid, name, age, classification, bio, pictures_path_relative)
    insert = "insert into {} (create_time, uid, name, age, classification, bio, pictures) values (%s, %s, %s, %s, %s, %s, %s)".format("user")
   
    logger.debug("Add Query: {}".format(add_query))
    # exectue the queries
    added = False
    try:
        mycursor.execute(insert, (datetime.now(),uid, name, age, classification, bio, pictures_path_relative))  # prevents from SQL injection too
        connection.commit()
        logger.info("{} record(s) affected".format(mycursor.rowcount))  
        added = True
    except Exception as e:
        logger.error(e)
        added = False

    mycursor.close()
    connection.close()
    return added

def check_user_exists(uid):
    """ Checks if the user already exists in the database

        Args:
            uid (string): unique identifier for each user

        Returns:
            within (bool): True if the user is in the database else false
    """
    connection = connect()
    mycursor = connection.cursor()

    select_query = "SELECT uid FROM user WHERE uid='{}'".format(uid)
    
    mycursor.execute(select_query)
    result = mycursor.fetchone() # only expecting 1 row
    logger.debug("User is in database? : {}".format(result))
    
    return (mycursor.rowcount > 0)

def get_user_pic_path(uid):
    """ Get the users picture directory

        Args: 
            uid (string): id of user

        Returns:
            picture path (string): path to the pictures of the user 
    """
    connection = connect()
    mycursor = connection.cursor()

    select_query = "SELECT pictures FROM user WHERE uid='{}'".format(uid)
    
    mycursor.execute(select_query)
    result = mycursor.fetchone() # only expecting 1 row
    logger.debug("Picture path: {}".format(result[0]))
    
    return result[0]

def add_user_test():
    return

def check_user_test():
    uid = "53f48a595ce652fc05a60456"
    exists = check_user_exists(uid)
    assert(exists == True)

def get_user_pic_path_test():
    uid = "53f48a595ce652fc05a60456"
    pic_path = get_user_pic_path(uid)
    print(pic_path)
    assert("Database/Pictures/53f48a595ce652fc05a60456_Thayná" == pic_path)

def main():
    add_user_test()
    check_user_test()
    get_user_pic_path_test()

if __name__ == "__main__":
    main()