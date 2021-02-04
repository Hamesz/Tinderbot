import itertools
import os
import time
import requests
from tinderbot.database.commands import add_user, check_user_exists, get_user_pic_path
from tinderbot.TinderAPI.tinder_api import session
from tinderbot.FaceRecognition.recognition import find_owner
from tinderbot.config import TINDER_PICTURE_DIRECTORY
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger("tinderbot.Logger")

def classify_users(no_users):
    """Classifies a number of users

        Args:
            no_users (int): The number of users to classify

        Returns:
            None
    """
    sess = session.Session() # inits the session
    for user in itertools.islice(sess.yield_users(), no_users):
        logger.debug("Checking user {} ({})".format(user.name, user.id))
        if(check_user_exists(user.id) == False):
            # store user details into database
            stored = store_details(user)
            if (stored):
                logger.info("Stored user: {} ({})".format(user.name, user.id))
                # get face
                face, picture = get_face_picture(user.id)
                imageplot = plt.imshow(face)
                plt.show()
                # get bio analysis

                # classify person
                
            else:
                logger.warning("Storing user failed: {} ({})".format(user.name, user.id))
        else:
            logger.debug("User already stored")
            pass
        input()

def get_face_picture(id):
    """Gets the users face from a given picture

        Args:
            id (string): User unique id

        Returns:
            face (array): image of face as an array
            picture_path (string): path to the picture the face is from
    """
    pic_path = get_user_pic_path(id)
    pictures = os.listdir(pic_path)
    pictures = [os.path.join(pic_path,picture) for picture in pictures]
    face, picture_path = find_owner(pictures)
    return face, picture_path

def store_details(user):
    """Stored the users details into the database

        Args:
            user (User): The user
        
        Returns:
            success (bool): True if successfully stored
    """
    logger.debug("adding user")
    # create picture directory
    picture_directory = os.path.join(TINDER_PICTURE_DIRECTORY,"{}_{}".format(user.id,user.name))
    os.mkdir(picture_directory)
    # update database
    success = add_user(uid=user.id,name=user.name,age=user.age,bio=user.bio,classification=1,pictures_path_relative=picture_directory) #.replace("\\","/")
    if (success):
        # download and store pictures
        download_photos(user, picture_directory)
        return True
    else:
        return False

def download_photos(user, pic_dir):
    """Downloads the users photos from tinder

        Args:
            user (User): The user
            pic_dir (string): the directory to store the pictures
        
        Returns:
            None
    """
    for x in range(len(user.photos)):
        pic_filename = "{}_{}.jpg".format(user.id,x)
        pic_full_path = os.path.join(pic_dir,pic_filename)
        with open(pic_full_path, 'wb') as handle:
            response = requests.get(user.photos[x], stream=True)
            if not response.ok:
                logger.error(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
    time.sleep(0.1)