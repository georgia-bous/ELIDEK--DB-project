create database elidek;
use elidek;

CREATE TABLE Executive(
executive_id INT UNSIGNED AUTO_INCREMENT,
    surname VARCHAR(20) NOT NULL,
    forename VARCHAR(15) NOT NULL,
    PRIMARY KEY(executive_id)

);

CREATE TABLE Scientific_field(
field_id INT UNSIGNED AUTO_INCREMENT,
    field_name VARCHAR(30) NOT NULL,
    field_description VARCHAR(100) NOT NULL,
PRIMARY KEY(field_id)
);


CREATE TABLE Program(
program_id INT UNSIGNED AUTO_INCREMENT,
program_name VARCHAR(30) NOT NULL,
    management  VARCHAR(25) NOT NULL,
PRIMARY KEY(program_id)

);


CREATE TABLE Organization(
organization_id INT UNSIGNED AUTO_INCREMENT,
    organization_name VARCHAR(25) NOT NULL,
    abbreviation VARCHAR(7) NOT NULL,
    street_name VARCHAR(15) NOT NULL,
    street_number INT NOT NULL,
    postal_code INT NOT NULL,
    city VARCHAR(20) NOT NULL,
    organization_type ENUM ('Company','University', 'Research Facility') NOT NULL,
PRIMARY KEY(organization_id)
   
);

CREATE TABLE Organization_contact_number(
organization_id INT UNSIGNED ,
    organization_number BIGINT UNSIGNED,
    PRIMARY KEY(organization_id, organization_number),
    CONSTRAINT fk_contact_organization FOREIGN KEY(organization_id) REFERENCES Organization(organization_id) ON DELETE CASCADE
);


CREATE TABLE Researcher(
researcher_id INT UNSIGNED AUTO_INCREMENT,
    organization_id INT UNSIGNED,
    forename VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    sex ENUM('Male', 'Female', 'Non-Binary') NOT NULL,
    birthdate DATE NOT NULL,
    starting_work_day DATE NOT NULL,
    PRIMARY KEY(researcher_id),
    CONSTRAINT fk_researcher_organization FOREIGN KEY(organization_id) REFERENCES Organization(organization_id) ON DELETE SET NULL
);


CREATE TABLE Project(
project_id INT UNSIGNED AUTO_INCREMENT,
    title VARCHAR(30) NOT NULL,
    summary VARCHAR(200),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    funding DOUBLE NOT NULL,
    evaluation_date DATE NOT NULL,
    grade FLOAT,
    organization_id INT UNSIGNED,
    program_id INT UNSIGNED,
    executive_id INT UNSIGNED,
    supervisor_id INT UNSIGNED,
    evaluator_id INT UNSIGNED,
    PRIMARY KEY(project_id),
    CONSTRAINT fk_project_program FOREIGN KEY(program_id) REFERENCES Program(program_id) ON DELETE SET NULL,
    CONSTRAINT fk_project_executive FOREIGN KEY(executive_id) REFERENCES Executive(executive_id) ON DELETE SET NULL,
    CONSTRAINT fk_project_evaluator FOREIGN KEY(evaluator_id) REFERENCES Researcher(researcher_id) ON DELETE SET NULL,
    CONSTRAINT fk_project_supervisor FOREIGN KEY(supervisor_id) REFERENCES Researcher(researcher_id) ON DELETE SET NULL,
    CONSTRAINT fk_project_organization FOREIGN KEY(organization_id) REFERENCES Organization(organization_id) ON DELETE SET NULL,
CONSTRAINT check_project_date CHECK(DATEDIFF(end_date, start_date) >= 365 AND DATEDIFF(end_date,start_date) <= 1460)
);


CREATE TABLE Field_of_project(
project_id INT UNSIGNED,
    field_id INT UNSIGNED,
    PRIMARY KEY(project_id, field_id),
    CONSTRAINT fk_field_project FOREIGN KEY(project_id) REFERENCES Project(project_id) ON DELETE CASCADE,
    CONSTRAINT fk_field_scientific FOREIGN KEY(field_id) REFERENCES Scientific_field(field_id)  ON DELETE CASCADE

);


CREATE TABLE Deliverable(
title VARCHAR(35),
    summary VARCHAR(100) NOT NULL,
    delivery_date DATE NOT NULL,
    project_id INT UNSIGNED,
    PRIMARY KEY(project_id, title),
    CONSTRAINT fk_deliverable_project FOREIGN KEY(project_id) REFERENCES Project(project_id) ON DELETE CASCADE
);

CREATE TABLE Works_in(
project_id INT UNSIGNED,
    researcher_id INT UNSIGNED ,
    PRIMARY KEY(project_id, researcher_id),
    CONSTRAINT fk_works_in_project FOREIGN KEY(project_id) REFERENCES Project(project_id) ON DELETE CASCADE,
    CONSTRAINT fk_works_in_researcher FOREIGN KEY(researcher_id) REFERENCES Researcher(researcher_id) ON DELETE CASCADE
);


CREATE INDEX project_start_date_idx
ON Project (start_date);

CREATE INDEX project_end_date_idx
ON Project (end_date);

CREATE INDEX researcher_birthdate_idx
ON Researcher (birthdate);


DELIMITER $$
CREATE TRIGGER res_trigg
BEFORE INSERT ON Works_in
FOR EACH ROW
BEGIN
IF EXISTS(SELECT
Project.project_id, Works_in.researcher_id FROM Project JOIN Works_in ON NEW.project_id = Project.project_id AND NEW.researcher_id = Project.evaluator_id
)
THEN SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'An evaluator cannot be working in the project he is evaluating';
END IF;
END
DELIMITER ;


