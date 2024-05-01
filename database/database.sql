IF EXISTS (SELECT 1
           FROM INFORMATION_SCHEMA.TABLES
           WHERE TABLE_NAME = 'DoctorsPatients')
    BEGIN
        DROP TABLE DoctorsPatients;
    END
GO

IF EXISTS (SELECT 1
           FROM INFORMATION_SCHEMA.TABLES
           WHERE TABLE_NAME = 'DoctorsUsers')
    BEGIN
        DROP TABLE DoctorsUsers;
    END
GO

IF EXISTS (SELECT 1
           FROM INFORMATION_SCHEMA.TABLES
           WHERE TABLE_NAME = 'Patients')
    BEGIN
        DROP TABLE Patients;
    END
GO

IF EXISTS (SELECT 1
           FROM INFORMATION_SCHEMA.TABLES
           WHERE TABLE_NAME = 'Doctors')
    BEGIN
        DROP TABLE Doctors;
    END
GO

IF EXISTS (SELECT 1
           FROM INFORMATION_SCHEMA.TABLES
           WHERE TABLE_NAME = 'TumorTypeMapping')
    BEGIN
        DROP TABLE TumorTypeMapping;
    END
GO

-- Create the table
CREATE TABLE [dbo].[Patients]
(
    [id]           NVARCHAR(50) NOT NULL,
    [firstname]    NVARCHAR(50) NOT NULL,
    [lastname]     NVARCHAR(50) NOT NULL,
    [age]          INT          NOT NULL,
    [sex]          NVARCHAR(1) NOT NULL,
    [tumor_type]   NVARCHAR(50) NULL,
    [last_checkup] DATETIME     NULL,
    CONSTRAINT [PK_Patients] PRIMARY KEY CLUSTERED ([id] ASC)
);

CREATE TABLE [dbo].[Doctors]
(
    [id]                    NVARCHAR(50) NOT NULL,
    [firstname]             NVARCHAR(50) NOT NULL,
    [lastname]              NVARCHAR(50) NOT NULL,
    [email]                 NVARCHAR(50) NOT NULL,
    [role]                  NVARCHAR(50) NOT NULL,
    [doctor_type]           NVARCHAR(50) NOT NULL,
    [successful_operations] INT          NULL,
    CONSTRAINT [PK_Doctors] PRIMARY KEY CLUSTERED ([id] ASC)
);


CREATE TABLE [dbo].[DoctorsUsers]
(
    DoctorID   NVARCHAR(50) NOT NULL PRIMARY KEY,
    Username   NVARCHAR(50) NOT NULL,
    [Password] NVARCHAR(50) NOT NULL
);
GO

CREATE TABLE [dbo].[DoctorsPatients]
(
    DoctorID  NVARCHAR(50) NOT NULL FOREIGN KEY REFERENCES Doctors (id),
    PatientID NVARCHAR(50) NOT NULL FOREIGN KEY REFERENCES Patients (id),
    PRIMARY KEY (DoctorID, PatientID)
);
GO

CREATE TABLE [dbo].[TumorTypeMapping]
(
    TumorType NVARCHAR(50) PRIMARY KEY,
    Category  NVARCHAR(50) NOT NULL
);
GO

-- Populate database
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
    ('30', 'Jamie', 'Magenta', 25, 'm', 'Squamous cell carcinoma', '2024-03-09');
GO

INSERT INTO TumorTypeMapping (TumorType, Category)
VALUES ('Adenocarcinoma', 'Lung'),
       ('Large cell carcinoma', 'Lung'),
       ('Squamous cell carcinoma', 'Lung'),
       ('Normal_l', 'Lung'),
       ('Glioma', 'Brain'),
       ('Meningioma', 'Brain'),
       ('Adenoma', 'Brain'),
       ('Normal_b', 'Brain');
GO

INSERT INTO Doctors(id, firstname, lastname, email, [role], doctor_type, successful_operations)
VALUES
    ('1', 'Dr. Michael', 'Smith', 'mich.smith@tumorsense.com', 'neurosurgeon', 'brain', 50),
    ('2', 'Dr. Emily', 'Johnson', 'emm.j@tumorsense.com', 'neurologist', 'brain', 200),
    ('3', 'Dr. William', 'Brown', 'wb@tumorsense.com', 'oncologist', 'brain', 100),
    ('4', 'Dr. Olivia', 'White', 'olw@tumorsense.com', 'radiologist', 'brain', 150),
    ('5', 'Dr. James', 'Black', 'jb@tumorsense.com', 'neurosurgeon', 'brain', 75),
    ('6', 'Dr. Sophia', 'Lee', 'sophia.lee@tumorsense.com', 'pulmonologist', 'lung', 120),
    ('7', 'Dr. Benjamin', 'Clark', 'ben.clark@tumorsense.com', 'thoracic surgeon', 'lung', 90),
    ('8', 'Dr. Ava', 'Martinez', 'ava.martinez@tumorsense.com', 'respiratory therapist', 'lung', 60);
GO


-- Assign patients to doctors based on doctor type
INSERT INTO DoctorsPatients (DoctorID, PatientID)
VALUES
    -- Brain specialists
    ('1', '1'), ('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('1', '6'), ('1', '11'), ('1', '12'), ('1', '21'), ('1', '22'),
    ('2', '13'), ('2', '14'), ('2', '23'), ('2', '24'), ('2', '25'), ('2', '26'), ('2', '30'),
    ('3', '5'), ('3', '6'), ('3', '15'), ('3', '16'), ('3', '25'), ('3', '26'),
    ('4', '7'), ('4', '8'), ('4', '17'), ('4', '18'), ('4', '27'), ('4', '28'),
    ('5', '9'), ('5', '10'), ('5', '19'), ('5', '20'), ('5', '29'), ('5', '30'),
    -- Lung specialists
    ('6', '3'), ('6', '4'), ('6', '5'), ('6', '6'), ('6', '9'), ('6', '10'), ('6', '15'), ('6', '16'), ('6', '21'), ('6', '22'),
    ('7', '19'), ('7', '20'), ('7', '25'), ('7', '26'), ('7', '29'), ('7', '30'),
    ('8', '21'), ('8', '22'), ('8', '27'), ('8', '28');


INSERT INTO DoctorsUsers (DoctorID, Username, [Password])
VALUES ('1', 'msmith', 'pwd1'),
       ('2', 'ejohnson', 'pwd2'),
       ('3', 'wbrown', 'pwd3'),
       ('4', 'owhite', 'pwd4'),
       ('5', 'jblack', 'pwd5'),
       ('6', 'slee', 'pwd5'),
       ('7', 'bjmen', 'pwd5'),
       ('8', 'ava', 'pwd5');
GO
