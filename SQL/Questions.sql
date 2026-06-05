
//Everything PostgreSQL and Metabase.//

//Metabase Questions//

//1. Poor Performers://

SELECT * FROM performance_reviews WHERE rating < 3;

//2. Resignations://

select e.*, t.termination_date  
FROM turnover t
JOIN employees e
ON t.employee_id = e.employee_id
WHERE t.reason = 'Better offer' OR t.reason = 'Career change' OR t.reason = 'Relocation'

//3. Training required//

SELECT * FROM training_records WHERE score IS NULL OR score <=60;