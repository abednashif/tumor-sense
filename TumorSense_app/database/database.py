from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


def get_engine():
    return create_engine("mssql+pyodbc://sa:pass_1234@127.0.0.1:1433/tumorsense?driver=SQL+Server+Native+Client+11.0")


def get_conn():
    return "mssql+pyodbc://sa:pass_1234@127.0.0.1:1433/tumorsense?driver=SQL+Server+Native+Client+11.0"


db = SQLAlchemy()
engine = get_engine()
db.metadata.bind = engine


class Patient(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    tumor_type = db.Column(db.String(50))
    last_checkup = db.Column(db.DateTime)


def fetch_all_patients():
    return Patient.query.all()


def fetch_patient(patient_id):
    return Patient.query.get(patient_id)


def create_patient(id, firstname, lastname, age, tumor_type, last_checkup):
    patient = Patient(id=id, firstname=firstname, lastname=lastname, age=age, tumor_type=tumor_type, last_checkup=last_checkup)
    db.session.add(patient)
    db.session.commit()


def get_patient_by_id(id):
    return Patient.query.filter_by(id=id).first()

