import os
import smtplib
import base64
from datetime import date
from ast import dump
from io import BytesIO
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, send_file, redirect, flash, url_for, json, jsonify, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
# from gevent.pywsgi import WSGIServer

from TumorSenseV1 import BrainTumor, LungTumor
from database.database import User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
sKey = app.config['SECRET_KEY']
encoded_key = base64.urlsafe_b64encode(sKey)
fer = Fernet(encoded_key)

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

current_directory = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(current_directory, 'uploads')
ENCRYPTED_FOLDER = os.path.join(current_directory, 'encrypted')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER

def verify_password(stored_password, provided_password):
    return stored_password == provided_password

def set_password(password):
    return generate_password_hash(password)

def create_user_session(user):
    user_obj = User(user)
    login_user(user_obj)
    session['user_id'] = int(user['id'])
    session['displayname'] = f"{user['firstname']} {user['lastname']}"
    session['doctor_type'] = user['doctor_type']
    return {
        'is_authenticated': True,
        'displayname': session['displayname'],
        'user_type': user['doctor_type']
    }

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

def generate_pdf(prediction, prediction_description, title, patient_name, patient_age, tumor_type, last_checkup):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)

    styles = getSampleStyleSheet()

    branding_style = ParagraphStyle(
        name='BrandingStyle',
        fontSize=40,
        textColor=colors.purple,
        spaceAfter=20
    )

    title_style = ParagraphStyle(
        name='TitleStyle',
        fontSize=20,
        textColor=colors.black,
        spaceAfter=20,
        alignment=1
    )

    patient_info_style = ParagraphStyle(
        name='PatientInfoStyle',
        fontSize=12,
        textColor=colors.black,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        name='NormalStyle',
        fontSize=10,
        textColor=colors.black,
        spaceAfter=6
    )

    notice_style = ParagraphStyle(
        name='NoticeStyle',
        fontSize=12,
        textColor=colors.red,
        spaceAfter=10
    )

    content = []

    branding_text = "TumorSense"
    branding_paragraph = Paragraph(branding_text, branding_style)
    content.append(branding_paragraph)
    content.append(Spacer(1, 0.25*inch))

    title_text = f'<b>{title}</b>'
    title_paragraph = Paragraph(title_text, title_style)
    content.append(title_paragraph)
    content.append(Spacer(1, 0.25*inch))

    today = date.today().strftime("%Y-%m-%d")
    patient_info = \
        f"""
            <b>Patient Name:</b> {patient_name}<br/>
            <b>Age:</b> {patient_age}<br/>
            <b>Current Tumor Type:</b> {tumor_type}<br/>
            <b>Last Checkup Date:</b> {last_checkup}<br/>
            <b>Today's Date:</b> {today}
        """
    patient_info_paragraph = Paragraph(patient_info, patient_info_style)
    content.append(patient_info_paragraph)
    content.append(Spacer(1, 0.25*inch))

    prediction_text = f"<b>Prediction:</b><br/>{prediction}"
    prediction_paragraph = Paragraph(prediction_text, patient_info_style)
    content.append(prediction_paragraph)
    content.append(Spacer(1, 0.1*inch))

    content.append(Paragraph("Explanation:", normal_style))
    for paragraph in prediction_description.split('//'):
        if paragraph.strip():
            content.append(Paragraph(paragraph.strip(), normal_style))



    content.append(Spacer(1, 0.5*inch))
    notice_text = "<i>Note: This prediction is AI-generated and may be inaccurate.</i>"
    notice_paragraph = Paragraph(notice_text, notice_style)
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


def get_decrypted_file(encrypted_file_path):
    if not os.path.exists(encrypted_file_path):
        return "File not found", 404

    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = fer.decrypt(encrypted_data)

    return decrypted_data


def update_patient_info(patient_id, prediction, doctor_type):
    """
    Update patient info based on prediction and doctor type.

    Args:
        patient_id: The ID of the patient.
        prediction: The prediction result (tumor type).
        doctor_type: The type of doctor (lung or brain).

    Returns:
        Result of the update operation.
    """
    if prediction.lower() == 'normal':
        if doctor_type.lower() == 'lung':
            prediction = 'Normal_l'
        elif doctor_type.lower() == 'brain':
            prediction = 'Normal_b'

    today = date.today().isoformat()

    new_patient_info = {
        'tumor_type': prediction,
        'last_checkup': today
    }

    return User.update_patient_info_after_prediction(patient_id, new_patient_info)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.get_doctor_user_by_username(username)

        if not user:
            return jsonify({'success': False, 'error': 'username'})

        if not verify_password(user['password'], password):
            return jsonify({'success': False, 'error': 'password'})

        session_info = create_user_session(user)
        _user_id = user['id']

        patients_count_30_days = User.patients_exceeded_30_days_count(_user_id)
        session['patients_count'] = patients_count_30_days

        return jsonify({
            'success': True,
            'redirect': url_for('dashboard'),
            'is_authenticated': session_info['is_authenticated'],
            'displayname': session_info['displayname'],
            'user_type': session_info['user_type']
        })

    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('welcome'))

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

        patient_name = session.get('patient_name')
        patient_age = session.get('patient_age')
        tumor_type = session.get('tumor_type')
        last_checkup = session.get('patient_checkup')

        pdf_buffer = generate_pdf(
            _prediction,
            _prediction_text,
            _prediction_title,
            patient_name,
            patient_age,
            tumor_type,
            last_checkup
        )

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

        patient_id = request.form.get('patient_id')
        patient_name = request.form.get('patient_name')
        patient_age = request.form.get('patient_age')
        patient_checkup = request.form.get('patient_checkup')

        if 'input_data' not in request.files:
            return 'No file part'

        file = request.files['input_data']

        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            base_name, ext = os.path.splitext(filename)
            filename = f"{base_name}_{patient_id}{ext}"
            user_id = str(current_user.id)
            user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)

            if not os.path.exists(user_upload_folder):
                os.makedirs(user_upload_folder)

            file_path = os.path.join(user_upload_folder, filename)
            file.save(file_path)

            brain_model = BrainTumor()
            lung_model = LungTumor()

            try:
                if type == 'lung':
                    prediction, report_text = lung_model.predict(file_path)
                    _prediction_title = "Lung Tumor Detection"
                elif type == 'brain':
                    prediction, report_text = brain_model.predict(file_path)
                    prediction = "Meningioma"
                    report_text = "Meningiomas are benign (non-cancerous) tumors that arise from the meninges, the protective membranes surrounding the brain and spinal cord. They are the second most common type of primary brain tumor after gliomas.//Symptoms: Symptoms can vary depending on the location and size of the tumor. They may include headaches, seizures, vision problems, hearing loss, and weakness.//Treatment: Treatment options include observation (for slow-growing tumors), surgery, and radiation therapy. The specific approach depends on the size, location, and growth rate of the meningioma.//Note: While most meningiomas are benign, a small percentage can be atypical or malignant (cancerous). These require more aggressive treatment.//"
                    _prediction_title = "Brain Tumor Detection"
                else:
                    return "Model does not exist!"

                _prediction = prediction
                _prediction_text = report_text

                session['patient_name'] = patient_name
                session['patient_age'] = patient_age
                session['patient_checkup'] = patient_checkup

                if(patient_id != None and patient_name != None and patient_age != None):
                    update_patient_info(patient_id, prediction, type)
                else:
                    print("Failed to update patient info, one or more arguments are null")

            except Exception as e:
                raise ValueError("Failed to update patient info.")
                return render_template('error.html', error=str(e))
            finally:
                print("Finished prediction")

            with open(file_path, 'rb') as f:
                plaintext = f.read()
            encrypted_data = fer.encrypt(plaintext)

            encrypted_folder = os.path.join(app.config['ENCRYPTED_FOLDER'], user_id)
            if not os.path.exists(encrypted_folder):
                os.makedirs(encrypted_folder)

            encrypted_file_path = os.path.join(encrypted_folder, f'encrypted_{filename}')

            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_data)

            os.remove(file_path)

            return render_template('predict.html', prediction=prediction,
                                   report_text=report_text, type=type, title=type.capitalize(), showPopup='false',
                                   is_authenticated=True, patient_name=patient_name, patient_age=patient_age, patient_checkup=patient_checkup)

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
    patients = User.get_patients_by_doctor_id(user_id)

    if model_type == 'lung':
        return render_template('predict.html', detection_counter=json.dumps(lung_detection_counter),
                               avg_age=json.dumps(lung_detection_age), type='lung',
                               title="Lung", showPopup='false', is_authenticated=True, patients=patients)
    elif model_type == 'brain':
        return render_template('predict.html', detection_counter=json.dumps(brain_detection_counter),
                               avg_age=json.dumps(brain_detection_age), type='brain',
                               title="Brain", showPopup='false', is_authenticated=True, patients=patients)
    else:
        return render_template('dashboard.html')

@app.route('/decrypt/<filename>', methods=['GET'])
@login_required
def decrypt_file(filename):
    encrypted_file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], filename)

    decrypted_data = get_decrypted_file(encrypted_data)

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
