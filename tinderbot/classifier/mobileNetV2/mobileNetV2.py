import os
import numpy as np
import tensorflow as tf
from PIL import Image

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tinderbot.classifier.classifier import Classifier

class MobileNetV2(Classifier):
    """
    Class implementing tinderbot.Classifier with Google MobileNetV2
    pre-trained network
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes trained model from the model
        directory

        :param args:    Default superclass parameter
        :param kwargs:  Default superclass parameter
        """
        super().__init__(*args, **kwargs)

        # Get model path
        dir_current = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(dir_current, 'model')

        # Load model parameters from ./model/ directory
        self.model = tf.keras.models.load_model(model_path)

    def _classify(self, img_array):
        """
        Classifies face of input img_array as hot/ugly

        :param img_array:   numpy array containing pixel values
        :return:            prediction class (hot/ugly) 1/-1
        """
        resized_img = self.reshape_image_array(img_array)
        img_batch = np.expand_dims(resized_img, axis=0)
        img_preprocessed = preprocess_input(img_batch)
        prediction = self.model.predict(img_preprocessed)
        return prediction
    
    def reshape_image_array(self, image_array, new_shape=160):
        """
        Converts input image array to the network-specific size

        :param image_array:     numpy array
        :param new_shape:       size of resized square image
                                (default 160)
        :return:                numpy resized array
        """
        return np.array(Image.fromarray(image_array).resize(size=(new_shape, new_shape)))
        


