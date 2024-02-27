
from flask import Flask, render_template, request, send_file
from TumorSenseV1 import TumorSense
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
model = TumorSense()

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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'input_data' not in request.files:
            return 'No file part'

        file = request.files['input_data']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            # Save the uploaded file to the uploads folder
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # TODO: validate input data

            if os.path.exists(file_path):
                prediction = model.predict(file_path)
            else:
                return 'Error: File not found'

            with open(file_path, 'rb') as f:
                plaintext = f.read()
            encrypted_data = cipher_suite.encrypt(plaintext)


            encrypted_file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], 'encrypted_' + filename)
            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_data)

            os.remove(file_path)

            # TODO add if login then allow image decryption

            return render_template('predict.html', prediction=prediction)


@app.route('/detect', methods=['GET'])
def view_prediction_page():
    return render_template('predict.html')


@app.route('/render', methods=['GET'])
def view_model():
    return render_template('render.html')


if __name__ == '__main__':
    app.run(debug=True, port=5700)

'''
    To run the app:
        1. Open a terminal
        2. execute "python app.py"
        3. copy or press the link or paste "http://127.0.0.1:5700 or http://localhost:5700" in the browser
'''