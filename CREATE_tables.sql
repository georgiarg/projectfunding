/* =====================
	CREATE DATABASE 
======================*/
USE [master]
GO

IF NOT EXISTS (SELECT name FROM master.dbo.sysdatabases 
WHERE name = 'ProjectFunding')
CREATE DATABASE [ProjectFunding] COLLATE Greek_CI_AI -- Collatiom : CI = Case Insensitive, AI = Accent Insensitive
GO

/* =====================
	CREATE ENTITIES 
======================*/
USE [ProjectFunding]
GO

IF OBJECT_ID ('Project', 'U') IS NULL
BEGIN
CREATE TABLE Project
(
	Project_ID int IDENTITY(1,1) PRIMARY KEY,
	Begin_date date not null,
	End_date date not null,
	Title varchar (100) not null,
	AmountofMoney float, 
	Summary varchar (500)
)
END
GO

IF OBJECT_ID ('Researcher', 'U') IS NULL
BEGIN
CREATE TABLE Researcher
(
	Researcher_ID int IDENTITY(1,1) PRIMARY KEY, 
	First_name varchar (50) not null,
	Last_name varchar (50) not null,
	Birth_date date, 
	Gender varchar (10) not null
)
END
GO

IF OBJECT_ID ('Stem', 'U') IS NULL
BEGIN
CREATE TABLE Stem
(
	Stem_ID int IDENTITY(1,1) PRIMARY KEY,
	Stem_name varchar (50) not null
)
END
GO

IF OBJECT_ID ('Program', 'U') IS NULL
BEGIN
CREATE TABLE Program
(
	Program_ID int IDENTITY(1,1) PRIMARY KEY,
	ProgramName varchar (50) not null,
	Program_address varchar (50)
)
END
GO

IF OBJECT_ID ('Evaluation', 'U') IS NULL
BEGIN
CREATE TABLE Evaluation
(
	Evaluation_ID int IDENTITY(1,1) PRIMARY KEY,
	Grade float,
	Evaluation_date date
)
END
GO

IF OBJECT_ID ('Scientific_field', 'U') IS NULL
BEGIN
CREATE TABLE Scientific_field
(
	Scientific_field_ID int IDENTITY(1,1) PRIMARY KEY,
	Scientific_field_name varchar (50) not null
)
END
GO

IF OBJECT_ID ('Deliverable', 'U') IS NULL
BEGIN
CREATE TABLE Deliverable
(
	Deliverable_ID int IDENTITY(1,1) PRIMARY KEY,
	Title varchar (50) not null,
	Summary varchar (50)
)
END
GO

IF OBJECT_ID ('Organization', 'U') IS NULL
BEGIN
CREATE TABLE Organization
(
	Organization_ID int IDENTITY(1,1) PRIMARY KEY,
	Abbreviation varchar (10),
	Organization_name varchar (50),
	Postcode int,
	Street varchar (50),
	City varchar (50)
)
END
GO


/* =====================
	CREATE ENTITY RELATIONS 
======================*/

IF OBJECT_ID ('Evaluates', 'U') IS NULL
BEGIN
CREATE TABLE Evaluates
(
	Evaluates_ID int IDENTITY(1,1) PRIMARY KEY,
	Evaluation_ID int FOREIGN KEY REFERENCES Evaluation(Evaluation_ID),
	Researcher_ID int FOREIGN KEY REFERENCES Researcher(Researcher_ID),
	Project_ID int FOREIGN KEY REFERENCES Project(Project_ID)
)
END
GO

IF OBJECT_ID ('Employee_Relation', 'U') IS NULL
BEGIN
CREATE TABLE Employee_Relation
(
	Employee_Relation_ID int IDENTITY(1,1) PRIMARY KEY,
	Researcher_ID int FOREIGN KEY REFERENCES Researcher(Researcher_ID),
	Organization_ID int FOREIGN KEY REFERENCES Organization(Organization_ID),
	Relation_date date
)
END
GO

IF OBJECT_ID ('WorksOnProject', 'U') IS NULL
BEGIN
CREATE TABLE WorksOnProject
(
	WorksOnProject_ID int IDENTITY(1,1) PRIMARY KEY,
	Project_ID int FOREIGN KEY REFERENCES Project(Project_ID),
	Researcher_ID int FOREIGN KEY REFERENCES Researcher(Researcher_ID)
)
END
GO

IF OBJECT_ID ('Delivery', 'U') IS NULL
BEGIN
CREATE TABLE Delivery
(
	Delivery_ID int IDENTITY(1,1) PRIMARY KEY,
	Deliverable_ID int FOREIGN KEY REFERENCES Deliverable(Deliverable_ID),
	Project_ID int FOREIGN KEY REFERENCES Project(Project_ID),
	Date_of_delivery date
)
END
GO

IF OBJECT_ID ('ProjectScientificField', 'U') IS NULL
BEGIN
CREATE TABLE ProjectScientificField
(
	ProjectScientificField_ID int IDENTITY(1,1) PRIMARY KEY,
	Scientific_field_ID int FOREIGN KEY REFERENCES Scientific_field(Scientific_field_ID),
	Project_ID int FOREIGN KEY REFERENCES Project(Project_ID)
)
END
GO

IF OBJECT_ID ('Organization_phones', 'U') IS NULL
BEGIN
CREATE TABLE Organization_phones
(
	Organization_phones_ID int IDENTITY(1,1) PRIMARY KEY,
	Organization_ID int FOREIGN KEY REFERENCES Organization(Organization_ID),
	Phone varchar (12)
)
END
GO

IF OBJECT_ID ('Research_center', 'U') IS NULL
BEGIN
CREATE TABLE Research_center
(
	Research_center_ID int IDENTITY(1,1) PRIMARY KEY,
	Organization_ID int FOREIGN KEY REFERENCES Organization(Organization_ID),
	MinistryofEducation_Budget float,
	PriavteActions_Budget float
)
END
GO


IF OBJECT_ID ('University', 'U') IS NULL
BEGIN
CREATE TABLE University
(
	University_ID int IDENTITY(1,1) PRIMARY KEY,
	Organization_ID int FOREIGN KEY REFERENCES Organization(Organization_ID),
	MinistryofEducation_Budget float
)
END
GO

IF OBJECT_ID ('Company', 'U') IS NULL
BEGIN
CREATE TABLE Company
(
	Company_ID int IDENTITY(1,1) PRIMARY KEY,
	Organization_ID int FOREIGN KEY REFERENCES Organization(Organization_ID),
	Equity float
)
END
GO

/* =====================
	ADD ALL FOREIGN KEYS (1-N relations)
======================*/
ALTER TABLE Project 
ADD Organization_ID int FOREIGN KEY REFERENCES Organization(Organization_ID)
GO

ALTER TABLE Project 
ADD Researcher_ID int FOREIGN KEY REFERENCES Researcher(Researcher_ID)
GO

ALTER TABLE Project
ADD Evaluation_ID int FOREIGN KEY REFERENCES Evaluation(Evaluation_ID)
GO

ALTER TABLE Project
ADD Stem_ID int FOREIGN KEY REFERENCES Stem(Stem_ID)
GO

ALTER TABLE Project
ADD Program_ID int FOREIGN KEY REFERENCES Program(Program_ID)
GO

