import os
import random

from flask import Flask, render_template, request, send_file, redirect, flash, url_for, json, jsonify, session, Response
from TumorSenseV1 import BrainTumor, LungTumor
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from ast import dump
from database.database import get_all_data, execute_query, User
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph
import smtplib



app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


is_authenticated = False
_user = None
_prediction = ''
# TODO: add the text to the pdf
_prediction_text = ''
title = 'TumorSense'

lung_detection_counter = {
    'Adenocarcinoma': 0,
    'Large cell carcinoma': 0,
    'Normal': 0,
    'Squamous cell carcinoma': 0,
}

brain_detection_counter = {
    'Glioma': 0,
    'Meningioma': 0,
    'Normal': 0,
    'Adenoma': 0
}

lung_detection_age = {
    'Adenocarcinoma': 0,
    'Large cell carcinoma': 0,
    'Normal': 0,
    'Squamous cell carcinoma': 0,
}

brain_detection_age = {
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


def load_tumorTypesCounts(doctor_id):
    global lung_detection_counter, brain_detection_counter

    # reset counts
    lung_detection_counter = {
        'Adenocarcinoma': 0,
        'Large cell carcinoma': 0,
        'Normal': 0,
        'Squamous cell carcinoma': 0,
    }

    brain_detection_counter = {
        'Glioma': 0,
        'Meningioma': 0,
        'Normal': 0,
        'Adenoma': 0
    }

    res = User.get_tumor_types_by_doctor_id(doctor_id)

    for tumor_type, lung_count, brain_count in res:
        if tumor_type == 'Normal_l' or tumor_type == 'Normal_b':
            tumor_type = 'Normal'
        if lung_count > 0:
            lung_detection_counter[tumor_type] += lung_count
        if brain_count > 0:
            brain_detection_counter[tumor_type] += brain_count

def load_average_age(doctor_id, doctor_type):
    global lung_detection_age, brain_detection_age

    #rest
    lung_detection_age = {
        'Adenocarcinoma': 0,
        'Large cell carcinoma': 0,
        'Normal': 0,
        'Squamous cell carcinoma': 0,
    }

    brain_detection_age = {
        'Glioma': 0,
        'Meningioma': 0,
        'Normal': 0,
        'Adenoma': 0
    }

    res = User.get_average_age_by_tumor_type(doctor_id, doctor_type)

    for tumor_type, _avg in res:
        if tumor_type == 'Normal_l' or tumor_type == 'Normal_b':
            tumor_type = 'Normal'
        if doctor_type == 'lung':
            lung_detection_age[tumor_type] = _avg
        if doctor_type == 'brain':
            brain_detection_age[tumor_type] = _avg


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_user(user_id):
    return User.get_doctor_user_by_id(user_id)

def generate_pdf(prediction, filename, title):
    pdf = SimpleDocTemplate(filename, pagesize=letter)

    title_style = ParagraphStyle(
        name='TitleStyle',
        fontSize=20,
        textColor=colors.black,
        spaceAfter=20
    )

    notice_style = ParagraphStyle(
        name='NoticeStyle',
        fontSize=12,
        textColor=colors.red,
        spaceAfter=10
    )

    content = []

    title_text = f'<b>{title}</b>'
    title_paragraph = Paragraph(title_text, title_style)
    content.append(title_paragraph)

    prediction_text = f"<br/><br/><b>Prediction:</b><br/>{prediction}"
    prediction_paragraph = Paragraph(prediction_text, style=ParagraphStyle(name='Normal'))
    content.append(prediction_paragraph)

    notice_text = "<br/><br/><i>Note: This prediction is AI-generated and may be inaccurate.</i>"
    notice_paragraph = Paragraph(notice_text, style=notice_style)
    content.append(notice_paragraph)

    pdf.build(content)

    # with open(filename, 'rb') as pdf_file:
    #     pdf_content = pdf_file.read()

    return send_file(filename, as_attachment=True)


def send_email_with_attachment(recipient_email, filename, attachment):
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    sender_email = 'your_email@example.com'
    sender_password = 'your_password'

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'Prediction PDF'

    attachment_part = MIMEApplication(attachment, Name=filename)
    attachment_part['Content-Disposition'] = f'attachment; filename="{filename}"'
    message.attach(attachment_part)

    server.send_message(message)

    server.quit()

    return True


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global is_authenticated, _user
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.get_doctor_user_by_username(username)
        if user and user['password'] == password:
            is_authenticated = True
            _user = user
            displayname = user['firstname'] + " " + user['lastname']
            session['displayname'] = displayname
            return render_template('dashboard.html', displayname=displayname, is_authenticated=True,
                                   user_type=user['doctor_type'])
        else:
            return render_template('welcome.html', is_authenticated=False, message="invalid username or password")
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    global is_authenticated
    is_authenticated = False
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/')
def index():
    if is_authenticated:
        return render_template('dashboard.html', is_authenticated=True,
                                   user_type=_user['doctor_type'])
    elif _user is None:
        return render_template('welcome.html', is_authenticated=False, message="invalid username or password")
    else:
        return  render_template('welcome.html', is_authenticated=False)

@app.route('/dashboard')
# @login_required
def dashboard():
    if is_authenticated:
        return render_template('dashboard.html', is_authenticated=True,
                                   user_type=_user['doctor_type'])
    else:
        return redirect(url_for('index'))


@app.route('/export-pdf', methods=['POST'])
def export_to_pdf():
    if _prediction:
        # _user_fullname = _user['firstname'] + _user['lastname']
        # pdf_filename = f'{_user_fullname}.pdf'
        pdf_filename = 'prediction.pdf'
        pdf_content = generate_pdf(_prediction, pdf_filename, title)

        response = Response(pdf_content, content_type='application/pdf')
        response.headers['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'

        return response
    else:
        return jsonify({'success': False, 'message': 'No prediction data provided'})

@app.route('/send-email', methods=['POST'])
def send_email():
    email = request.json.get('email')

    if prediction and email:
        _user_fullname = _user['firstname'] + _user['lastname']
        pdf_filename = f'{_user_fullname}.pdf'
        pdf_content = generate_pdf(_prediction, pdf_filename, title)

        send_email_with_attachment(email, pdf_filename, pdf_content)
        return jsonify({'success': True, 'message': 'Email sent successfully'})
    else:
        return jsonify({'success': False, 'message': 'Prediction data or email not provided'})


@app.route('/predict/<string:model_type>', methods=['POST'])
def predict(model_type):
    type = model_type.lower()

    if request.method == 'POST':
        global is_authenticated, _prediction
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
                        _prediction = prediction
                    #  else:
                    #      os.remove(file_path)
                    #      return render_template('predict.html',
                    #              detection_counter=json.dumps(lung_detection_counter),
                    #              type='lung', title="Lung")
                    case 'brain':
                        # imageType = brain_model.checkIfMRI(file_path)
                        # if imageType == brain_model._MRI:
                        prediction, report_text = brain_model.predict(file_path)
                        _prediction = prediction
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
    global is_authenticated, _user

    if not is_authenticated:
        return redirect(url_for('index'))

    load_tumorTypesCounts(_user['id'])
    load_average_age(_user['id'], _user['doctor_type'])

    match type:
        case 'lung':
            return render_template('predict.html', detection_counter=json.dumps(lung_detection_counter)
                                   ,avg_age=json.dumps(lung_detection_age), type='lung',
                                   title="Lung", showPopup='false', is_authenticated=is_authenticated)
        case 'brain':
            return render_template('predict.html', detection_counter=json.dumps(brain_detection_counter)
                                   ,avg_age=json.dumps(brain_detection_age), type='brain',
                                   title="Brain", showPopup='false', is_authenticated=is_authenticated)

        case _:
            return render_template('dashboard.html')


@app.route('/render', methods=['GET'])
def view_model():
    return render_template('render.html')


if __name__ == '__main__':
    app.run(debug=True, port=8001)
    # app.run()
