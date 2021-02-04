import itertools
import os
import time
import requests
from tinderbot.database.commands import add_user, check_user_exists, get_user_pic_path
from tinderbot.TinderAPI.tinder_api import session
from tinderbot.FaceRecognition.recognition import find_owner
from tinderbot.config import TINDER_PICTURE_DIRECTORY
import matplotlib.pyplot as plt
from tinderbot.classifier.mobileNetV2.mobileNetV2 import MobileNetV2
import logging
logger = logging.getLogger("tinderbot.Logger")

def classify_users(no_users):
    """Classifies a number of users

        Args:
            no_users (int): The number of users to classify

        Returns:
            None
    """
    # initalise tinder session
    sess = session.Session()
    # initialise classifier 
    classifier = MobileNetV2()
    for user in itertools.islice(sess.yield_users(), no_users):
        logger.debug("="*20)
        logger.debug("Checking user: {} ({})".format(user.name, user.id))
        if(check_user_exists(user.id) == False):\
            # get face
            face, picture = get_face_picture(user)
            # get classification
            classification = classifier.classify(face)[0,0]
            logger.info(f"Classification: {classification}")
            # store user details into database
            stored = store_details(user, classification=classification)
            if (stored):
                logger.info("Stored user: {} ({})".format(user.name, user.id))
                imageplot = plt.imshow(face)
                plt.show()               
            else:
                logger.warning("Storing user failed: {} ({})".format(user.name, user.id))
        else:
            logger.debug("User already stored")
            pass
        # input()

def get_face_picture(user):
    """Gets the users face from a given picture

        Args:
            id (string): User unique id

        Returns:
            face (array): image of face as an array
            picture_path (string): path to the picture the face is from
    """
    # get the picture directory
    picture_directory = os.path.join(TINDER_PICTURE_DIRECTORY,"{}_{}".format(user.id,user.name))
    # check if directory exists
    if(not os.path.isdir(picture_directory)):
        os.mkdir(picture_directory)
    # download the photos
    download_photos(user, picture_directory)
    # now get the owners face
    pictures = os.listdir(picture_directory)
    pictures = [os.path.join(picture_directory,picture) for picture in pictures]
    face, picture_path = find_owner(pictures)
    return face, picture_path

def store_details(user, classification=0):
    """Stored the users details into the database

        Args:
            user (User): The user
        
        Returns:
            success (bool): True if successfully stored
    """
    logger.debug("adding user")
    # create picture directory
    picture_directory = os.path.join(TINDER_PICTURE_DIRECTORY,"{}_{}".format(user.id,user.name))
    if(not os.path.isdir(picture_directory)):
        os.mkdir(picture_directory)
    # process classification 
    classification = str("{:.5f}".format(classification))
    # update database
    success = add_user(uid=user.id,name=user.name,age=user.age,bio=user.bio,classification=classification,pictures_path_relative=picture_directory) #.replace("\\","/")
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