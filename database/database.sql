IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'DoctorsPatients')
    BEGIN
        DROP TABLE DoctorsPatients;
    END
GO

IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'DoctorsUsers')
    BEGIN
        DROP TABLE DoctorsUsers;
    END
GO

IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Patients')
    BEGIN
        DROP TABLE Patients;
    END
GO

IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Doctors')
    BEGIN
        DROP TABLE Doctors;
    END
GO

-- Create the table
CREATE TABLE [dbo].[Patients] (
    [id]           NVARCHAR (50) NOT NULL,
    [firstname]    NVARCHAR (50) NOT NULL,
    [lastname]     NVARCHAR (50) NOT NULL,
    [age]          INT           NOT NULL,
    [tumor_type]   NVARCHAR (50) NULL,
    [last_checkup] DATETIME      NULL,
    CONSTRAINT [PK_Patients] PRIMARY KEY CLUSTERED ([id] ASC)
);

CREATE TABLE [dbo].[Doctors] (
    [id]                    NVARCHAR (50) NOT NULL,
    [firstname]             NVARCHAR (50) NOT NULL,
    [lastname]              NVARCHAR (50) NOT NULL,
    [email]                 NVARCHAR (50) NOT NULL,
    [role]                  NVARCHAR (50) NOT NULL,
    [successful_operations] INT           NULL,
    CONSTRAINT [PK_Doctors] PRIMARY KEY CLUSTERED ([id] ASC)
);


CREATE TABLE [dbo].[DoctorsUsers] (
    DoctorID NVARCHAR(50) NOT NULL PRIMARY KEY,
    Username NVARCHAR(50) NOT NULL,
    [Password] NVARCHAR(50) NOT NULL
);
GO

CREATE TABLE [dbo].[DoctorsPatients] (
    DoctorID NVARCHAR(50) NOT NULL FOREIGN KEY REFERENCES Doctors(id),
    PatientID NVARCHAR(50) NOT NULL FOREIGN KEY REFERENCES Patients(id),
    PRIMARY KEY (DoctorID, PatientID)
);
GO

-- Populate database
INSERT INTO Patients (id, firstname, lastname, age, tumor_type, last_checkup)
VALUES
    ('1', 'John', 'Doe', 30, 'glioma', '2023-01-01'),
    ('2', 'Jane', 'Smith', 25, 'meningioma', '2023-02-15'),
    ('3', 'Alice', 'Johnson', 40, 'normal', NULL),
    ('4', 'Bob', 'Brown', 35, 'adenoma', '2023-03-20'),
    ('5', 'Charlie', 'White', 45, 'glioma', '2023-04-30'),
    ('6', 'Douglas', 'Higgins', 50, 'meningioma', '2023-05-15'),
    ('7', 'Eve', 'Black', 55, 'normal', NULL),
    ('8', 'Frank', 'Green', 60, 'adenoma', '2023-06-20'),
    ('9', 'Grace', 'Blue', 65, 'glioma', '2023-07-30'),
    ('10', 'Hank', 'Red', 70, 'meningioma', '2023-08-15'),
    ('11', 'Ivy', 'Yellow', 75, 'normal', NULL),
    ('12', 'Jack', 'Orange', 80, 'adenoma', '2023-09-20'),
    ('13', 'Kelly', 'Purple', 85, 'glioma', '2023-10-30'),
    ('14', 'Liam', 'Pink', 90, 'meningioma', '2023-11-15'),
    ('15', 'Mia', 'Cyan', 95, 'normal', NULL),
    ('16', 'Noah', 'Magenta', 100, 'adenoma', '2023-12-20'),
    ('17', 'Olivia', 'Lime', 105, 'glioma', '2024-01-30'),
    ('18', 'Paul', 'Teal', 110, 'meningioma', '2024-02-15');
GO

INSERT INTO Doctors(id, firstname, lastname, email, [role], successful_operations)
VALUES
    ('1', 'Dr. Michael', 'Smith', 'mich.smith@tumorsense.com', 'neurosurgeon', 50),
    ('2', 'Dr. Emily', 'Johnson', 'emm.j@tumorsense.com', 'neurologist', 200),
    ('3', 'Dr. William', 'Brown', 'wb@tumorsense.com', 'oncologist', 100),
    ('4', 'Dr. Olivia', 'White', 'olw@tumorsense.com', 'radiologist', 150),
    ('5', 'Dr. James', 'Black', 'jb@tumorsense.com', 'neurosurgeon', 75);
GO

INSERT INTO DoctorsPatients (DoctorID, PatientID)
VALUES
    ('1', '1'), -- Dr. Michael Smith is assigned to Patient 1
    ('1', '2'), -- Dr. Michael Smith is assigned to Patient 2
    ('2', '3'), -- Dr. Emily Johnson is assigned to Patient 3
    ('2', '4'), -- Dr. Emily Johnson is assigned to Patient 4
    ('3', '5'), -- Dr. William Brown is assigned to Patient 5
    ('3', '6'), -- Dr. William Brown is assigned to Patient 6
    ('4', '7'), -- Dr. Olivia White is assigned to Patient 7
    ('4', '8'), -- Dr. Olivia White is assigned to Patient 8
    ('5', '9'), -- Dr. James Black is assigned to Patient 9
    ('5', '10'); -- Dr. James Black is assigned to Patient 10

INSERT INTO DoctorsUsers (DoctorID, Username, [Password])
VALUES
    ('1', 'msmith', 'pwd1'),
    ('2', 'ejohnson', 'pwd2'),
    ('3', 'wbrown', 'pwd3'),
    ('4', 'owhite', 'pwd4'),
    ('5', 'jblack', 'pwd5');
GO