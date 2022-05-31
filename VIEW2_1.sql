CREATE VIEW [Projects per Researcher] AS
SELECT Project$.Project_ID, Project$.Researcher_ID AS Researchers
FROM Project$
INNER JOIN Evaluates$ ON Project$.Project_ID = Evaluates$.Project_ID
RIGHT JOIN WorksOnProject$ ON WorksOnProject$.Project_ID = Project$.Project_ID
UNION
SELECT Project$.Project_ID, Evaluates$.Researcher_ID 
FROM Project$
INNER JOIN Evaluates$ ON Project$.Project_ID = Evaluates$.Project_ID
RIGHT JOIN WorksOnProject$ ON WorksOnProject$.Project_ID = Project$.Project_ID
UNION 
SELECT Project$.Project_ID, WorksOnProject$.Researcher_ID 
FROM Project$
INNER JOIN Evaluates$ ON Project$.Project_ID = Evaluates$.Project_ID
RIGHT JOIN WorksOnProject$ ON WorksOnProject$.Project_ID = Project$.Project_ID




