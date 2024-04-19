import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array, array_to_img
from tensorflow.keras.optimizers import Adam
from markupsafe import Markup


class BrainTumor:
    _MRI = 'MRI'

    def __init__(self):
        current_directory = os.path.dirname(__file__)
        # model_path = os.path.join(current_directory, 'model.h5')
        model_path = os.path.join(current_directory, 'models/fine_tuned_model.h5')
        mriDetect_path = os.path.join(current_directory, 'models/mri-img-detection.h5')
        self.model = load_model(model_path)
        self.model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

        self.detect_mri = load_model(mriDetect_path)
        self.detect_mri.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

    def predict(self, data):
        tumor_types = {
            'Glioma': Markup(
                'Gliomas are the most common type of primary brain tumor, arising from glial cells, which are supportive cells in the brain and spinal cord. They can occur at any age but are most frequent in adults.//Types: There are several subtypes of gliomas, categorized by their aggressiveness and cell type of origin. The most common classifications are://- Low-Grade Glioma (LGG): These are slow-growing tumors with a relatively good prognosis. Examples include pilocytic astrocytoma and oligodendroglioma.//- High-Grade Glioma (HGG): These are fast-growing and aggressive tumors with a poorer prognosis. Examples include glioblastoma multiforme (GBM), the most common and aggressive type of brain tumor.//Symptoms: Symptoms can vary depending on the location and size of the tumor. They may include headaches, seizures, weakness, cognitive decline, and speech problems.//Treatment: Treatment typically involves surgery, radiation therapy, and or chemotherapy. The specific approach depends on the type and grade of the glioma.//'),
            'Meningioma': Markup(
                'Meningiomas are benign (non-cancerous) tumors that arise from the meninges, the protective membranes surrounding the brain and spinal cord. They are the second most common type of primary brain tumor after gliomas.//Symptoms: Symptoms can vary depending on the location and size of the tumor. They may include headaches, seizures, vision problems, hearing loss, and weakness.//Treatment: Treatment options include observation (for slow-growing tumors), surgery, and radiation therapy. The specific approach depends on the size, location, and growth rate of the meningioma.//Note: While most meningiomas are benign, a small percentage can be atypical or malignant (cancerous). These require more aggressive treatment.//'),
            'Normal': Markup(
                'In the context of brain imaging and tumor detection, normal refers to the absence of any abnormalities or tumors. A normal result indicates that no suspicious masses or lesions were found on the scan.//'),
            'Adenoma': Markup(
                'Adenomas are benign tumors that arise from glandular tissue. While they can occur in various organs, they are not typically found in the brain.//Importance in Brain Tumor Detection: In the context of brain imaging, adenoma is unlikely. It\'s more probable that normal was intended or there\'s a typo. It\'s crucial to confirm the actual result with the radiologist or physician.//')
        }

        index = ['Glioma', 'Meningioma', 'Normal', 'Adenoma']

        image = load_img(data, target_size=(224, 224))

        img_arr = img_to_array(image)
        _data = np.expand_dims(img_arr, axis=0)

        result = np.argmax(self.model.predict(_data / 255.0), axis=1)

        result = index[result[0]]

        report_text = tumor_types[result]

        return result, report_text


    def checkIfMRI(self, _image_path):
        images_labels = ["Not a MRI image!", "MRI"]
        threshold = 0.5

        _image = load_img(_image_path, target_size=(224, 224))
        image = img_to_array(_image)
        image = np.expand_dims(image, axis=0)
        res = self.detect_mri.predict(image)

        return images_labels[0] if res >= threshold else images_labels[1]


class LungTumor:
    _CT = 'CT'
    def __init__(self):
        current_directory = os.path.dirname(__file__)
        model_path = os.path.join(current_directory, 'models/LungTumorModel.hdf5')
        # CTDetect_path = os.path.join(current_directory, 'models/ct-img-detection.h5')

        self.model = load_model(model_path)
        self.model.compile(optimizer='Adam', loss='categorical_crossentropy')

        # self.detect_CT = load_model(CTDetect_path)
        # self.detect_CT.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

    def predict(self, data):

        tumor_types = {
            'Adenocarcinoma: left > lower lobe T2_N0_M0_Ib': Markup(
                        'Adenocarcinoma is a type of cancer that develops in the glandular cells of epithelial tissue.//It can occur in various organs, including the lungs.//In this case, the tumor is located in the left lower lobe of the lung.//The TNM staging classification indicates that the tumor is relatively small (T2),//has not spread to nearby lymph nodes (N0), and has no distant metastasis (M0).//This suggests an early stage of adenocarcinoma.//'),

            'Large cell carcinoma: left > hilum T2_N2_M0_IIIa': Markup(
                'Large cell carcinoma is a type of non-small cell lung cancer (NSCLC).//It is characterized by the presence of large, abnormal-looking cells in the lung tissue.//The tumor is located in the left hilum, which is the area where the bronchi and blood vessels enter the lung.//The TNM staging classification indicates that the tumor is relatively large (T2),//has spread to nearby lymph nodes (N2), and has no distant metastasis (M0).//This suggests an advanced stage of large cell carcinoma.//'),

            'Normal': Markup(
                'Normal refers to the absence of any abnormalities or tumors.//A "Normal" result indicates that no suspicious masses or lesions were found on the scan.//It is important to note that "Normal" results do not rule out the possibility of future abnormalities//and regular screenings may be recommended for monitoring purposes.//'),

            'Squamous cell carcinoma: left > hilum T1_N2_M0_IIIa': Markup(
                'Squamous cell carcinoma is another type of non-small cell lung cancer (NSCLC).//It arises from the squamous cells lining the airways in the lungs.//The tumor is located in the left hilum, the area where the bronchi and blood vessels enter the lung.//The TNM staging classification indicates that the tumor is relatively small (T1),//has spread to nearby lymph nodes (N2), and has no distant metastasis (M0).//This suggests an advanced stage of squamous cell carcinoma.//')
        }

        index = ['Adenocarcinoma: left > lower lobe T2_N0_M0_Ib', 'Large cell carcinoma: left > hilum T2_N2_M0_IIIa'
            , 'Normal', 'Squamous cell carcinoma: left > hilum T1_N2_M0_IIIa']


        data = load_img(data, target_size=(224, 224))
        data = img_to_array(data)
        data = array_to_img(data, scale=False)
        data = data.resize((255, 255))
        data = img_to_array(data)

        data = np.expand_dims(data, axis=0)

        result = np.argmax(self.model.predict(data / 255.0), axis=1)
        result = index[result[0]]

        report_text = tumor_types[result]

        return result, report_text


    def checkIfCT(self, _image):
        images_labels = ["Not a CT image!", "CT"]
        threshold = 0.5

        image = img_to_array(_image)

        image = np.expand_dims(image, axis=0)
        res = self.detect_ct.predict(image)

        return images_labels[0] if res >= threshold else class_labels[1]