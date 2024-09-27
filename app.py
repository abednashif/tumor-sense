import os
import smtplib
from ast import dump
from io import BytesIO
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, send_file, redirect, flash, url_for, json, jsonify, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from werkzeug.utils import secure_filename
# from gevent.pywsgi import WSGIServer

from TumorSenseV1 import BrainTumor, LungTumor
from database.database import User


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

_prediction = ''
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

brain_model = BrainTumor()
lung_model = LungTumor()


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

    if res is None or len(res) == 0:
        return

    for tumor_type, _avg in res:
        if tumor_type == 'Normal_l' or tumor_type == 'Normal_b':
            tumor_type = 'Normal'
        if doctor_type == 'lung':
            lung_detection_age[tumor_type] = _avg
        elif doctor_type == 'brain':
            brain_detection_age[tumor_type] = _avg

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_pdf(prediction, prediction_description, title):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

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

    prediction_description_text = f"<br/><br/>{prediction_description}"
    prediction_description_text = prediction_description_text.replace('//', '<br/>')

    content.append(Paragraph(prediction_description_text, style=ParagraphStyle(name='Normal')))

    notice_text = "<br/><br/><br/><i>Note: This prediction is AI-generated and may be inaccurate.</i>"
    notice_paragraph = Paragraph(notice_text, style=notice_style)
    content.append(notice_paragraph)

    pdf.build(content)

    buffer.seek(0)
    return buffer


def send_email_with_attachment(recipient_email, filename, attachment):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    sender_email = 'tumorsense@gmail.com'
    sender_password = os.environ.get('EMAIL_PASSWORD')

    subject = "TumorSense Prediction PDF"
    body = "Please find attached the PDF containing your TumorSense prediction."

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        attachment_part = MIMEApplication(attachment, Name=filename)
        attachment_part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(attachment_part)

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.get_doctor_user_by_username(username)
        if user and user['password'] == password:
            user_id = user['id']
            if isinstance(user_id, str):
                user_id = int(user_id)

            user_obj = User(user)
            login_user(user_obj)
            session['user_id'] = user_id
            displayname = user['firstname'] + " " + user['lastname']
            session['displayname'] = displayname
            session['doctor_type'] = user['doctor_type']

            return render_template('dashboard.html', displayname=displayname, is_authenticated=True,
                                   user_type=user['doctor_type'])
        else:
            return render_template('welcome.html', is_authenticated=False, message="invalid username or password")
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html', is_authenticated=True,
                               user_type=current_user.doctor_type)
    else:
        return render_template('home.html', is_authenticated=False)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html', is_authenticated=True,
                               user_type=current_user.doctor_type)
    else:
        return redirect(url_for('index'))


@app.route('/export-pdf', methods=['POST'])
@login_required
def export_to_pdf():
    if _prediction:
        pdf_filename = 'prediction.pdf'
        pdf_buffer = generate_pdf(_prediction, _prediction_text, _prediction_title)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=pdf_filename,
            mimetype='application/pdf'
        )
    else:
        return jsonify({'success': False, 'message': 'No prediction data available'}), 400


@app.route('/send-email', methods=['POST'])
def send_mail():
    email = request.json.get('email')

    if _prediction and email:
        pdf_filename = 'prediction.pdf'
        pdf_buffer = generate_pdf(_prediction, _prediction_text, _prediction_title)

        try:
            send_email_with_attachment(email, pdf_filename, pdf_buffer.getvalue())
            return jsonify({'success': True, 'message': 'Email sent successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Failed to send email: {str(e)}'}), 500
    else:
        return jsonify({'success': False, 'message': 'Prediction data or email not provided'}), 400


@app.route('/predict/<string:model_type>', methods=['POST'])
def predict(model_type):
    type = model_type.lower()

    if request.method == 'POST':
        global _prediction, _prediction_title, _prediction_text

        if 'input_data' not in request.files:
            return 'No file part'

        file = request.files['input_data']

        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user_id = str(current_user.id)
            user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)

            if not os.path.exists(user_upload_folder):
                os.makedirs(user_upload_folder)

            file_path = os.path.join(user_upload_folder, filename)
            file.save(file_path)

            try:
                if type == 'lung':
                    prediction, report_text = lung_model.predict(file_path)
                    _prediction_title = "Lung Tumor Detection"
                elif type == 'brain':
                    prediction, report_text = brain_model.predict(file_path)
                    _prediction_title = "Brain Tumor Detection"
                else:
                    return "Model does not exist!"

                _prediction = prediction
                _prediction_text = report_text
            except Exception as e:
                return f"Error: {str(e)}"
            finally:
                print("Finished prediction")

            with open(file_path, 'rb') as f:
                plaintext = f.read()
            encrypted_data = cipher_suite.encrypt(plaintext)

            encrypted_folder = os.path.join(app.config['ENCRYPTED_FOLDER'], user_id)
            if not os.path.exists(encrypted_folder):
                os.makedirs(encrypted_folder)

            encrypted_file_path = os.path.join(encrypted_folder, f'encrypted_{filename}')

            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_data)

            os.remove(file_path)

            return render_template('predict.html', prediction=prediction,
                                   report_text=report_text, type=type, title=type.capitalize(), showPopup='false',
                                   is_authenticated=True)

    return redirect(url_for('index'))

@app.route('/profile/<string:username>', methods=['GET'])
@login_required
def get_profile(username):
    if current_user.is_authenticated == False:
        return redirect(url_for('index'))

    if username == current_user.username:
        patients = User.get_patients_by_doctor_id(current_user.id)
        return render_template('profile.html', user=current_user, patients=patients, is_authenticated=True)
    return redirect(url_for('index'))

@app.route('/detect/<string:model_type>', methods=['GET'])
def view_prediction_page(model_type):
    model_type = model_type.lower()

    if not session.get('user_id'):
        return redirect(url_for('index'))

    user_id = session['user_id']
    doctor_type = session['doctor_type'] if 'doctor_type' in session else None

    load_tumorTypesCounts(user_id)
    load_average_age(user_id, doctor_type)

    if model_type == 'lung':
        return render_template('predict.html', detection_counter=json.dumps(lung_detection_counter),
                               avg_age=json.dumps(lung_detection_age), type='lung',
                               title="Lung", showPopup='false', is_authenticated=True)
    elif model_type == 'brain':
        return render_template('predict.html', detection_counter=json.dumps(brain_detection_counter),
                               avg_age=json.dumps(brain_detection_age), type='brain',
                               title="Brain", showPopup='false', is_authenticated=True)
    else:
        return render_template('dashboard.html')



@app.route('/decrypt/<filename>', methods=['GET'])
@login_required
def decrypt_file(filename):
    encrypted_file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], filename)
    if not os.path.exists(encrypted_file_path):
        return "File not found", 404

    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = cipher_suite.decrypt(encrypted_data)

    decrypted_filename = filename.replace('encrypted_', 'decrypted_')
    return send_file(
        BytesIO(decrypted_data),
        as_attachment=True,
        download_name=decrypted_filename,
        mimetype='application/octet-stream'
    )


if __name__ == '__main__':
    # app.run(debug=True, port=8002)
    app.run(host='0.0.0.0', port=8001)
    # production
    # http_server = WSGIServer(('', 8001), app)
    # http_server.serve_forever()
