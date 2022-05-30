
from flask import Flask ,render_template , request, redirect, url_for
import pypyodbc, re, json, os
from datetime import datetime

app=Flask(__name__)
sql_server_name = 'DESKTOP-RKKJMM1\SQLEXPRESS'
sql_database_name = 'ProjectFunding'
connection = pypyodbc.connect('Driver={SQL Server};Server='+sql_server_name+';Database='+sql_database_name)



@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content
#RESEARCHERS 
################
@app.route("/researchers", methods=['GET', 'POST'])
def researchers():
    rs = connection.cursor()   

    queryString = """
    SELECT DISTINCT 
    First_name + ' ' + Last_name as Full_name,
    datediff( YY, Birth_date, getdate()) as Age,
    Researcher_ID,
    Gender
    FROM Researcher$
    """
    rs.execute(queryString)
    researchers = rs.fetchall()

    return render_template("researchers.html", researchers=researchers)
# YOUNGRESEARCHERS QUERY
##############
@app.route("/youngresearchers", methods=['GET', 'POST'])
def young_researchers():
    rs = connection.cursor()   

    queryString = """
    SELECT TOP (5) R.First_name + ' ' + R.Last_name as Researcher_name, R.Researcher_ID , COUNT(*) as number_of_projects
    FROM Researcher$ AS R , WorksOnProject$ as W , Project$ as P
    WHERE R.Researcher_ID=W.Researcher_ID 
    AND R.Birth_date BETWEEN '1983-01-01' and '2024-01-01'
    AND P.Project_ID= W.Project_ID
    AND P.End_date BETWEEN '2022-12-31' and '3000-01-01'
    GROUP BY R.Researcher_ID, R.First_name, R.Last_name
    HAVING COUNT(*)> 0
    ORDER BY -COUNT(*)
    """
    rs.execute(queryString)
    youngresearchers = rs.fetchall()

    return render_template("youngresearchers.html", youngresearchers=youngresearchers)

@app.route("/sameprojects", methods=['GET', 'POST'])
def same_projects():
    rs = connection.cursor()   

    queryString = """
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
    """
    rs.execute(queryString)
    sameprojects = rs.fetchall()

    return render_template("sameprojects.html", sameprojects=sameprojects)

@app.route("/interestingfield", methods=['GET', 'POST'])
def interestingfield():
    rs = connection.cursor()   

    queryString = """
        SELECT Project$.Project_ID, Project$.Title AS Project_Title
    FROM Project$
    INNER JOIN ProjectScientificField$ ON Project$.Project_ID = ProjectScientificField$.Project_ID
    WHERE Scientific_field_ID = 527355 AND GETDATE() < Project$.End_date
    """
    rs.execute(queryString)
    interestingfield = rs.fetchall()

    rs1=connection.cursor()
    queryString1="""
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
    """
    rs1.execute(queryString1)
    interestingfield1 = rs1.fetchall()


    return render_template("interestingfield.html", interestingfield=interestingfield , interestingfield1=interestingfield1)

@app.route("/top5stems", methods=['GET', 'POST'])
def top_5_stems():
    rs = connection.cursor()   

    queryString = """
        SELECT TOP 5 Stem$.Stem_name, Organization$.Organization_name AS Company_name, sum(cast(Project$.AmountofMoney as float)) AS Total_Amount_of_Money
    FROM Project$
    INNER JOIN Company$ ON Project$.Organization_ID = Company$.Organization_ID
    INNER JOIN Stem$ ON Stem$.Stem_ID = Project$.Stem_ID
    INNER JOIN Organization$ ON Organization$.Organization_ID = Project$.Organization_ID
    GROUP BY Stem$.Stem_name, Organization$.Organization_name
    ORDER BY Total_Amount_of_Money desc

    """
    rs.execute(queryString)
    top5stems = rs.fetchall()

    return render_template("top5stems.html", top5stems=top5stems)

@app.route("/researchersdeliverables", methods=['GET', 'POST'])
def researchers_deliver():
    rs = connection.cursor()   

    queryString = """
        SELECT R.First_name + R.Last_name as Full_name, COUNT(*) as Number_of_projects
    FROM Researcher$ as R, WorksOnProject$ as W
    WHERE R.Researcher_ID=W.Researcher_ID
    AND NOT EXISTS
    (SELECT D.Project_ID
    FROM DELIVERY as D
    WHERE D.Project_ID=W.Project_ID
    )
    GROUP BY R.Researcher_ID, R.First_name, R.Last_name
    HAVING COUNT(*)>4
    """
    rs.execute(queryString)
    researchersdeliverables = rs.fetchall()

    return render_template("researchers_deliverables.html", researchersdeliverables=researchersdeliverables)

@app.route("/fieldcouples", methods=['GET', 'POST'])
def field_couples():
    rs = connection.cursor()   

    queryString = """
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

    """
    rs.execute(queryString)
    fieldcouples = rs.fetchall()

    return render_template("couplesfields.html", fieldcouples=fieldcouples)


@app.route("/", methods=['GET', 'POST'])
def dashboard():
    rs = connection.cursor() 
    if request.method=="POST":
        resid=request.form["ri"]
        return redirect(url_for("projectsperresearcher","projectsperorganization" , resid=resid))
    else:
        return render_template("selectdrop.html")

@app.route("/<resid>", methods=['GET', 'POST'])
def projectsperresearcher(resid):
    rs = connection.cursor()   

    queryString = """
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
    """
    rs.execute(queryString)
    projectsperresearcher = rs.fetchall()
    return render_template("projectsperresearcher.html", projectsperresearcher=projectsperresearcher, resid=resid)

@app.route("/projectsperorganization", methods=['GET', 'POST'])
def projectsperorganization():
    rs = connection.cursor()   

    queryString = """
    SELECT Organization$.Organization_name, Organization$.Organization_ID, Organization$.Abbreviation, Project$.Project_ID
    FROM Project$
    INNER JOIN Organization$ ON Organization$.Organization_ID = Project$.Organization_ID
    """
    rs.execute(queryString)
    projectsperorganization = rs.fetchall()
    return render_template("projectsperorganization.html", projectsperorganization=projectsperorganization)


# NEW PROJECT FORM
##############
@app.route("/newproject", methods=["GET", "POST"])
def newproject():
    rs = connection.cursor()
    
    Begin_date = str(request.form.get('inputBeginDate'))
    if(Begin_date != 'None'):
        Begin_date = datetime.strptime(Begin_date, '%Y-%m-%d')
    End_date = str(request.form.get('inputEndDate'))
    if(End_date != 'None'):
        End_date = datetime.strptime(End_date, '%Y-%m-%d')

    Project_title = str(request.form.get('inputProjectTitle'))
    Summary = str(request.form.get('inputSummary'))
    Amount = str(request.form.get('inputAmountOfFunding'))
    Stem_ID = str(request.form.get('inputIDofResponsibleStem'))
    Researcher_ID = str(request.form.get('inputIDofResearcherManager'))
    Organization_ID = str(request.form.get('inputIDofOrganization'))
    Program_ID = str(request.form.get('inputIDofProgram'))
    ScientificField_ID = str(request.form.get('inputIDofScientificField'))

    if (Begin_date == 'None' or End_date == 'None' or Amount == 'None' or Project_title == 'None'):
        return render_template("newproject.html")
         
    queryString = """
    SELECT max(Project_ID)
    FROM Project$
    """
    rs.execute(queryString)
    newProject_ID = rs.fetchall()
    newProject_ID = newProject_ID[0][0]+1

    queryString = """
    SELECT max(Evaluation_ID)
    FROM Project$
    """
    rs.execute(queryString)
    newEvaluation_ID = rs.fetchall()
    newEvaluation_ID = newEvaluation_ID[0][0] +1

    queryString = """
    INSERT INTO Project$
           (Project_ID,
            Title,
            AmountofMoney,
            Begin_date,
            Summary,
            Organization_ID,
            Researcher_ID,
            Evaluation_ID,
            Stem_ID,
            Program_ID,
            End_date
)
    VALUES
           ('{}'
           ,'{}'
           ,'{}'
           ,'{}'
           ,'{}'
           ,'{}'
           ,'{}'
           ,'{}'
           ,'{}'
           ,'{}'
           ,'{}')
    """.format(newProject_ID, Project_title, Amount, Begin_date, Summary,Organization_ID, Researcher_ID, newEvaluation_ID, Stem_ID, Program_ID , End_date)
    rs.execute(queryString)
    connection.commit()

    queryString = """
    SELECT max(ProjectScientificField_ID)
    FROM ProjectScientificField$
    """
    rs.execute(queryString)
    newProjectScientificField_ID = rs.fetchall()
    newProjectScientificField_ID = newProjectScientificField_ID[0][0] + 1

    queryString = """
    INSERT INTO ProjectScientificField$
            (ProjectScientificField_ID,
            Project_ID,
            Scientific_field_ID
            )
        VALUES
            ('{}'
            ,'{}'
            ,'{}'
            )
    """.format( newProjectScientificField_ID, newProject_ID, ScientificField_ID )
    rs.execute(queryString)
    connection.commit()
    
    queryString = """
    SELECT MAX(Evaluates_ID)
    FROM Evaluates$
    """
    rs.execute(queryString) 
    newEvaluates_ID = rs.fetchall()[0][0] +1
    

    queryString = """
    INSERT INTO Evaluates$
           (Evaluates_ID
           ,Evaluation_ID
           ,Researcher_ID
           ,Project_ID
           )
     VALUES
           ('{}',
           '{}')
    """.format(newEvaluates_ID, newEvaluation_ID, Researcher_ID ,newProject_ID)
    rs.execute(queryString)
    connection.commit()
   
    return render_template("newproject.html")

#RESEARCHER FORM
@app.route("/researchers/researcherform", methods=["GET", "POST"])
def researcherform():
    rs = connection.cursor() 

    current_researcher_id = request.args.get("researcher_id")
    if (current_researcher_id == None):
        current_researcher_id = ''

    queryString = """
    SELECT *
    FROM Researcher$
    WHERE Researcher_ID = '{}'
    """.format(current_researcher_id)
    rs.execute(queryString)
    current_researcher = rs.fetchall()
    if (current_researcher != []):
        birth_date = datetime.strftime(current_researcher[0].get('birth_date'), '%Y-%m-%d')
    else:
        birth_date = '1960-01-01'

    First_name = str(request.form.get('inputFirstName'))
    Last_name = str(request.form.get('inputLastName'))
    Birth_date = str(request.form.get('inputBirthDate'))
    if (Birth_date != 'None'):
        Birth_date = datetime.strptime(Birth_date, '%Y-%m-%d')
    #     min_time = datetime.strptime(min_time, '%Y-%m-%dT%H:%M')
    #     min_time_query = 'AND Entry_time >= \'' + datetime.strftime(min_time, '%m-%d-%Y %H:%M:%S') + '\' '
    Researcher_ID = str(request.form.get('inputResearcherID'))
    Gender = str(request.form.get('inputGender'))
   

    if (First_name != 'None' and Last_name != 'None' and Birth_date != 'None' and Researcher_ID != 'None' and Gender != 'None'):
        queryString = """
        IF '{}' IN (select Researcher_ID from Researcher$)
            UPDATE Researcher$
            SET First_name = '{}'
                ,Last_name = '{}'
                ,Birth_date = '{}'
                ,Researcher_ID = '{}'
                ,Gender = '{}'
            WHERE Researcher_ID = '{}'
        ELSE
            INSERT INTO Researcher$
                (First_name
                ,Last_name
                ,Birth_date
                ,Researcher_ID 
                ,Gender )
            VALUES
                ('{}'
                ,'{}'
                ,'{}'
                ,'{}'
                ,'{}'
                )
        """.format(Researcher_ID,
                First_name,  #repeat for update
                Last_name, 
                Birth_date, 
                Researcher_ID, 
                Gender, 
                Researcher_ID,
                First_name,  #repeat for insert
                Last_name, 
                Birth_date, 
                Researcher_ID, 
                Gender)
        rs.execute(queryString)
        connection.commit()

    return render_template("researcherform.html", current_researcher=current_researcher, birth_date=birth_date)    


# SERVICE ACCESSES
##############
@app.route("/programs", methods=['GET', 'POST'])
def programs():
    rs = connection.cursor()   

    queryString = """
    SELECT ProgramName
    FROM Program$ 
    """
    rs.execute(queryString)
    allprograms = rs.fetchall()

    selected_program_type = str(request.form.get('select-program-type'))
    if (selected_program_type == 'None'):
        selected_program_type = '\'\''

    stem = str(request.form.get('inputstem'))
    if (stem != None and stem != ''):
        stem_query = """AND""" + stem + '= 120 '
    else:
        stem_query = ''


    begin_date = request.form.get('begin_date')
    if ( begin_date != None):
         begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
         begin_date_query = """AND Begin_date <= \'""" + datetime.strftime( begin_date, '%Y-%m-%d %H:%M:%S') + '\' '
    else:
         begin_date_query = ''

    end_date = request.form.get('end_date')
    if ( end_date != None):
         end_date= datetime.strptime( end_date, '%Y-%m-%d')
         end_date_query = """AND End_date <= \'""" + datetime.strftime(end_date, '%Y-%m-%d %H:%M:%S') + '\' '
    else :
        end_date_query = ''

    queryString = """
    SELECT DISTINCT
    Title
    FROM Project$
    INNER JOIN Program$ ON Program$.Program_ID = Project$.Program_ID
    INNER JOIN Stem$ ON Stem$.Stem_ID = Project$.Stem_ID
    WHERE ProgramName = '{}'
    """.format(selected_program_type)
    #queryString = queryString + stem_query + end_date_query+begin_date_query
    rs.execute(queryString)
    projects = rs.fetchall()

    selected_project = str(request.form.get('select-project'))
    if (selected_project == 'None'):
        selected_project = ''

    queryString = """
    SELECT DISTINCT
    First_name + ' ' + Last_name as Full_name,
    Researcher$.Researcher_ID
    FROM Researcher$
    INNER JOIN WorksOnProject$ ON WorksOnProject$.Researcher_ID = Researcher$.Researcher_ID
    INNER JOIN Project$ ON Project$.Project_ID = WorksOnProject$.Project_ID
    INNER JOIN Program$ ON Program$.Program_ID = Project$.Program_ID
    WHERE Title = '{}'
    """.format(selected_project)
    rs.execute(queryString)
    res = rs.fetchall()

    return render_template("programs.html", allprograms=allprograms, projects=projects, selected_program_type=selected_program_type, res=res, selected_project=selected_project)

if __name__== "__main__":
    app.run(debug=True)