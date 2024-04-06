import tensorflow as tf
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from markupsafe import Markup

class TumorSense:
    def __init__(self):
        current_directory = os.path.dirname(__file__)
        model_path = os.path.join(current_directory, 'model.h5')
        self.model = tf.keras.models.load_model(model_path)
        
    def predict(self, data):
        tumor_types = {
            'glioma': Markup(
                'Glioma://Definition: Gliomas are the most common type of primary brain tumor, arising from glial cells, which are supportive cells in the brain and spinal cord. They can occur at any age but are most frequent in adults.//Types: There are several subtypes of gliomas, categorized by their aggressiveness and cell type of origin. The most common classifications are://- Low-Grade Glioma (LGG): These are slow-growing tumors with a relatively good prognosis. Examples include pilocytic astrocytoma and oligodendroglioma.//- High-Grade Glioma (HGG): These are fast-growing and aggressive tumors with a poorer prognosis. Examples include glioblastoma multiforme (GBM), the most common and aggressive type of brain tumor.//Symptoms: Symptoms can vary depending on the location and size of the tumor. They may include headaches, seizures, weakness, cognitive decline, and speech problems.//Treatment: Treatment typically involves surgery, radiation therapy, and or chemotherapy. The specific approach depends on the type and grade of the glioma.//'),
            'meningioma': Markup(
                'Meningioma://Definition: Meningiomas are benign (non-cancerous) tumors that arise from the meninges, the protective membranes surrounding the brain and spinal cord. They are the second most common type of primary brain tumor after gliomas.//Symptoms: Symptoms can vary depending on the location and size of the tumor. They may include headaches, seizures, vision problems, hearing loss, and weakness.//Treatment: Treatment options include observation (for slow-growing tumors), surgery, and radiation therapy. The specific approach depends on the size, location, and growth rate of the meningioma.//Note: While most meningiomas are benign, a small percentage can be atypical or malignant (cancerous). These require more aggressive treatment.//'),
            'normal': Markup(
                'Normal://Definition: In the context of brain imaging and tumor detection, normal refers to the absence of any abnormalities or tumors. A normal result indicates that no suspicious masses or lesions were found on the scan.//'),
            'adenoma': Markup(
                'Adenoma://Definition: Adenomas are benign tumors that arise from glandular tissue. While they can occur in various organs, they are not typically found in the brain.//Importance in Brain Tumor Detection: In the context of brain imaging, adenoma is unlikely. It\'s more probable that normal was intended or there\'s a typo. It\'s crucial to confirm the actual result with the radiologist or physician.//')
        }

        index = ['glioma','meningioma','normal','adenoma']
        
        data = load_img(data,target_size = (224,224))
        data = img_to_array(data)
        data = np.expand_dims(data,axis=0)
        
        # result = self.model.predict(data)
        
        result = np.argmax(self.model.predict(data//255.0),axis=1)
        result = index[result[0]]

        report_text = tumor_types[result]
        
        return result, report_text
