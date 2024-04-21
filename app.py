import os
import random

from flask import Flask, render_template, request, send_file, redirect, flash, url_for, json, jsonify, session
from TumorSenseV1 import BrainTumor, LungTumor
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from ast import dump
from database.database import get_all_data, execute_query, User
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

bcrypt = Bcrypt(app)

is_authenticated = False

# TODO: add more entries in patients table for lung tumor then populate this object
# TODO: use a special query to group each type and count them then assign values to the object
lung_detection_counter = {
    'Adenocarcinoma': 0,
    'Large cell carcinoma': 0,
    'Normal': 0,
    'Squamous cell carcinom': 0,
}

brain_detection_counter = {
    'Glioma': 0,
    'Meningioma': 0,
    'Normal': 0,
    'Adenoma': 0
}

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

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

key = Fernet.generate_key()
cipher_suite = Fernet(key)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_user(user_id):
    return User.get_doctor_user_by_id(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global is_authenticated
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.get_doctor_user_by_username(username)
        if user and user['password'] == password:
            is_authenticated = True
            displayname = user['firstname'] + " " + user['lastname']
            session['displayname'] = displayname
            return render_template('dashboard.html', displayname=displayname, is_authenticated=True)
        else:
            flash('Invalid username or password', 'error')
    return render_template('welcome.html', is_authenticated=False)

@app.route('/logout')
def logout():
    global is_authenticated
    is_authenticated = False
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/')
def index():
    if is_authenticated:
        return render_template('dashboard.html', is_authenticated=True)
    else:
        return render_template('welcome.html', is_authenticated=False)

@app.route('/dashboard')
# @login_required
def dashboard():
    if is_authenticated:
        return render_template('dashboard.html', is_authenticated=True)
    else:
        return render_template('welcome.html', is_authenticated=False)

@app.route('/predict/<string:model_type>', methods=['POST'])
def predict(model_type):
    type = model_type.lower()

    if request.method == 'POST':
        global is_authenticated
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

            if not is_authenticated:
                return redirect(url_for('index'))

            if type == 'lung':
                return render_template('predict.html', prediction=prediction,
                                       report_text=report_text, type='lung', title="Lung", showPopup='false',
                                       is_authenticated=is_authenticated)
            elif type == 'brain':
                return render_template('predict.html', prediction=prediction,
                                       report_text=report_text, type='brain', title="Brain", showPopup='false',
                                       is_authenticated=is_authenticated)


@app.route('/detect/<string:model_type>', methods=['GET'])
def view_prediction_page(model_type):
    type = model_type.lower()
    global is_authenticated

    if not is_authenticated:
        return redirect(url_for('index'))

    match type:
        case 'lung':
            return render_template('predict.html', detection_counter=json.dumps(lung_detection_counter),
                                   type='lung', title="Lung", showPopup='false', is_authenticated=is_authenticated)
        case 'brain':
            return render_template('predict.html', detection_counter=json.dumps(brain_detection_counter),
                                   type='brain', title="Brain", showPopup='false', is_authenticated=is_authenticated)

        case _:
            return render_template('dashboard.html')


@app.route('/render', methods=['GET'])
def view_model():
    return render_template('render.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
    # app.run()
