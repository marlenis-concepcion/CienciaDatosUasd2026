SET search_path TO oulad;

CREATE INDEX IF NOT EXISTS idx_student_info_result
ON student_info (final_result);

CREATE INDEX IF NOT EXISTS idx_student_vle_student_course
ON student_vle (id_student, code_module, code_presentation);

CREATE INDEX IF NOT EXISTS idx_student_assessment_student
ON student_assessment (id_student);

CREATE INDEX IF NOT EXISTS idx_assessments_course
ON assessments (code_module, code_presentation);

CREATE OR REPLACE VIEW vw_student_course_summary AS
SELECT
    si.id_student,
    si.code_module,
    si.code_presentation,
    si.final_result,
    COALESCE(SUM(sv.sum_click), 0) AS total_clicks,
    AVG(CASE WHEN a.id_assessment IS NOT NULL THEN sa.score END) AS avg_score,
    COUNT(DISTINCT CASE WHEN a.id_assessment IS NOT NULL THEN sa.id_assessment END) AS completed_assessments,
    sr.date_unregistration
FROM student_info si
LEFT JOIN student_vle sv
    ON si.id_student = sv.id_student
    AND si.code_module = sv.code_module
    AND si.code_presentation = sv.code_presentation
LEFT JOIN student_registration sr
    ON si.id_student = sr.id_student
    AND si.code_module = sr.code_module
    AND si.code_presentation = sr.code_presentation
LEFT JOIN student_assessment sa
    ON si.id_student = sa.id_student
LEFT JOIN assessments a
    ON sa.id_assessment = a.id_assessment
    AND si.code_module = a.code_module
    AND si.code_presentation = a.code_presentation
GROUP BY
    si.id_student,
    si.code_module,
    si.code_presentation,
    si.final_result,
    sr.date_unregistration;

CREATE OR REPLACE VIEW vw_course_performance AS
SELECT
    code_module,
    code_presentation,
    COUNT(*) AS students,
    COUNT(*) FILTER (WHERE final_result = 'Pass') AS passed,
    COUNT(*) FILTER (WHERE final_result = 'Fail') AS failed,
    COUNT(*) FILTER (WHERE final_result = 'Withdrawn') AS withdrawn,
    COUNT(*) FILTER (WHERE final_result = 'Distinction') AS distinction
FROM student_info
GROUP BY code_module, code_presentation;
