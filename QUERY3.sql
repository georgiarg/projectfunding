SELECT Project$.Project_ID, Project$.Title AS Project_Title
FROM Project$
INNER JOIN ProjectScientificField$ ON Project$.Project_ID = ProjectScientificField$.Project_ID
WHERE Scientific_field_ID = 527355 AND GETDATE() < Project$.End_date


SELECT Project$.Researcher_ID AS Researchers
FROM Project$
INNER JOIN Evaluates$ ON Project$.Project_ID = Evaluates$.Project_ID
RIGHT JOIN WorksOnProject$ ON WorksOnProject$.Project_ID = Project$.Project_ID
INNER JOIN ProjectScientificField$ ON Project$.Project_ID = ProjectScientificField$.Project_ID
WHERE Scientific_field_ID = 527355 AND GETDATE() < Project$.End_date
UNION 
SELECT Evaluates$.Researcher_ID
FROM Project$
INNER JOIN Evaluates$ ON Project$.Project_ID = Evaluates$.Project_ID
INNER JOIN Evaluation$ ON Evaluation$.Evaluation_ID = Evaluates$.Evaluation_ID
RIGHT JOIN WorksOnProject$ ON WorksOnProject$.Project_ID = Project$.Project_ID
INNER JOIN ProjectScientificField$ ON Project$.Project_ID = ProjectScientificField$.Project_ID
WHERE Scientific_field_ID = 527355 AND GETDATE() < Project$.End_date AND Evaluation$.Evaluation_date > DATEADD(year,-1,GETDATE())
UNION
SELECT  WorksOnProject$.Researcher_ID 
FROM Project$
INNER JOIN Evaluates$ ON Project$.Project_ID = Evaluates$.Project_ID
RIGHT JOIN WorksOnProject$ ON WorksOnProject$.Project_ID = Project$.Project_ID
INNER JOIN ProjectScientificField$ ON Project$.Project_ID = ProjectScientificField$.Project_ID
WHERE Scientific_field_ID = 527355 AND GETDATE() < Project$.End_date


