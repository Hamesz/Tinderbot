import face_recognition
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os,sys
import logging
import tinderbot.Logger
import ast

logger = logging.getLogger("Logger")

# returns the array for where faces are found in the picture
def get_faces(picture):
    """ Gets the faces within a picture

        Args:
            picture (string): location of a file

        Returns:
            faces (list): list of array which cointains the face[top:bottom, left:right]]
    """
    image = face_recognition.load_image_file(picture)
    face_locations = face_recognition.face_locations(image)
    logger.debug("I found {} face(s) in this photograph.".format(len(face_locations)))

    faces = []

    for face_location in face_locations:

        # Print the location of each face in this image
        old_top, old_right, old_bottom, old_left = face_location
        logger.debug("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(old_top, old_left, old_bottom, old_right))

        # increase image size
        bias = int((old_bottom - old_top)*0.5)
        new_top = old_top - bias if old_top - bias > 0 else 0
        new_bottom = old_bottom + bias if old_bottom + bias < image.shape[0] else image.shape[0] - 1
        new_left = old_left - bias if old_left - bias > 0 else 0
        new_right = old_right + bias if old_right + bias < image.shape[1] else image.shape[1] - 1
        # You can access the actual face itself like this:
        face_image = image[new_top:new_bottom, new_left:new_right]
        faces.append(face_image)
    return faces

# show the faces and press enter to look at next face
def show_face(face):
    pil_image = Image.fromarray(face)
    pil_image.show()
    input()

# train to recognize a face
def get_face_encodings(pic):
    image = face_recognition.load_image_file(pic)
    face_encodings = face_recognition.face_encodings(image)
    return face_encodings

def compare_faces(known_face_encoding,unkown_face_encoding):    
    # unknown_encoding = face_recognition.face_encodings(unkown_face)[0]
    results = face_recognition.compare_faces([known_face_encoding], unkown_face_encoding)
    return results

# pictures is [path to image]
def find_owner(pictures):
    """ Gets the profile owner's face

        Args:
            pictures (list): list of paths to pictures

        Returns:
            face location + picture path (array, string): location of the owners face for the given picture 
    """
    faces_dictionary = dict()
    logger.debug("Finding Owner")
    for pic in pictures:
        a = get_occurence_of_face(pic, faces_dictionary)
        found= a[0]
        faces_dictionary  = a[1]
        if (found):
            logger.debug("Found face!")
            key = list(faces_dictionary.keys())[0]
            face = faces_dictionary[key][1]
            picture_path = faces_dictionary[key][3]
            return face, picture_path
    # logger.debug_face_occurence(faces_dictionary)
    key = list(faces_dictionary.keys())[0]
    face = faces_dictionary[key][1]
    picture_path = faces_dictionary[key][3]
    return face, picture_path

def print_face_occurence(dict):
    for key,value in dict.items():
        (encoding,face,occurence) = value
        logger.debug("Occurence: {}".format(occurence))
        show_face(face)

def get_occurence_of_face(pic,faces_dictionary):
    """Updates the faces dictionary with the faces of the people in the picture by comparing the encodings,
        If the person is in the dictionary but not seen in the picture then the person is removed from the dictionary.

        Args:
            pic (string): path to picture
            faces_dictionary (dict): dictionary of {person:[encoding, face, occurance, picture path]}

        Returns:
            face detected (bool): True if only 1 face is detected
            faces_dictionary (dict): dictionary of {person:[encoding, face, occurance, picture path]}
    """
    logger.debug("picture: {}".format(pic))
    # get the loaction of all faces 
    faces = get_faces(pic)
    logger.debug(pic)
    # get the face encodings for all faces
    face_encodings = get_face_encodings(pic)

    # only 1 face found
    if (len(face_encodings) == 1):
        d = {
            0:[face_encodings[0],faces[0],1, pic]
        }
        logger.debug("Found picture with only 1 face")
        return (True, d)

    # no face found
    if (len(face_encodings) == 0):
        logger.debug("Found picture with 0 faces")
        return (False, faces_dictionary)
    
    # check if dict is empty
    if (not faces_dictionary):
        logger.debug("ïnitalising face dictionary")
        for i in range(len(face_encodings)):
            faces_dictionary[i] = [face_encodings[i],faces[i],1, pic]
    else:
        # get occurences of faces (face -> String(of list), Occurence -> Int)
        logger.info(type(faces_dictionary))
        for key, value in faces_dictionary.items():
            # key is person
            # value is face encoding, face position, num of times seen this face
            (encoding,face,occurence, stored_picture) = value
            same = False

            for x in range(len(face_encodings)) :
                unkown_face_encoding = face_encodings[x]
                plot_comapre_2(faces[x],face)
               
                same = compare_faces(encoding,unkown_face_encoding)
                print("="*20)
                logger.debug(str(same))
                print("="*20)
                if (same[0] == True):
                    logger.debug("Found same faces")
                    faces_dictionary[key] = (encoding,face,occurence + 1, stored_picture)
                    break
            # if same == alse then we did not find a saved face in this picture
            # thus remove it
            if (same == False):
                logger.debug("Fcae that was in dictionary is not seen in another picture. Removing!")
                del faces_dictionary[key]

        if (len(faces_dictionary) == 1):
            return True, faces_dictionary

    return False,faces_dictionary

def plot_comapre_2(imgLr,imgRr,blocking=True):
    logger.warning("Displaying face comparisons!")
    f = plt.figure()
    f.add_subplot(1,2,1)
    plt.imshow(imgLr)
    f.add_subplot(1,2,2)
    plt.imshow(imgRr)
    plt.show()


def test(pic1,pic2):
    # get known faces
    known_image = face_recognition.load_image_file(pic1)
    faces_locations = face_recognition.face_locations(known_image)

    faces_known_list = []
    for face_locations in faces_locations:
        top, right, bottom, left = face_locations
        face = known_image[top:bottom, left:right]
        faces_known_list.append(face)

    plot_comapre_2(faces_known_list[0],faces_known_list[1],True)
    
    # for unknown faces
    unknown_image = face_recognition.load_image_file(pic2)
    faces_locations = face_recognition.face_locations(unknown_image)

    faces_unknown_list = []
    for face_locations in faces_locations:
        top, right, bottom, left = face_locations
        face = unknown_image[top:bottom, left:right]
        faces_unknown_list.append(face)
    
    plot_comapre_2(faces_unknown_list[0],faces_unknown_list[1],True)

    # for face in faces_list:   
    #     show_face(face)
    
    faces_encodings_known   = get_face_encodings(pic1)
    faces_encodings_unknown = get_face_encodings(pic2)    

    plot_comapre_2(faces_known_list[0],faces_unknown_list[0])
    results_0 = compare_faces(faces_encodings_known[0],faces_encodings_unknown[0])
    # show_face(faces_known_list[0])
    # show_face(faces_unknown_list[0])
    print(results_0)
    plot_comapre_2(faces_known_list[0],faces_unknown_list[1])
    results_1 = compare_faces(faces_encodings_known[0],faces_encodings_unknown[1])
    # show_face(faces_known_list[0])
    # show_face(faces_unknown_list[1])
    print(results_1)

    exit()
    for i in range(len(faces_unknown_list)):
        for j in range(len(faces_known_list)):
            face_known_ecoding = get_face_encodings(faces_known_list[j])
            # comapre them
            plot_comapre_2(faces_known_list[j],faces_unknown_list[i])
            compare_faces()


    plot_comapre_2(faces_list[0],faces_list[1])

    exit()
    
    lizzie_encoding = face_recognition.face_encodings(known_image)[1]
    lizzie_friend_encoding = face_recognition.face_encodings(known_image)[0]

    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    unknown_2_encoding = face_recognition.face_encodings(unknown_image)[1]

    logger.debug("Lizzie encoding vs Unknown encoding: {}".format(face_recognition.compare_faces([lizzie_encoding], unknown_encoding)))
    logger.debug("Lizzie encoding vs Unknown 1 encoding: {}".format(face_recognition.compare_faces([lizzie_encoding], unknown_1_encoding)))


def main():
    dir_FaceRecognition = (os.path.dirname(os.path.realpath(__file__)))
    # dir_Libs            = os.path.join(dir_FaceRecognition,"..")
    # dir_root            = os.path.join(dir_Libs,"..")
    # dir_Database        = os.path.join(dir_root,"Database")   
    # dir_Pictures        = os.path.join(dir_Database,"Pictures")

    # logger.setLevel(logging.DEBUG)

    # dir_Eimera = os.path.join(dir_Pictures,os.listdir(dir_Pictures)[8])
    # dir_lizzie = "C:\\Users\\James H\\git\\TinderBot\\Database\\Pictures\\5e4c5d0a10ba09010017a892_Lizzie"
    # pics_Eimera = os.listdir(dir_lizzie)
    # for x in range(len(pics_Eimera)):
    #     full_path = os.path.join(dir_lizzie,pics_Eimera[x])
    #     pics_Eimera[x] = full_path

    # print(pics_Eimera)
    # face = find_owner(pics_Eimera)
    # # test(pics_Eimera[0],pics_Eimera[1])
    # show_face(face)
   

    return

if __name__ == "__main__":
    main()