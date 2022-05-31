WITH CTE AS
	(SELECT Project$.Organization_ID, year(Project$.Begin_date) AS First_Year, COUNT(year(Project$.Begin_date)) AS No_of_projects
	FROM Project$
	WHERE Project$.Organization_ID is not null
	GROUP BY Project$.Organization_ID, year(Project$.Begin_date))
	SELECT *
FROM CTE 
INNER JOIN (SELECT Organization$.Organization_name, Project$.Organization_ID, year(Project$.Begin_date) AS Second_year, COUNT(year(Project$.Begin_date)) AS No_of_projects
	FROM Project$
	INNER JOIN Organization$ ON Organization$.Organization_ID = Project$.Organization_ID
	WHERE Project$.Organization_ID is not null
	GROUP BY Project$.Organization_ID, Organization$.Organization_name, year(Project$.Begin_date)) AS A ON CTE.Organization_ID = A.Organization_ID
WHERE CTE.Organization_ID = A.Organization_ID 
AND CTE.First_year <> A.Second_year 
AND CTE.First_year < A.Second_year 
AND CTE.First_year = A.Second_year - 1
AND CTE.No_of_projects = A.No_of_projects
AND CTE.No_of_projects >= 10
AND A.No_of_projects >= 10

