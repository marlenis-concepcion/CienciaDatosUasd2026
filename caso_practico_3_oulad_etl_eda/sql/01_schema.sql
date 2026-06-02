CREATE SCHEMA IF NOT EXISTS oulad;
SET search_path TO oulad;

CREATE TABLE IF NOT EXISTS courses (
    code_module VARCHAR(10) NOT NULL,
    code_presentation VARCHAR(10) NOT NULL,
    module_presentation_length INTEGER NOT NULL,
    PRIMARY KEY (code_module, code_presentation),
    CHECK (module_presentation_length > 0)
);

CREATE TABLE IF NOT EXISTS assessments (
    code_module VARCHAR(10) NOT NULL,
    code_presentation VARCHAR(10) NOT NULL,
    id_assessment INTEGER NOT NULL PRIMARY KEY,
    assessment_type VARCHAR(10) NOT NULL,
    date INTEGER,
    weight NUMERIC(5,2) NOT NULL,
    FOREIGN KEY (code_module, code_presentation)
        REFERENCES courses (code_module, code_presentation),
    CHECK (assessment_type IN ('TMA', 'CMA', 'Exam')),
    CHECK (weight >= 0 AND weight <= 100)
);

CREATE TABLE IF NOT EXISTS student_info (
    code_module VARCHAR(10) NOT NULL,
    code_presentation VARCHAR(10) NOT NULL,
    id_student INTEGER NOT NULL,
    gender CHAR(1) NOT NULL,
    region VARCHAR(80) NOT NULL,
    highest_education VARCHAR(80) NOT NULL,
    imd_band VARCHAR(20),
    age_band VARCHAR(20) NOT NULL,
    num_of_prev_attempts INTEGER NOT NULL,
    studied_credits INTEGER NOT NULL,
    disability CHAR(1) NOT NULL,
    final_result VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_student, code_module, code_presentation),
    FOREIGN KEY (code_module, code_presentation)
        REFERENCES courses (code_module, code_presentation),
    CHECK (gender IN ('M', 'F')),
    CHECK (disability IN ('Y', 'N')),
    CHECK (final_result IN ('Pass', 'Fail', 'Withdrawn', 'Distinction')),
    CHECK (num_of_prev_attempts >= 0),
    CHECK (studied_credits > 0)
);

CREATE TABLE IF NOT EXISTS student_registration (
    code_module VARCHAR(10) NOT NULL,
    code_presentation VARCHAR(10) NOT NULL,
    id_student INTEGER NOT NULL,
    date_registration INTEGER,
    date_unregistration INTEGER,
    PRIMARY KEY (id_student, code_module, code_presentation),
    FOREIGN KEY (id_student, code_module, code_presentation)
        REFERENCES student_info (id_student, code_module, code_presentation),
    CHECK (date_unregistration IS NULL OR date_registration IS NULL OR date_unregistration >= date_registration)
);

CREATE TABLE IF NOT EXISTS vle (
    id_site INTEGER NOT NULL PRIMARY KEY,
    code_module VARCHAR(10) NOT NULL,
    code_presentation VARCHAR(10) NOT NULL,
    activity_type VARCHAR(80) NOT NULL,
    week_from INTEGER,
    week_to INTEGER,
    FOREIGN KEY (code_module, code_presentation)
        REFERENCES courses (code_module, code_presentation),
    CHECK (week_to IS NULL OR week_from IS NULL OR week_to >= week_from)
);

CREATE TABLE IF NOT EXISTS student_assessment (
    id_assessment INTEGER NOT NULL,
    id_student INTEGER NOT NULL,
    date_submitted INTEGER,
    is_banked INTEGER NOT NULL,
    score NUMERIC(5,2),
    PRIMARY KEY (id_assessment, id_student),
    FOREIGN KEY (id_assessment) REFERENCES assessments (id_assessment),
    CHECK (is_banked IN (0, 1)),
    CHECK (score IS NULL OR score BETWEEN 0 AND 100)
);

CREATE TABLE IF NOT EXISTS student_vle (
    code_module VARCHAR(10) NOT NULL,
    code_presentation VARCHAR(10) NOT NULL,
    id_student INTEGER NOT NULL,
    id_site INTEGER NOT NULL,
    date INTEGER NOT NULL,
    sum_click INTEGER NOT NULL,
    PRIMARY KEY (code_module, code_presentation, id_student, id_site, date),
    FOREIGN KEY (id_student, code_module, code_presentation)
        REFERENCES student_info (id_student, code_module, code_presentation),
    FOREIGN KEY (id_site) REFERENCES vle (id_site),
    CHECK (sum_click >= 0)
);

