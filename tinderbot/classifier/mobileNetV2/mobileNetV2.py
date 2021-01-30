import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tinderbot.classifier.classifier import Classifier

from PIL import Image
import numpy as np

class MobileNetV2(Classifier):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get model path
        dir_current = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(dir_current, 'model')

        # Load model parameters from ./model/ directory
        self.model = tf.keras.models.load_model(model_path)

    #! TODO: Preprocess imgs pixels from [-1,1]
    def _classify(self, img_array):
        resized_img = self.reshape_image_array(img_array)
        img_batch = np.expand_dims(preprocessed_img, axis=0)
        img_preprocessed = preprocess_input(img_batch)
        prediction = self.model.predict(img_preprocessed)
        return prediction
    
    def reshape_image_array(self, image_array, new_shape=160):
        return np.array(Image.fromarray(image_array).resize(size=(160, 160)))
        


