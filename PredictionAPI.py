# To use this API

# import requests
#
# url = 'http://localhost:5700/predict'
#
# code = 'pass'
#
# file_path = '/path/to/your/image.jpg'
#
# files = {'input_data': open(file_path, 'rb')}
# data = {'code': code}
#
# response = requests.post(url, files=files, data=data)
#
# if response.status_code == 200:
#     prediction = response.json()['prediction']
#     print('Prediction:', prediction)
# else:
#     print('Error:', response.text)


from flask import Flask, request
from flask_restful import Api, Resource
from TumorSenseV1 import BrainTumor
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
api = Api(app)
model = BrainTumor()

current_directory = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(current_directory, 'uploads')
ENCRYPTED_FOLDER = os.path.join(current_directory, 'encrypted')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

key = Fernet.generate_key()
cipher_suite = Fernet(key)

# TODO: add a UI method to generate an API key for a registered user
AUTH_CODE = "pass"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Predict(Resource):
    def post(self):
        code = request.form.get('code')
        if code != AUTH_CODE:
            return {'message': 'Invalid authentication code'}, 401

        if 'input_data' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['input_data']

        if file.filename == '':
            return {'message': 'No selected file'}, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # TODO: validate input data

            if os.path.exists(file_path):
                prediction = model.predict(file_path)
            else:
                return {'message': 'Error: File not found'}, 404

            with open(file_path, 'rb') as f:
                plaintext = f.read()
            encrypted_data = cipher_suite.encrypt(plaintext)

            encrypted_file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], 'encrypted_' + filename)
            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_data)

            os.remove(file_path)

            # TODO add if login then allow image decryption

            return {'prediction': prediction}, 200
        else:
            return {'message': 'Invalid file type'}, 400


api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True, port=5700)
