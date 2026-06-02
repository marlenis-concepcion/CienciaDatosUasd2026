SET search_path TO oulad;

SELECT 'courses' AS table_name, COUNT(*) AS rows_loaded FROM courses
UNION ALL
SELECT 'assessments', COUNT(*) FROM assessments
UNION ALL
SELECT 'student_info', COUNT(*) FROM student_info
UNION ALL
SELECT 'student_registration', COUNT(*) FROM student_registration
UNION ALL
SELECT 'vle', COUNT(*) FROM vle
UNION ALL
SELECT 'student_assessment', COUNT(*) FROM student_assessment
UNION ALL
SELECT 'student_vle', COUNT(*) FROM student_vle;

SELECT code_module, code_presentation, id_student, COUNT(*) AS duplicate_count
FROM student_info
GROUP BY code_module, code_presentation, id_student
HAVING COUNT(*) > 1;

SELECT final_result, COUNT(*) AS total
FROM student_info
GROUP BY final_result
ORDER BY total DESC;

SELECT code_module, code_presentation, AVG(total_clicks) AS avg_clicks
FROM vw_student_course_summary
GROUP BY code_module, code_presentation
ORDER BY code_module, code_presentation;

