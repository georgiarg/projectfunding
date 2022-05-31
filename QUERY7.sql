SELECT TOP 5 Stem$.Stem_name, Organization$.Organization_name AS Company_name, sum(cast(Project$.AmountofMoney as float)) AS Total_Amount_of_Money
FROM Project$
INNER JOIN Company$ ON Project$.Organization_ID = Company$.Organization_ID
INNER JOIN Stem$ ON Stem$.Stem_ID = Project$.Stem_ID
INNER JOIN Organization$ ON Organization$.Organization_ID = Project$.Organization_ID
GROUP BY Stem$.Stem_name, Organization$.Organization_name
ORDER BY Total_Amount_of_Money desc

