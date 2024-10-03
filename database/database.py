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
    with engine.begin() as con:
        if params is None:
            params = {}
        sql = text(query)
        res = con.execute(sql, params)

        if res.returns_rows:
            return [row for row in res]
        else:
            return res.rowcount

def execute_query_single(query, **params):
    """
    Execute any SQL query safely with parameterized inputs and return a single entry.

    Args:
        query (str): The SQL query to execute.
        **params: Optional keyword arguments for parameter values.

    Returns:
        dict: A dictionary containing the fetched data.
    """
    with engine.begin() as con:
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
    def get_patients_by_doctor_id(doctor_id, doctor_type):
        """
        Retrieve a list of patients for a specific doctor by their ID and ensure
        that the patient's tumor type matches the doctor's specialty, case-insensitive.

        Args:
            doctor_id: The ID of the doctor.
            doctor_type: The type of the doctor.

        Returns:
            A list of patient objects.
        """
        if doctor_id is None or doctor_type is None:
            return None

        return execute_query(
            "SELECT P.* "
            "FROM Patients AS P "
            "INNER JOIN DoctorsPatients AS DP ON P.id = DP.PatientID "
            "INNER JOIN TumorTypeMapping AS TTM ON P.tumor_type = TTM.TumorType "
            "INNER JOIN Doctors AS D ON DP.DoctorID = D.id "
            "WHERE DP.DoctorID = :doctor_id AND LOWER(TTM.Category) = LOWER(:doctor_type) "
            "ORDER BY CASE WHEN P.last_checkup IS NULL THEN 1 ELSE 0 END, P.last_checkup",
            params={'doctor_id': doctor_id, 'doctor_type': doctor_type}
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
                TumorTypeMapping TTM ON P.tumor_type = TTM.TumorType
            WHERE
                D.id = :doctor_id
                AND lower(D.doctor_type) = lower(:doctor_type)
                AND lower(TTM.Category) = lower(:doctor_type)
            GROUP BY
                TTM.TumorType;
        """
        return execute_query(query, params={'doctor_id': doctor_id, 'doctor_type': doctor_type})

    @staticmethod
    def update_patient_info_after_prediction(patient_id, new_patient_info):
        """
        Update patient information after a prediction.

        Args:
            patient_id: The ID of the patient.
            new_patient_info: A dictionary containing updated tumor_type and last_checkup date.

        Returns:
            A boolean indicating success or failure of the update operation.
        """
        if not new_patient_info or patient_id is None:
            print("Invalid input: new_patient_info or patient_id is None")
            return False

        query = """
            UPDATE Patients
            SET tumor_type = :tumor_type,
                last_checkup = :last_checkup
            WHERE id = :patient_id;
        """

        try:
            result = execute_query(query, params={
                'tumor_type': new_patient_info['tumor_type'],
                'last_checkup': new_patient_info['last_checkup'],
                'patient_id': patient_id
            })
            print(f"Update result: {result} rows affected")
            return result > 0
        except Exception as e:
            print(f"Error updating patient info: {e}")
            return False

    @staticmethod
    def patients_exceeded_30_days_count(_user_id, doctor_type):
        """
        Get the number of patients exceeded 30 days from last checkup, ensuring the patient's tumor type matches the doctor's specialty.

        Args:
            _user_id: The ID of the doctor.
            doctor_type: The type of the doctor.

        Returns:
            Number of patients.
        """

        if _user_id is None or doctor_type is None:
            print("Invalid input: _user_id or doctor_type is None")
            return False

        query = """
                SELECT COUNT(*)
                FROM Patients AS p
                JOIN DoctorsPatients AS dp ON p.id = dp.PatientID
                JOIN TumorTypeMapping AS ttm ON p.tumor_type = ttm.TumorType
                JOIN Doctors AS d ON dp.DoctorID = d.id
                WHERE dp.DoctorID = :_user_id
                AND LOWER(ttm.Category) = LOWER(:doctor_type)
                AND DATE('now') > DATE(p.last_checkup, '+30 days');
            """
        return execute_query(query, params={'_user_id': _user_id, 'doctor_type': doctor_type})[0][0]


    @staticmethod
    def add_patient(patient_data):
        """
        Add a new patient and associate them with a doctor.

        Args:
            patient_data: A dictionary containing:
                - firstname
                - lastname
                - age
                - sex
                - tumor_type
                - doctor_id
                - last_checkup

        Returns:
            Boolean indicating success or failure
        """
        if not patient_data:
            print("Invalid input: patient_data is None")
            return False

        new_id_query = """
            SELECT COALESCE(MAX(CAST(SUBSTR(id, 2) AS INTEGER)), 0) + 1 
            FROM Patients 
            WHERE id LIKE 'P%';
        """

        try:
            new_id_num = execute_query(new_id_query)[0][0]
            new_patient_id = f"P{new_id_num:04d}"

            insert_patient_query = """
                INSERT INTO Patients (id, firstname, lastname, age, sex, tumor_type, last_checkup)
                VALUES (:id, :firstname, :lastname, :age, :sex, :tumor_type, :last_checkup);
            """

            execute_query(insert_patient_query, params={
                'id': new_patient_id,
                'firstname': patient_data['firstname'],
                'lastname': patient_data['lastname'],
                'age': patient_data['age'],
                'sex': patient_data['sex'],
                'tumor_type': patient_data['tumor_type'],
                'last_checkup': patient_data['last_checkup']
            })

            link_doctor_patient_query = """
                INSERT INTO DoctorsPatients (DoctorID, PatientID)
                VALUES (:doctor_id, :patient_id);
            """

            execute_query(link_doctor_patient_query, params={
                'doctor_id': patient_data['doctor_id'],
                'patient_id': new_patient_id
            })

            return True

        except Exception as e:
            print(f"Error adding patient: {e}")
            return False