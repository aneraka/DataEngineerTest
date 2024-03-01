SELECT 
    a.id,
    a.department_id,
    a.job_id,
    a.name,
    a.datetime,
    b.job,c.department 
FROM data.hired_employees a
LEFT JOIN data.get_jobs b ON (a.job_id = b.id)
LEFT JOIN data.get_department c ON (a.department_id = c.id)