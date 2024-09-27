import sqlalchemy as sa
from sqlalchemy.sql import text
from flask_login import UserMixin

connection_uri = "sqlite:///database/database.db"

engine = sa.create_engine(connection_uri)

def execute_query(query, params=None):
    """
    Execute any SQL query safely with parameterized inputs.

    Args:
        query (str): The SQL query to execute.
        params (dict): Optional dictionary of parameter values.

    Returns:
        list: A list containing the fetched data.
    """
    with engine.connect() as con:
        if params is None:
            params = {}
        sql = text(query)
        res = con.execute(sql, params)
        return [row for row in res]

def execute_query_single(query, **params):
    """
    Execute any SQL query safely with parameterized inputs and return a single entry.

    Args:
        query (str): The SQL query to execute.
        **params: Optional keyword arguments for parameter values.

    Returns:
        dict: A dictionary containing the fetched data.
    """
    with engine.connect() as con:
        sql = text(query)
        res = con.execute(sql, params)
        row = res.fetchone()
        if row:
            column_names = [name.lower() for name in res.keys()]
            result = {column_names[i]: row[i] for i in range(len(column_names))}
            return result
        else:
            return None

def get_all_data(table_name):
    """
    Retrieve all rows from a specified table.

    Args:
        table_name (str): The name of the table.

    Returns:
        list: A list containing the fetched data.
    """
    query = f"SELECT * FROM {table_name}"
    return execute_query(query)


class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.password = user_data['password']
        self.firstname = user_data.get('firstname')
        self.lastname = user_data.get('lastname')
        self.doctor_type = user_data.get('doctor_type')
        self.email = user_data.get('email')
        self._is_active = True  # Default to True

    @staticmethod
    def get(user_id):
        """
        Retrieve a User object by its user ID.
        """
        user_data = User.get_doctor_user_by_id(user_id)
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_username(username):
        """
        Retrieve a User object by its username.
        """
        user_data = User.get_doctor_user_by_username(username)
        return User(user_data) if user_data else None

    def get_id(self):
        """
        Return the unique ID of the user.
        This method is required by Flask-Login.
        """
        return str(self.id)

    @property
    def is_authenticated(self):
        """
        Check if the user is authenticated.
        This method is required by Flask-Login.
        """
        return True

    @property
    def is_active(self):
        """
        Check if the user is active.
        This method is required by Flask-Login.
        """
        return self._is_active 

    @staticmethod
    def get_doctor_user_by_id(doctor_id):
        """
        Retrieve a doctor user by their ID.

        Args:
            doctor_id: The ID of the doctor.

        Returns:
            A dictionary representing the doctor user object.
        """
        if doctor_id is None:
            return None
        return execute_query_single(
            "SELECT * FROM DoctorsUsers du INNER JOIN Doctors AS doc ON doc.id = :doctor_id WHERE du.DoctorID = :doctor_id",
            doctor_id=doctor_id  
        )

    @staticmethod
    def get_doctor_user_by_username(username):
        """
        Retrieve a doctor user by username.

        Args:
            username: The username of the doctor.

        Returns:
            A dictionary representing the doctor user object.
        """
        if username is None:
            return None
        return execute_query_single(
            "SELECT * FROM DoctorsUsers du INNER JOIN Doctors AS doc ON du.DoctorID = doc.id WHERE du.Username = :username",
            username=username  
        )

    @staticmethod
    def get_patients_by_doctor_id(doctor_id):
        """
        Retrieve a list of patients for a specific doctor by their ID.

        Args:
            doctor_id: The ID of the doctor.

        Returns:
            A list of patient objects.
        """
        if doctor_id is None:
            return None
        return execute_query(
            "SELECT * FROM Patients INNER JOIN DoctorsPatients ON Patients.id = DoctorsPatients.PatientID "
            "WHERE DoctorsPatients.DoctorID = :doctor_id",
            params={'doctor_id': doctor_id}
        )

    @staticmethod
    def get_tumor_types_by_doctor_id(doctor_id):
        """
        Get a list of tumor types for a specific doctor.

        Args:
            doctor_id: The ID of the doctor.

        Returns:
            A list of tumor types with counts by category.
        """
        query = """
            SELECT
                TTM.TumorType,
                SUM(CASE WHEN TTM.Category = 'Lung' THEN 1 ELSE 0 END) AS LungCount,
                SUM(CASE WHEN TTM.Category = 'Brain' THEN 1 ELSE 0 END) AS BrainCount
            FROM
                Patients P
            INNER JOIN
                TumorTypeMapping TTM ON P.tumor_type = TTM.TumorType
            INNER JOIN
                DoctorsPatients DP ON P.id = DP.PatientID
            WHERE
                DP.DoctorID = :doctor_id
            GROUP BY
                TTM.TumorType;
        """
        return execute_query(query, params={'doctor_id': doctor_id})

    @staticmethod
    def get_average_age_by_tumor_type(doctor_id, doctor_type):
        """
        Get the average age of patients for each tumor type, filtered by doctor type.

        Args:
            doctor_id (str): The ID of the doctor.
            doctor_type (str): The type of doctor ('brain' or 'lung').

        Returns:
            A list of dictionaries containing the tumor type and average age.
        """
        if doctor_id is None or doctor_type not in ['brain', 'lung']:
            return None

        query = """
            SELECT
                TTM.TumorType,
                AVG(P.age) AS AverageAge
            FROM
                Patients P
            INNER JOIN
                DoctorsPatients DP ON P.id = DP.PatientID
            INNER JOIN
                Doctors D ON DP.DoctorID = D.id
            INNER JOIN
                TumorTypeMapping TTM ON lower(D.doctor_type) = lower(TTM.Category)
            WHERE
                D.id = :doctor_id
                AND lower(D.doctor_type) = :doctor_type
                AND lower(TTM.Category) = :doctor_type
            GROUP BY
                TTM.TumorType;
        """
        return execute_query(query, params={'doctor_id': doctor_id, 'doctor_type': doctor_type})

    @staticmethod
    def get_patients_by_doctor_id(doctor_id):
        """
        Get a list of patients for a specific doctor.

        Args:
            doctor_id: The ID of the doctor.

        Returns:
            A list of patients associated with the doctor.
        """
        query = """
            SELECT 
                P.id,
                P.firstname,
                P.lastname,
                P.age,
                P.sex,
                P.tumor_type,
                P.last_checkup
            FROM 
                Patients P
            INNER JOIN 
                DoctorsPatients DP ON P.id = DP.PatientID
            WHERE 
                DP.DoctorID = :doctor_id;
        """
        return execute_query(query, params={'doctor_id': doctor_id})