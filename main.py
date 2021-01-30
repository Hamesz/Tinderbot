# this deals with classifying a person
import os, sys, time
import itertools
from datetime import datetime
from Database.update import add_user, check_user_exists, get_user_pic_path
# sys.modules.keys()
import requests
from Libs.TinderAPI.tinder_api import session
from Libs.FaceRecognition.recognition import find_owner
from config import pic_dir
sess = session.Session() # inits the session
import logging
import Logger
import matplotlib.pyplot as plt

logger = logging.getLogger("Logger")

def main():
    classify_users()

def classify_users():
    for user in itertools.islice(sess.yield_users(), 100):
        print(user.__get_info__())
        if(check_user_exists(user.id) == False):
            # store user details into database
            stored = store_details(user)
            print("Stored: {}".format(stored))
            # get face
            pic_path = get_user_pic_path(user.id)
            pictures = os.listdir(pic_path)
            pictures = [os.path.join(pic_path,picture) for picture in pictures]
            face, picture = find_owner(pictures)
            print("face:\n{}".format(face))
            imageplot = plt.imshow(face)
            plt.show()
            # get bio analysis
            
            # classify person
            
        else:
            pass
        input()

# deal with storing
def store_details(user):
    print("adding user")
    # create picture directory
    pic_dir = os.path.join('Database','Pictures',"{}_{}".format(user.id,user.name))
    os.mkdir(pic_dir)
    # update database
    success = add_user(uid=user.id,name=user.name,age=user.age,bio=user.bio,classification=1,pictures_path_relative=pic_dir.replace("\\","/"))
    if (success):
        # download and store pictures
        download_photos(user, pic_dir)
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