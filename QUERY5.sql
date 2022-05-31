SELECT TOP 3 a1.Scientific_field_name, a2.Scientific_field_name
FROM (
SELECT DISTINCT s1.Scientific_field_name, s2.Project_ID
FROM Scientific_field$ AS s1
INNER JOIN (
	SELECT A.Scientific_field_ID AS Scientific_field_ID1, B.Scientific_field_ID AS Scientific_field_ID2, A.Project_ID
	FROM ProjectScientificField$ A, ProjectScientificField$ B
	WHERE A.Project_ID = B.Project_ID AND A.Scientific_field_ID > B.Scientific_field_ID) AS s2 ON s1.Scientific_field_ID = s2.Scientific_field_ID1) AS a1
INNER JOIN (
SELECT DISTINCT s3.Scientific_field_name, s4.Project_ID
FROM Scientific_field$ AS s3
INNER JOIN(
	SELECT A.Scientific_field_ID AS Scientific_field_ID1, B.Scientific_field_ID AS Scientific_field_ID2, A.Project_ID
	FROM ProjectScientificField$ A, ProjectScientificField$ B
	WHERE A.Project_ID = B.Project_ID AND A.Scientific_field_ID > B.Scientific_field_ID) AS s4 ON s3.Scientific_field_ID = s4.Scientific_field_ID2) AS a2
ON a2.Project_ID = a1.Project_ID
WHERE a1.Scientific_field_name <> a2.Scientific_field_name
GROUP BY a1.Scientific_field_name, a2.Scientific_field_name/*, a1.Project_ID*/
ORDER BY COUNT(*) desc
