
SELECT TOP (5) R.First_name + ' ' + R.Last_name as Researcher_name, R.Researcher_ID , COUNT(*) as number_of_projects
FROM Researcher$ AS R , WorksOnProject$ as W , Project$ as P
WHERE R.Researcher_ID=W.Researcher_ID 
AND R.Birth_date BETWEEN '1983-01-01' and '2024-01-01'
AND P.Project_ID= W.Project_ID
AND P.End_date BETWEEN '2022-12-31' and '3000-01-01'
GROUP BY R.Researcher_ID, R.First_name, R.Last_name
HAVING COUNT(*)> 0
ORDER BY -COUNT(*)