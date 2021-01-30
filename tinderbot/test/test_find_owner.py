import unittest
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt 
from tinderbot.FaceRecognition.recognition import find_owner

class TestFindOwner(unittest.TestCase):
    

    def test_single_face(self):
        test_pictures_path = Path('data','pictures','test')
        picture_names = os.listdir(test_pictures_path)
        pictures_paths = [os.path.join(test_pictures_path,picture_name) for picture_name in picture_names]
        face, picture = find_owner(pictures_paths)
        imageplot = plt.imshow(face)
        plt.show()
        
# if __name__ == '__main__':
#     unittest.main()