import sqlalchemy as sa
from sqlalchemy.sql import text
from flask_login import UserMixin

connection_uri = sa.engine.url.URL(
    "mssql+pyodbc",
    username="sa",
    password="pass_1234",
    host="127.0.0.1",
    database="TumorSense",
    port=1433,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "ApplicationIntent": "ReadOnly",
    },
)


engine = sa.create_engine(connection_uri)


def execute_query(query, **params):
    """
    Execute any SQL query safely with parameterized inputs.

    Args:
        query (str): The SQL query to execute.
        **params: Optional keyword arguments for parameter values.

    Returns:
        list: A list containing the fetched data.
    """
    with engine.connect() as con:
        sql = text(query)
        res = con.execute(sql, **params)
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
        res = con.execute(sql, **params)
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


class User:
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.password = user_data['password']
        self.is_active = True
    @staticmethod
    def get(self, user_id):
        user_data = get_doctor_user_by_id(user_id)
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_username(self, username):
        user_data = self.get_doctor_user_by_username(username)
        return User(user_data) if user_data else None



    def get_doctor_user_by_id(doctor_id):
        """
        Retrieve a doctor user by id.

        Args:
            doctor_id: or user_id

        Returns:
            obj: The doctor user object.
        """
        return execute_query_single(f"SELECT * FROM DoctorsUsers du INNER JOIN Doctors AS doc ON doc.id = '{doctor_id}'"
                                    f" WHERE du.DoctorID = '{doctor_id}'")

    def get_doctor_user_by_username(username):
        """
        Retrieve a doctor user by username.
        Args:
            username: username
        Returns:
            obj: The doctor user object.
        """
        return execute_query_single(f"SELECT * FROM DoctorsUsers du INNER JOIN Doctors AS doc ON "
                                    f" du.DoctorID = doc.id WHERE du.Username = '{username}'")

    def get_patients_by_doctor_id(doctor_id):
        """
        Get a doctor's patients.

        Returns:
            list: A list of patient objects.
        """
        return execute_query(f"SELECT * FROM Patients INNER JOIN DoctorsPatients "
                                 f"ON Patients.id = DoctorsPatients.PatientID "
                                 f"WHERE DoctorsPatients.DoctorID = '{doctor_id}'")

