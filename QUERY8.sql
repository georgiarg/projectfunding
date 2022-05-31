SELECT R.First_name, R.Last_name, R.Researcher_ID, COUNT(*) as Number_of_projects
FROM Researcher$ as R, WorksOnProject$ as W
WHERE R.Researcher_ID=W.Researcher_ID
AND NOT EXISTS
(SELECT D.Project_ID
FROM DELIVERY as D
WHERE D.Project_ID=W.Project_ID
)
GROUP BY R.Researcher_ID, R.First_name, R.Last_name
HAVING COUNT(*)>4

