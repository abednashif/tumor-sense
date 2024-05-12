import sqlite3

def create_sqlite_database(filename):
    """ create a database connection to an SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_tables():
    drop_statements = [
        "DROP TABLE IF EXISTS DoctorsPatients;",
        "DROP TABLE IF EXISTS DoctorsUsers;",
        "DROP TABLE IF EXISTS Patients;",
        "DROP TABLE IF EXISTS Doctors;",
        "DROP TABLE IF EXISTS TumorTypeMapping;"
    ]

    create_statements = [
        """CREATE TABLE IF NOT EXISTS Patients (
                id TEXT PRIMARY KEY, 
                firstname TEXT NOT NULL, 
                lastname TEXT NOT NULL, 
                age INTEGER NOT NULL, 
                sex TEXT NOT NULL, 
                tumor_type TEXT, 
                last_checkup TEXT
        );""",
        """CREATE TABLE IF NOT EXISTS Doctors (
                id TEXT PRIMARY KEY, 
                firstname TEXT NOT NULL, 
                lastname TEXT NOT NULL, 
                email TEXT NOT NULL, 
                role TEXT NOT NULL, 
                doctor_type TEXT NOT NULL, 
                successful_operations INTEGER
        );""",
        """CREATE TABLE IF NOT EXISTS DoctorsUsers (
                DoctorID TEXT PRIMARY KEY, 
                Username TEXT NOT NULL, 
                Password TEXT NOT NULL
        );""",
        """CREATE TABLE IF NOT EXISTS DoctorsPatients (
                DoctorID TEXT NOT NULL, 
                PatientID TEXT NOT NULL, 
                PRIMARY KEY (DoctorID, PatientID), 
                FOREIGN KEY (DoctorID) REFERENCES Doctors(id), 
                FOREIGN KEY (PatientID) REFERENCES Patients(id)
        );""",
        """CREATE TABLE IF NOT EXISTS TumorTypeMapping (
                TumorType TEXT PRIMARY KEY, 
                Category TEXT NOT NULL
        );"""
    ]

    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()

            # Drop existing tables
            for drop_statement in drop_statements:
                cursor.execute(drop_statement)

            # Create tables
            for create_statement in create_statements:
                cursor.execute(create_statement)

            conn.commit()
    except sqlite3.Error as e:
        print(e)


def populate_database():
    insert_statements = [
        """INSERT INTO Patients (id, firstname, lastname, age, sex, tumor_type, last_checkup)
           VALUES (?, ?, ?, ?, ?, ?, ?);""",
        """INSERT INTO TumorTypeMapping (TumorType, Category)
           VALUES (?, ?);""",
        """INSERT INTO Doctors (id, firstname, lastname, email, role, doctor_type, successful_operations)
           VALUES (?, ?, ?, ?, ?, ?, ?);""",
        """INSERT INTO DoctorsPatients (DoctorID, PatientID)
           VALUES (?, ?);""",
        """INSERT INTO DoctorsUsers (DoctorID, Username, Password)
           VALUES (?, ?, ?);"""
    ]

    data = [
        # Patients data
        [('1', 'John', 'Doe', 30, 'm', 'Glioma', '2023-01-01'),
         ('2', 'Jane', 'Smith', 25, 'f', 'Meningioma', '2023-02-15'),
         ('3', 'Alice', 'Johnson', 40, 'f', 'Normal_l', None),
         ('4', 'Bob', 'Brown', 35, 'm', 'Adenoma', '2023-03-20'),
         ('5', 'Charlie', 'White', 45, 'm', 'Glioma', '2023-04-30'),
         ('6', 'Douglas', 'Higgins', 50, 'm', 'Meningioma', '2023-05-15'),
         ('7', 'Eve', 'Black', 55, 'f', 'Normal_l', None),
         ('8', 'Frank', 'Green', 60, 'm', 'Adenoma', '2023-06-20'),
         ('9', 'Grace', 'Blue', 65, 'f', 'Glioma', '2023-07-30'),
         ('10', 'Hank', 'Red', 70, 'm', 'Meningioma', '2023-08-15'),
         ('11', 'Ivy', 'Yellow', 75, 'f', 'Normal_l', None),
         ('12', 'Jack', 'Orange', 80, 'm', 'Adenoma', '2023-09-20'),
         ('13', 'Kelly', 'Purple', 85, 'f', 'Glioma', '2023-10-30'),
         ('14', 'Liam', 'Pink', 90, 'm', 'Meningioma', '2023-11-15'),
         ('15', 'Mia', 'Cyan', 22, 'f', 'Normal_l', None),
         ('16', 'Noah', 'Magenta', 44, 'm', 'Adenoma', '2023-12-20'),
         ('17', 'Olivia', 'Lime', 20, 'f', 'Glioma', '2024-01-30'),
         ('18', 'Paul', 'Teal', 67, 'm', 'Meningioma', '2024-02-15'),
         ('19', 'Quinn', 'Grey', 50, 'm', 'Adenocarcinoma', '2024-03-01'),
         ('20', 'Riley', 'Black', 55, 'f', 'Large cell carcinoma', '2024-03-02'),
         ('21', 'Sawyer', 'Green', 60, 'm', 'Normal_b', None),
         ('22', 'Taylor', 'Blue', 65, 'm', 'Squamous cell carcinoma', '2024-03-03'),
         ('23', 'Parker', 'Yellow', 70, 'm', 'Adenocarcinoma', '2024-03-04'),
         ('24', 'Morgan', 'Orange', 75, 'm', 'Large cell carcinoma', '2024-03-05'),
         ('25', 'Alex', 'Red', 62, 'f', 'Normal_b', None),
         ('26', 'Jordan', 'Purple', 85, 'm', 'Squamous cell carcinoma', '2024-03-06'),
         ('27', 'Avery', 'Pink', 30, 'f', 'Adenocarcinoma', '2024-03-07'),
         ('28', 'Casey', 'Teal', 56, 'm', 'Large cell carcinoma', '2024-03-08'),
         ('29', 'Skyler', 'Cyan', 33, 'f', 'Normal_b', None),
         ('30', 'Jamie', 'Magenta', 25, 'm', 'Squamous cell carcinoma', '2024-03-09')],

        # TumorTypeMapping data
        [('Adenocarcinoma', 'Lung'),
         ('Large cell carcinoma', 'Lung'),
         ('Squamous cell carcinoma', 'Lung'),
         ('Normal_l', 'Lung'),
         ('Glioma', 'Brain'),
         ('Meningioma', 'Brain'),
         ('Adenoma', 'Brain'),
         ('Normal_b', 'Brain')],

        # Doctors data
        [('1', 'Dr. Michael', 'Smith', 'mich.smith@tumorsense.com', 'neurosurgeon', 'brain', 50),
         ('2', 'Dr. Emily', 'Johnson', 'emm.j@tumorsense.com', 'neurologist', 'brain', 200),
         ('3', 'Dr. William', 'Brown', 'wb@tumorsense.com', 'oncologist', 'brain', 100),
         ('4', 'Dr. Olivia', 'White', 'olw@tumorsense.com', 'radiologist', 'brain', 150),
         ('5', 'Dr. James', 'Black', 'jb@tumorsense.com', 'neurosurgeon', 'brain', 75),
         ('6', 'Dr. Sophia', 'Lee', 'sophia.lee@tumorsense.com', 'pulmonologist', 'lung', 120),
         ('7', 'Dr. Benjamin', 'Clark', 'ben.clark@tumorsense.com', 'thoracic surgeon', 'lung', 90),
         ('8', 'Dr. Ava', 'Martinez', 'ava.martinez@tumorsense.com', 'respiratory therapist', 'lung', 60)],

        # DoctorsPatients data
        [('1', '1'), ('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('1', '6'), ('1', '11'), ('1', '12'), ('1', '21'), ('1', '22'),
         ('2', '13'), ('2', '14'), ('2', '23'), ('2', '24'), ('2', '25'), ('2', '26'), ('2', '30'),
         ('3', '5'), ('3', '6'), ('3', '15'), ('3', '16'), ('3', '25'), ('3', '26'),
         ('4', '7'), ('4', '8'), ('4', '17'), ('4', '18'), ('4', '27'), ('4', '28'),
         ('5', '9'), ('5', '10'), ('5', '19'), ('5', '20'), ('5', '29'), ('5', '30'),
         ('6', '3'), ('6', '4'), ('6', '5'), ('6', '6'), ('6', '9'), ('6', '10'), ('6', '15'), ('6', '16'), ('6', '21'), ('6', '22'),
         ('7', '19'), ('7', '20'), ('7', '25'), ('7', '26'), ('7', '29'), ('7', '30'),
         ('8', '21'), ('8', '22'), ('8', '27'), ('8', '28')],

        # DoctorsUsers data
        [('1', 'msmith', 'pwd1'),
         ('2', 'ejohnson', 'pwd2'),
         ('3', 'wbrown', 'pwd3'),
         ('4', 'owhite', 'pwd4'),
         ('5', 'jblack', 'pwd5'),
         ('6', 'slee', 'pwd5'),
         ('7', 'bjmen', 'pwd5'),
         ('8', 'ava', 'pwd5')]
    ]

    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            for idx, insert_statement in enumerate(insert_statements):
                cursor.executemany(insert_statement, data[idx])
            conn.commit()
    except sqlite3.Error as e:
        print(e)



if __name__ == '__main__':
    create_sqlite_database("database.db")
    create_tables()
    populate_database()
