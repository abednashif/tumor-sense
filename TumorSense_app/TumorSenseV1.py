import tensorflow as tf
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

class TumorSense:
    def __init__(self):
        current_directory = os.path.dirname(__file__)
        model_path = os.path.join(current_directory, 'model.h5')
        self.model = tf.keras.models.load_model(model_path)
        
    def predict(self, data):
        index = ['glioma','meningioma','normal','adenoma']
        
        data = load_img(data,target_size = (224,224))
        data = img_to_array(data)
        data = np.expand_dims(data,axis=0)
        
        # result = self.model.predict(data)
        
        result = np.argmax(self.model.predict(data/255.0),axis=1)
        result = index[result[0]]
        
        return result
