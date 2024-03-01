SELECT 
    department_id,
    department,
    hired
FROM (
    SELECT  
        a.department_id,
        c.department, 
        count(a.id) AS hired 
    FROM data.hired_employees a
    LEFT JOIN data.get_department c ON (a.department_id = c.id)
    WHERE extract(YEAR FROM cast(datetime AS timestamp)) = {year}
    group by a.department_id,c.department
) AS a
JOIN (
    SELECT 
        avg(cantidad) AS mean 
    FROM (SELECT department_id,count(id) AS cantidad
        FROM data.hired_employees
        WHERE extract(YEAR FROM cast(datetime AS timestamp)) = {year}
    GROUP BY department_id) AS s
) AS b on (1=1)
WHERE hired >mean