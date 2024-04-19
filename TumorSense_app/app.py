import os
import random

from flask import Flask, render_template, request, send_file, redirect, flash, url_for, json
from TumorSenseV1 import BrainTumor, LungTumor
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from ast import dump
from database.database import get_all_data, execute_query

app = Flask(__name__)


brain_model = BrainTumor()
lung_model = LungTumor()


current_directory = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(current_directory, 'uploads')
ENCRYPTED_FOLDER = os.path.join(current_directory, 'encrypted')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER
# app.config = get_conn()
#
# with app.app_context():
#     db.create_all()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

key = Fernet.generate_key()
cipher_suite = Fernet(key)

lung_detection_counter = {
    'Adenocarcinoma': random.randint(1, 50),
    'Large cell carcinoma': random.randint(1, 50),
    'Normal': random.randint(1, 50),
    'Squamous cell carcinom': random.randint(1, 50),
}

brain_detection_counter = {
    'Glioma': random.randint(1, 50),
    'Meningioma': random.randint(1, 50),
    'Normal': random.randint(1, 50),
    'Adenoma': random.randint(1, 50)
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             flash('Username already exists. Please choose a different one.', 'error')
#             return redirect(url_for('register'))
#
#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#
#         flash('You have been successfully registered. Please log in.', 'success')
#         return redirect(url_for('login'))
#
#     return render_template('register.html')


@app.route('/predict/<string:model_type>', methods=['POST'])
def predict(model_type):
    type = model_type.lower()

    if request.method == 'POST':
        if 'input_data' not in request.files:
            return 'No file part'

        file = request.files['input_data']

        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                match type:
                    case 'lung':
                        # imageType = lung_model.checkIfCT(file_path)
                        # if imageType == lung_model._CT:
                            prediction, report_text = lung_model.predict(file_path)
                        #  else:
                        #      os.remove(file_path)
                        #      return render_template('predict.html',
                        #              detection_counter=json.dumps(lung_detection_counter),
                        #              type='lung', title="Lung")
                    case 'brain':
                        # imageType = brain_model.checkIfMRI(file_path)
                        # if imageType == brain_model._MRI:
                            prediction, report_text = brain_model.predict(file_path)
                        # else:
                        #     os.remove(file_path)
                        #     return render_template('predict.html',
                        #                            detection_counter=json.dumps(brain_detection_counter),
                        #                            type='brain', title="Brain", showPopup='true')
                    case _:
                        return "Model does not exist!"
            except Exception.args as e:
                return "Model does not exist!"
            finally:
                print("finished")


            with open(file_path, 'rb') as f:
                plaintext = f.read()
            encrypted_data = cipher_suite.encrypt(plaintext)


            encrypted_file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], 'encrypted_' + filename)
            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_data)

            os.remove(file_path)

            if type == 'lung':
                return render_template('predict.html', prediction=prediction,
                                       report_text=report_text, type='lung', title="Lung", showPopup='false')
            elif type == 'brain':
                return render_template('predict.html', prediction=prediction,
                                       report_text=report_text, type='brain', title="Brain", showPopup='false')


@app.route('/detect/<string:model_type>', methods=['GET'])
def view_prediction_page(model_type):
    type = model_type.lower()

    match type:
        case 'lung':
            return render_template('predict.html', detection_counter=json.dumps(lung_detection_counter),
                                   type='lung', title="Lung", showPopup='false')
        case 'brain':
            return render_template('predict.html', detection_counter=json.dumps(brain_detection_counter),
                                   type='brain', title="Brain", showPopup='false')

        case _:
            return render_template('index.html')

@app.route('/render', methods=['GET'])
def view_model():
    return render_template('render.html')


if __name__ == '__main__':
    app.run(debug=True, port=5700)
