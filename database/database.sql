DROP TABLE IF EXISTS DoctorsPatients;
DROP TABLE IF EXISTS DoctorsUsers;
DROP TABLE IF EXISTS Patients;
DROP TABLE IF EXISTS Doctors;
DROP TABLE IF EXISTS TumorTypeMapping;

CREATE TABLE Patients (
    id TEXT PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    age INTEGER NOT NULL,
    sex TEXT NOT NULL,
    tumor_type TEXT,
    last_checkup TEXT
);

CREATE TABLE Doctors (
    id TEXT PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL,
    doctor_type TEXT NOT NULL,
    successful_operations INTEGER
);

CREATE TABLE DoctorsUsers (
    DoctorID TEXT PRIMARY KEY,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(id)
);

CREATE TABLE DoctorsPatients (
    DoctorID TEXT NOT NULL,
    PatientID TEXT NOT NULL,
    PRIMARY KEY (DoctorID, PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(id),
    FOREIGN KEY (PatientID) REFERENCES Patients(id)
);

CREATE TABLE TumorTypeMapping (
    TumorType TEXT PRIMARY KEY,
    Category TEXT NOT NULL
);


INSERT INTO Patients (id, firstname, lastname, age, sex, tumor_type, last_checkup)
VALUES
    ('1', 'John', 'Doe', 30, 'm', 'Glioma', '2023-01-01'),
    ('2', 'Jane', 'Smith', 25, 'f', 'Meningioma', '2023-02-15'),
    ('3', 'Alice', 'Johnson', 40, 'f', 'Normal_l', NULL),
    ('4', 'Bob', 'Brown', 35, 'm', 'Adenoma', '2023-03-20'),
    ('5', 'Charlie', 'White', 45, 'm', 'Glioma', '2023-04-30'),
    ('6', 'Douglas', 'Higgins', 50, 'm', 'Meningioma', '2023-05-15'),
    ('7', 'Eve', 'Black', 55, 'f', 'Normal_l', NULL),
    ('8', 'Frank', 'Green', 60, 'm', 'Adenoma', '2023-06-20'),
    ('9', 'Grace', 'Blue', 65, 'f', 'Glioma', '2023-07-30'),
    ('10', 'Hank', 'Red', 70, 'm', 'Meningioma', '2023-08-15'),
    ('11', 'Ivy', 'Yellow', 75, 'f', 'Normal_l', NULL),
    ('12', 'Jack', 'Orange', 80, 'm', 'Adenoma', '2023-09-20'),
    ('13', 'Kelly', 'Purple', 85, 'f', 'Glioma', '2023-10-30'),
    ('14', 'Liam', 'Pink', 90, 'm', 'Meningioma', '2023-11-15'),
    ('15', 'Mia', 'Cyan', 22, 'f', 'Normal_l', NULL),
    ('16', 'Noah', 'Magenta', 44, 'm', 'Adenoma', '2023-12-20'),
    ('17', 'Olivia', 'Lime', 20, 'f', 'Glioma', '2024-01-30'),
    ('18', 'Paul', 'Teal', 67, 'm', 'Meningioma', '2024-02-15'),
    ('19', 'Quinn', 'Grey', 50, 'm', 'Adenocarcinoma', '2024-03-01'),
    ('20', 'Riley', 'Black', 55, 'f', 'Large cell carcinoma', '2024-03-02'),
    ('21', 'Sawyer', 'Green', 60, 'm', 'Normal_b', NULL),
    ('22', 'Taylor', 'Blue', 65, 'm', 'Squamous cell carcinoma', '2024-03-03'),
    ('23', 'Parker', 'Yellow', 70, 'm', 'Adenocarcinoma', '2024-03-04'),
    ('24', 'Morgan', 'Orange', 75, 'm', 'Large cell carcinoma', '2024-03-05'),
    ('25', 'Alex', 'Red', 62, 'f', 'Normal_b', NULL),
    ('26', 'Jordan', 'Purple', 85, 'm', 'Squamous cell carcinoma', '2024-03-06'),
    ('27', 'Avery', 'Pink', 30, 'f', 'Adenocarcinoma', '2024-03-07'),
    ('28', 'Casey', 'Teal', 56, 'm', 'Large cell carcinoma', '2024-03-08'),
    ('29', 'Skyler', 'Cyan', 33, 'f', 'Normal_b', NULL),
    ('30', 'Jamie', 'Magenta', 25, 'm', 'Squamous cell carcinoma', '2024-03-09'),
    ('31', 'Chris', 'Grey', 23, 'm', 'Glioma', '2024-01-15'),
    ('32', 'Lily', 'Green', 34, 'f', 'Meningioma', '2024-01-16'),
    ('33', 'Samuel', 'Brown', 42, 'm', 'Normal_l', NULL),
    ('34', 'Sophia', 'Black', 51, 'f', 'Adenoma', '2024-01-17'),
    ('35', 'Henry', 'White', 27, 'm', 'Glioma', '2024-01-18'),
    ('36', 'Isabella', 'Doe', 39, 'f', 'Meningioma', '2024-01-19'),
    ('37', 'Matthew', 'Smith', 49, 'm', 'Normal_l', NULL),
    ('38', 'Charlotte', 'Johnson', 53, 'f', 'Adenoma', '2024-01-20'),
    ('39', 'Daniel', 'Lee', 33, 'm', 'Glioma', '2024-01-21'),
    ('40', 'Olivia', 'Brown', 46, 'f', 'Meningioma', '2024-01-22'),
    ('41', 'Ethan', 'Green', 28, 'm', 'Normal_l', NULL),
    ('42', 'Emily', 'Blue', 36, 'f', 'Adenoma', '2024-01-23'),
    ('43', 'Lucas', 'Yellow', 44, 'm', 'Glioma', '2024-01-24'),
    ('44', 'Ava', 'Purple', 52, 'f', 'Meningioma', '2024-01-25'),
    ('45', 'Elijah', 'Red', 57, 'm', 'Normal_l', NULL),
    ('46', 'Amelia', 'Orange', 62, 'f', 'Adenoma', '2024-01-26'),
    ('47', 'Mason', 'Pink', 31, 'm', 'Glioma', '2024-01-27'),
    ('48', 'Harper', 'Teal', 47, 'f', 'Meningioma', '2024-01-28'),
    ('49', 'Logan', 'Grey', 56, 'm', 'Normal_l', NULL),
    ('50', 'Ella', 'Cyan', 64, 'f', 'Adenoma', '2024-01-29'),
    ('51', 'Jackson', 'Magenta', 24, 'm', 'Glioma', '2024-01-30'),
    ('52', 'Scarlett', 'Lime', 38, 'f', 'Meningioma', '2024-02-01'),
    ('53', 'Sebastian', 'Grey', 54, 'm', 'Normal_l', NULL),
    ('54', 'Grace', 'Green', 43, 'f', 'Adenoma', '2024-02-02'),
    ('55', 'Alexander', 'Brown', 50, 'm', 'Glioma', '2024-02-03'),
    ('56', 'Chloe', 'Black', 58, 'f', 'Meningioma', '2024-02-04'),
    ('57', 'Benjamin', 'White', 61, 'm', 'Normal_l', NULL),
    ('58', 'Lillian', 'Pink', 40, 'f', 'Adenoma', '2024-02-05'),
    ('59', 'James', 'Teal', 32, 'm', 'Glioma', '2024-02-06'),
    ('60', 'Victoria', 'Blue', 48, 'f', 'Meningioma', '2024-02-07');

INSERT INTO Doctors (id, firstname, lastname, email, role, doctor_type, successful_operations)
VALUES
    ('1', 'Dr. Michael', 'Smith', 'mich.smith@tumorsense.com', 'neurosurgeon', 'brain', 50),
    ('2', 'Dr. Emily', 'Johnson', 'emm.j@tumorsense.com', 'neurologist', 'brain', 200),
    ('3', 'Dr. William', 'Brown', 'wb@tumorsense.com', 'oncologist', 'brain', 100),
    ('4', 'Dr. Olivia', 'White', 'olw@tumorsense.com', 'radiologist', 'brain', 150),
    ('5', 'Dr. James', 'Black', 'jb@tumorsense.com', 'neurosurgeon', 'brain', 75),
    ('6', 'Dr. Sophia', 'Lee', 'sophia.lee@tumorsense.com', 'pulmonologist', 'lung', 120),
    ('7', 'Dr. Benjamin', 'Clark', 'ben.clark@tumorsense.com', 'thoracic surgeon', 'lung', 90),
    ('8', 'Dr. Ava', 'Martinez', 'ava.martinez@tumorsense.com', 'respiratory therapist', 'lung', 60);

INSERT INTO DoctorsUsers (DoctorID, Username, Password)
VALUES ('1', 'msmith', 'pwd1'),
       ('2', 'ejohnson', 'pwd2'),
       ('3', 'wbrown', 'pwd3'),
       ('4', 'owhite', 'pwd4'),
       ('5', 'jblack', 'pwd5'),
       ('6', 'slee', 'pwd5'),
       ('7', 'bjmen', 'pwd5'),
       ('8', 'ava', 'pwd5');

INSERT INTO DoctorsPatients (DoctorID, PatientID)
VALUES
    -- Brain specialists
    ('1', '1'), ('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('1', '6'),
    ('1', '11'), ('1', '12'), ('1', '21'),
    ('2', '13'), ('2', '14'), ('2', '23'), ('2', '24'), ('2', '25'),
    ('2', '26'), ('2', '30'),
    ('3', '5'), ('3', '6'), ('3', '15'), ('3', '16'), ('3', '25'),
    ('3', '26'),
    ('4', '7'), ('4', '8'), ('4', '17'), ('4', '18'), ('4', '27'),
    ('4', '28'),
    ('5', '9'), ('5', '10'), ('5', '19'), ('5', '20'), ('5', '29'),
    ('5', '30'),
    ('1', '31'), ('1', '32'), ('1', '33'), ('1', '34'), ('1', '35'),
    ('2', '36'), ('2', '37'), ('2', '38'), ('2', '39'), ('2', '40'),
    ('3', '41'), ('3', '42'), ('3', '43'), ('3', '44'), ('3', '45'),
    ('4', '46'), ('4', '47'), ('4', '48'), ('4', '49'), ('4', '50'),
    ('5', '51'), ('5', '52'), ('5', '53'), ('5', '54'), ('5', '55'),

    -- Lung specialists
    ('6', '3'), ('6', '4'), ('6', '5'), ('6', '6'), ('6', '9'),
    ('6', '10'), ('6', '15'), ('6', '16'), ('6', '21'), ('6', '22'),
    ('7', '19'), ('7', '20'), ('7', '25'), ('7', '26'), ('7', '29'),
    ('7', '30'),
    ('8', '21'), ('8', '22'), ('8', '27'), ('8', '28'),
    ('6', '56'), ('6', '57'), ('6', '58'), ('6', '59'), ('6', '60'),
    ('7', '41'), ('7', '42'), ('7', '43'), ('7', '44'), ('7', '45'),
    ('8', '46'), ('8', '47'), ('8', '48'), ('8', '49'), ('8', '50');

INSERT INTO TumorTypeMapping (TumorType, Category)
VALUES
        ('Adenocarcinoma', 'Lung'),
       ('Large cell carcinoma', 'Lung'),
       ('Squamous cell carcinoma', 'Lung'),
       ('Normal_l', 'Lung'),
       ('Glioma', 'Brain'),
       ('Meningioma', 'Brain'),
       ('Adenoma', 'Brain'),
       ('Normal_b', 'Brain');
