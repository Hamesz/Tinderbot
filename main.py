# this deals with classifying a person
import os, sys, time
import itertools
from datetime import datetime
import requests

from tinderbot.database.commands import add_user, check_user_exists, get_user_pic_path
from tinderbot.TinderAPI.tinder_api import session
from tinderbot.FaceRecognition.recognition import find_owner
from tinderbot.config import TINDER_PICTURE_DIRECTORY

sess = session.Session() # inits the session
import logging
import matplotlib.pyplot as plt

logger = logging.getLogger("tinderbot.Logger")
logger.setLevel(logging.DEBUG)

def main():
    classify_users()

def classify_users():
    for user in itertools.islice(sess.yield_users(), 100):
        logger.debug("Checking user {} ({})".format(user.name, user.id))
        if(check_user_exists(user.id) == False):
            # store user details into database
            stored = store_details(user)
            if (stored):
                logger.info("Stored user: {} ({})".format(user.name, user.id))
                
                # get face
                pic_path = get_user_pic_path(user.id)
                pictures = os.listdir(pic_path)
                pictures = [os.path.join(pic_path,picture) for picture in pictures]
                face, picture = find_owner(pictures)

                logger.debug("face:\n{}".format(face))
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

# deal with storing
def store_details(user):
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

if __name__ == "__main__":
    main()