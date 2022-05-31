CREATE VIEW [Projects per Organization] AS
SELECT Organization$.Organization_name, Organization$.Organization_ID, Organization$.Abbreviation, Project$.Project_ID
FROM Project$
INNER JOIN Organization$ ON Organization$.Organization_ID = Project$.Organization_ID