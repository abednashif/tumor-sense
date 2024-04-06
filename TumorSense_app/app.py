
from flask import Flask, render_template, request, send_file, redirect, flash, url_for
from TumorSenseV1 import TumorSense
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
# from flask_sqlalchemy import SQLAlchemy
# from model_classes.user import User
import os

app = Flask(__name__)
model = TumorSense()

# TODO:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@hostname/database_name'
# db = SQLAlchemy(app)

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



@app.route('/predict', methods=['POST'])
def predict():
    # to test the prediction without doing all of the logic
    # reportText = ("Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium,                   optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis) obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam,                  nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit, tenetur error, harum nesciunt ipsum debitis quas aliquid. Reprehenderit, quia.")
    # return render_template('predict.html', prediction='Giloma', report_text=reportText)

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

            # TODO: validate input data

            if os.path.exists(file_path):
                prediction, report_text = model.predict(file_path)
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

            return render_template('predict.html', prediction=prediction, report_text=report_text)


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