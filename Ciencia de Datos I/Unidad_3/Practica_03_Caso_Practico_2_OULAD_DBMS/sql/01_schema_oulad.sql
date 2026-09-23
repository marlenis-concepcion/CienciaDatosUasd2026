-- OULAD Database Schema for PostgreSQL
-- Open University Learning Analytics Dataset
-- Created for: Ciencia de Datos I - UASD
-- Date: 2026-06-14

-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- DIMENSION TABLES (Gradual loading with ordinal encoding)
-- ============================================================================

-- Courses/Modules dimension
CREATE TABLE IF NOT EXISTS courses (
    code_module VARCHAR(10) PRIMARY KEY,
    code_presentation VARCHAR(10) NOT NULL,
    module_presentation_length INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_courses_presentation ON courses(code_presentation);

-- Module details with ordinal encoding
CREATE TABLE IF NOT EXISTS modules (
    code_module VARCHAR(10) PRIMARY KEY,
    module_name VARCHAR(255) NOT NULL,
    module_ordinal SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (code_module) REFERENCES courses(code_module) ON DELETE CASCADE
);

-- Assessments/Evaluations table
CREATE TABLE IF NOT EXISTS assessments (
    id_assessment INTEGER PRIMARY KEY,
    code_module VARCHAR(10) NOT NULL,
    id_type VARCHAR(10) NOT NULL,
    assessment_type VARCHAR(50) NOT NULL,
    assessment_type_ordinal SMALLINT,
    date INTEGER NOT NULL,
    weight NUMERIC(5, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (code_module) REFERENCES courses(code_module) ON DELETE CASCADE
);

CREATE INDEX idx_assessments_module ON assessments(code_module);
CREATE INDEX idx_assessments_type ON assessments(assessment_type);

-- VLE (Virtual Learning Environment) resources table
CREATE TABLE IF NOT EXISTS vle (
    id_site INTEGER PRIMARY KEY,
    code_module VARCHAR(10) NOT NULL,
    id_week INTEGER NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    activity_type_ordinal SMALLINT,
    week_from INTEGER,
    week_to INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (code_module) REFERENCES courses(code_module) ON DELETE CASCADE
);

CREATE INDEX idx_vle_module ON vle(code_module);
CREATE INDEX idx_vle_week ON vle(id_week);
CREATE INDEX idx_vle_activity ON vle(activity_type);

-- ============================================================================
-- FACT TABLES (Student interactions and outcomes)
-- ============================================================================

-- Student Information (demographics and academic history)
CREATE TABLE IF NOT EXISTS student_info (
    id_student INTEGER NOT NULL,
    code_module VARCHAR(10) NOT NULL,
    code_presentation VARCHAR(10) NOT NULL,
    gender CHAR(1),
    gender_ordinal SMALLINT,
    region VARCHAR(100),
    region_ordinal SMALLINT,
    highest_education VARCHAR(50),
    highest_education_ordinal SMALLINT,
    imd_band VARCHAR(50),
    imd_band_ordinal SMALLINT,
    imd_midpoint NUMERIC(5, 2),
    age_band VARCHAR(50),
    age_band_ordinal SMALLINT,
    num_of_prev_attempts INTEGER,
    studied_credits INTEGER,
    disability VARCHAR(10),
    disability_ordinal SMALLINT,
    final_result VARCHAR(50),
    final_result_ordinal SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_student, code_module, code_presentation),
    FOREIGN KEY (code_module) REFERENCES courses(code_module) ON DELETE CASCADE
);

CREATE INDEX idx_student_info_module ON student_info(code_module);
CREATE INDEX idx_student_info_result ON student_info(final_result);
CREATE INDEX idx_student_info_gender ON student_info(gender);

-- Student Assessments (grades on evaluations)
CREATE TABLE IF NOT EXISTS student_assessment (
    id_assessment INTEGER NOT NULL,
    id_student INTEGER NOT NULL,
    date_submitted INTEGER NOT NULL,
    is_banked SMALLINT,
    score NUMERIC(5, 2),
    score_ordinal SMALLINT,
    score_category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_assessment, id_student),
    FOREIGN KEY (id_assessment) REFERENCES assessments(id_assessment) ON DELETE CASCADE,
    FOREIGN KEY (id_student) REFERENCES student_info(id_student) ON DELETE CASCADE
);

CREATE INDEX idx_student_assessment_student ON student_assessment(id_student);
CREATE INDEX idx_student_assessment_date ON student_assessment(date_submitted);
CREATE INDEX idx_student_assessment_score ON student_assessment(score);

-- Student VLE interactions (click-stream data)
CREATE TABLE IF NOT EXISTS student_vle (
    id_site INTEGER NOT NULL,
    id_student INTEGER NOT NULL,
    date INTEGER NOT NULL,
    sum_click INTEGER NOT NULL,
    sum_click_ordinal SMALLINT,
    click_category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_site, id_student, date),
    FOREIGN KEY (id_site) REFERENCES vle(id_site) ON DELETE CASCADE,
    FOREIGN KEY (id_student) REFERENCES student_info(id_student) ON DELETE CASCADE
);

CREATE INDEX idx_student_vle_student ON student_vle(id_student);
CREATE INDEX idx_student_vle_date ON student_vle(date);
CREATE INDEX idx_student_vle_site ON student_vle(id_site);

-- ============================================================================
-- DERIVED/AGGREGATED TABLES (For EDA and FullDomain)
-- ============================================================================

-- FullDomain for Student Assessment details
CREATE TABLE IF NOT EXISTS fulldomaine_assessment (
    id_fulldomaine_assessment BIGSERIAL PRIMARY KEY,
    id_student INTEGER NOT NULL,
    id_assessment INTEGER NOT NULL,
    code_module VARCHAR(10) NOT NULL,
    assessment_type VARCHAR(50),
    assessment_weight NUMERIC(5, 2),
    student_score NUMERIC(5, 2),
    score_ordinal SMALLINT,
    score_performance VARCHAR(50),
    date_submitted INTEGER,
    days_to_deadline INTEGER,
    is_banked SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_student) REFERENCES student_info(id_student) ON DELETE CASCADE,
    FOREIGN KEY (id_assessment) REFERENCES assessments(id_assessment) ON DELETE CASCADE,
    FOREIGN KEY (code_module) REFERENCES courses(code_module) ON DELETE CASCADE
);

CREATE INDEX idx_fulldomaine_assessment_student ON fulldomaine_assessment(id_student);
CREATE INDEX idx_fulldomaine_assessment_module ON fulldomaine_assessment(code_module);
CREATE INDEX idx_fulldomaine_assessment_performance ON fulldomaine_assessment(score_performance);

-- FullDomain for Student VLE interactions (aggregated level)
CREATE TABLE IF NOT EXISTS fulldomaine_vle (
    id_fulldomaine_vle BIGSERIAL PRIMARY KEY,
    id_student INTEGER NOT NULL,
    id_site INTEGER NOT NULL,
    code_module VARCHAR(10) NOT NULL,
    activity_type VARCHAR(50),
    date_accessed INTEGER,
    week_accessed SMALLINT,
    total_clicks INTEGER,
    click_ordinal SMALLINT,
    engagement_level VARCHAR(50),
    is_first_14_days SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_student) REFERENCES student_info(id_student) ON DELETE CASCADE,
    FOREIGN KEY (id_site) REFERENCES vle(id_site) ON DELETE CASCADE,
    FOREIGN KEY (code_module) REFERENCES courses(code_module) ON DELETE CASCADE
);

CREATE INDEX idx_fulldomaine_vle_student ON fulldomaine_vle(id_student);
CREATE INDEX idx_fulldomaine_vle_module ON fulldomaine_vle(code_module);
CREATE INDEX idx_fulldomaine_vle_activity ON fulldomaine_vle(activity_type);
CREATE INDEX idx_fulldomaine_vle_engagement ON fulldomaine_vle(engagement_level);

-- Student progress summary (weekly aggregation)
CREATE TABLE IF NOT EXISTS student_progress_weekly (
    id_student INTEGER NOT NULL,
    code_module VARCHAR(10) NOT NULL,
    week_number SMALLINT NOT NULL,
    total_vle_clicks INTEGER,
    unique_vle_activities SMALLINT,
    assessment_submissions INTEGER,
    assessment_average_score NUMERIC(5, 2),
    engagement_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_student, code_module, week_number),
    FOREIGN KEY (id_student) REFERENCES student_info(id_student) ON DELETE CASCADE,
    FOREIGN KEY (code_module) REFERENCES courses(code_module) ON DELETE CASCADE
);

CREATE INDEX idx_progress_student ON student_progress_weekly(id_student);
CREATE INDEX idx_progress_module ON student_progress_weekly(code_module);
CREATE INDEX idx_progress_week ON student_progress_weekly(week_number);

-- ============================================================================
-- AUDIT AND METADATA TABLES
-- ============================================================================

CREATE TABLE IF NOT EXISTS data_load_log (
    id_load BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    records_loaded INTEGER,
    load_start TIMESTAMP,
    load_end TIMESTAMP,
    status VARCHAR(20),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data_quality_metrics (
    id_metric BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    metric_name VARCHAR(100),
    metric_value NUMERIC(10, 2),
    check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

CREATE OR REPLACE VIEW v_student_summary AS
SELECT
    si.id_student,
    si.code_module,
    si.gender,
    si.highest_education,
    si.age_band,
    si.num_of_prev_attempts,
    si.studied_credits,
    si.disability,
    si.final_result,
    COUNT(DISTINCT sa.id_assessment) as total_assessments,
    AVG(sa.score) as avg_assessment_score,
    COUNT(DISTINCT sv.id_site) as unique_vle_resources,
    SUM(sv.sum_click) as total_vle_clicks,
    si.created_at
FROM student_info si
LEFT JOIN student_assessment sa ON si.id_student = sa.id_student
LEFT JOIN student_vle sv ON si.id_student = sv.id_student
GROUP BY si.id_student, si.code_module, si.gender, si.highest_education,
         si.age_band, si.num_of_prev_attempts, si.studied_credits,
         si.disability, si.final_result, si.created_at;

CREATE OR REPLACE VIEW v_assessment_statistics AS
SELECT
    a.code_module,
    a.id_assessment,
    a.assessment_type,
    a.weight,
    COUNT(DISTINCT sa.id_student) as students_submitted,
    AVG(sa.score) as mean_score,
    STDDEV(sa.score) as stddev_score,
    MIN(sa.score) as min_score,
    MAX(sa.score) as max_score,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sa.score) as median_score
FROM assessments a
LEFT JOIN student_assessment sa ON a.id_assessment = sa.id_assessment
GROUP BY a.code_module, a.id_assessment, a.assessment_type, a.weight;

CREATE OR REPLACE VIEW v_vle_engagement AS
SELECT
    sv.id_student,
    sv.id_site,
    vle.code_module,
    vle.activity_type,
    COUNT(DISTINCT sv.date) as days_active,
    SUM(sv.sum_click) as total_clicks,
    AVG(sv.sum_click) as avg_clicks_per_day,
    MAX(sv.date) as last_access_date,
    MIN(sv.date) as first_access_date
FROM student_vle sv
JOIN vle ON sv.id_site = vle.id_site
GROUP BY sv.id_student, sv.id_site, vle.code_module, vle.activity_type;

-- ============================================================================
-- GRANT PERMISSIONS (if needed)
-- ============================================================================
-- GRANT ALL PRIVILEGES ON DATABASE oulad_uasd TO <username>;
-- GRANT USAGE ON SCHEMA public TO <username>;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <username>;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO <username>;

COMMIT;
