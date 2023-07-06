from flask import Flask, redirect, url_for, render_template, request, flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.safe_load(open('db.yaml'))

app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']= db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template("home_page.html", content = "Testing")

@app.route('/query_31')
def query_31():
    return render_template("query_31_menu.html")


@app.route('/query_31_researchers')
def query_31_researchers():
    return render_template('query_31_researchers.html')

@app.route('/query_31_projects')
def query_31_projects():
    return render_template('query_31_projects.html')

@app.route("/query_31_programs")
def query_31_programs():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("""SELECT * FROM Program;""")
    if resultValue > 0:
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')


@app.route('/query_31_researchers_result',methods=['GET', 'POST'])
def query_31_researchers_result():
    select = request.form.get('project_select')
    com = """SELECT Researcher.researcher_id, Researcher.forename, Researcher.surname FROM Researcher WHERE Researcher.researcher_id IN (SELECT Works_in.researcher_id FROM Works_in WHERE Works_in.project_id IN(SELECT Project.project_id FROM Project WHERE Project.project_id = %s));"""
    tuple = (str(select),)
    cur = mysql.connection.cursor()
    resultValue = cur.execute(com, tuple)
    if resultValue > 0:
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')




@app.route('/query_31_projects_result_executive',methods=['GET', 'POST'])
def query_31_projects_result_executive():
    select = request.form.get('executive_select')
    com = """SELECT Project.project_id, Project.title, Project.summary FROM Project WHERE Project.executive_id IN (SELECT Executive.executive_id FROM Executive WHERE Executive.executive_id = %s);"""
    tuple = (str(select),)
    cur = mysql.connection.cursor()
    resultValue = cur.execute(com, tuple)
    if resultValue > 0:
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')


@app.route('/query_31_projects_result_duration',methods=['GET', 'POST'])
def query_31_projects_result_duration():
    select = request.form.get('duration_select')
    com = """SELECT Project.project_id, Project.title, Project.summary FROM Project WHERE DATEDIFF(Project.end_date, Project.start_date) <= %s;"""
    tuple = (str(select),)
    cur = mysql.connection.cursor()
    resultValue = cur.execute(com, tuple)
    if resultValue > 0:
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')


@app.route('/query_31_projects_result_date',methods=['GET', 'POST'])
def query_31_projects_result_date():
    select = request.form.get('start_date')
    com = """SELECT Project.project_id, Project.title, Project.summary FROM Project WHERE Project.start_date = %s;"""
    tuple = (str(select),)
    cur = mysql.connection.cursor()
    resultValue = cur.execute(com, tuple)
    if resultValue > 0:
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')



@app.route("/query_32")
def query_32():
    return render_template("query_32_two_views.html")


@app.route("/query_32_first_view_result")
def query_32_first_view_result():
    cur = mysql.connection.cursor()
    cur.execute("""create or replace view projects_per_researcher as
    select r.researcher_id, r.surname, r.forename, p.project_id, p.title
    from Researcher as r 
    inner join Works_in as w on r.researcher_id=w.researcher_id 
    inner join Project as p on p.project_id=w.project_id
    order by r.researcher_id;""")
    resultValue = cur.execute("""select * from projects_per_researcher;""")
    if resultValue > 0:
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')


@app.route("/query_32_second_view_result")
def query_32_second_view_result():
    cur = mysql.connection.cursor()
    cur.execute("""create or replace view projects_per_organization as
    select o.organization_id, o.organization_name, p.project_id, p.title
    from Organization as o natural join Project as p
    order by organization_id;""")
    resultValue = cur.execute("""select  * from projects_per_organization;""")
    if resultValue > 0:
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')



@app.route("/query_33",methods=['GET', 'POST'])
def query_33():
    #select = "Physics"
    select = request.form.get('field_select')
    #return select
    com = """create or replace view famous_field as
    select p.project_id, p.title, f.field_id, f.field_name
    from Project as p 
    inner join Field_of_Project as fp on fp.project_id=p.project_id
    inner join Scientific_field as f on f.field_id=fp.field_id
    where datediff(curdate(), p.start_date)>0 and datediff(p.end_date, curdate())>0 AND f.field_name = %s;"""
    tuple = (str(select), )
    cur = mysql.connection.cursor()
    cur.execute(com, tuple)
    cur.execute("""create or replace view researcher_on_project as
    select r.researcher_id, r.surname, r.forename, p.project_id, p.title
    from Researcher as r
    inner join Works_in as w on w.researcher_id= r.researcher_id
    inner join Project as p on p.project_id=w.project_id;""")
    resultValue = cur.execute("""select ff.field_id, ff.field_name, ff.project_id, ff.title, rp.researcher_id, rp.surname, rp.forename
    from famous_field as ff
    inner join researcher_on_project as rp on ff.project_id=rp.project_id
    order by ff.field_id, rp.project_id;""")
    #resultValue = cur.execute("""SELECT researcher_id, forename, surname FROM Researcher WHERE DATEDIFF(Researcher.starting_work_day, CURRENT_DATE()) <= 365 AND researcher_id IN ( SELECT researcher_id FROM Works_in WHERE Works_in.project_id IN (SELECT project_id  FROM Project WHERE project_id IN (SELECT project_id FROM Field_of_Project WHERE field_id IN(SELECT field_id FROM Scientific_field WHERE field_name = "Mechatronics")) AND  CURRENT_DATE() > start_date AND CURRENT_DATE() < end_date));""")
    if resultValue > 0: #check if empty
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')

@app.route('/query_34')
def query_34():
    cur = mysql.connection.cursor()
    cur.execute("""create or replace view projects_per_organization_per_year (organization_id, organization_name, projects, yearr)
        AS
        SELECT org.organization_id, org.organization_name, count(*), YEAR(p.start_date) as yearr FROM Organization org
        INNER JOIN Project p
        ON org.organization_id = p.organization_id
        GROUP BY org.organization_id, yearr;""")
    resultValue = cur.execute("""SELECT i.organization_id, i.organization_name, i.yearr AS first_year, dupl.yearr AS second_year, i.projects AS projects_each_year
        FROM projects_per_organization_per_year i, projects_per_organization_per_year dupl
        WHERE i.organization_id = dupl.organization_id AND i.yearr = dupl.yearr -1 AND i.projects = dupl.projects AND i.projects >= 10;""")
    if resultValue > 0: #check if empty
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')
    



@app.route('/query_35')
def query_35():
    cur = mysql.connection.cursor()
    cur.execute("""create or replace view project_with_field as
        select p.project_id, p.title, f.field_id, f.field_name
        from Project as p
        inner join Field_of_Project as fp on fp.project_id=p.project_id
        inner join Scientific_field as f on f.field_id=fp.field_id;""")
    cur.execute("""create or replace view project_with_pair as
        select pf1.project_id, pf1.title, pf1.field_name as f1_name, pf2.field_name as f2_name
        from project_with_field as pf1
        cross join project_with_field as pf2
        where pf1.project_id =pf2.project_id and pf1.field_id >pf2.field_id
        order by pf1.project_id;""")
    resultValue = cur.execute("""select count(project_id) as val, f1_name, f2_name
        from project_with_pair
        group by f1_name, f2_name
        order by val desc
        limit 3;
        """)
    if resultValue > 0: #check if empty
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        return render_template('result.html', field_names=['val', 'field Name', 'field Name'], res=res)
    else:
        return render_template('empty.html')



  
@app.route('/query_36')
def query_36():
    cur = mysql.connection.cursor()
    cur.execute("""create or replace view young_Researcher as
        select researcher_id, surname, forename
        from Researcher
        where datediff(curdate(), birthdate)<14640;""")
    cur.execute("""create or replace view active_Project as
        select project_id, title
        from Project
        where datediff(curdate(), start_date)>0 and datediff(end_date, curdate())>0;""")
    cur.execute("""create or replace view young_Researcher_on_active_Project as
        select yr.researcher_id, yr.surname, yr.forename, ap.project_id
        from young_Researcher as yr
        inner join Works_in as w on yr.researcher_id=w.researcher_id
        inner join active_Project as ap on w.project_id=ap.project_id;""")
    cur.execute("""create or replace view active_projects_of_researcher as
        select researcher_id, surname, forename, count(project_id) as active_projects
        from young_Researcher_on_active_Project
        group by researcher_id;""")
    resultValue = cur.execute("""select researcher_id, surname, forename, active_projects
        from active_projects_of_researcher
        where active_projects=(select maxi from (select max(active_projects) as maxi from active_projects_of_researcher)as maximum);""")
    if resultValue > 0: #check if empty
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)      
    else:
        return render_template('empty.html')


@app.route('/query_37')
def query_37():
    cur = mysql.connection.cursor()
    resultValue= cur.execute("SELECT Executive.forename, Executive.surname, Project.funding, Organization.organization_name FROM Project JOIN Executive ON Project.executive_id = Executive.executive_id JOIN Organization ON Organization.organization_id = Project.project_id WHERE Organization.organization_type = 'Company' AND Executive.executive_id IN( SELECT Project.executive_id FROM Project WHERE Project.organization_id IN (SELECT Organization.organization_id FROM Organization WHERE Organization.organization_type = 'Company')  ORDER BY funding DESC) AND Project.organization_id IN (SELECT Organization.organization_id FROM Organization WHERE Organization.organization_type = 'Company');")
    if resultValue > 0: #check if empty
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')


@app.route('/query_38')
def query_38():
    cur = mysql.connection.cursor()
    resultValue= cur.execute("""create or replace view Projects_without_deliverables as
    select project_id, title
    from Project
    where project_id not in (select Project.project_id from Project join Deliverable on Project.project_id=Deliverable.project_id);""")

    resultValue = cur.execute("""
        select researcher_id, surname, forename, count(project_id) as proj_wtht_deliverables
        from (select r.researcher_id, r.surname, r.forename, pwtd.project_id, pwtd.title
		from Researcher as r
		inner join Works_in as w on w.researcher_id=r.researcher_id
		inner join Projects_without_deliverables as pwtd on pwtd.project_id=w.project_id)as researcher_on_proj_wtht_deliv
        group by researcher_id
        having proj_wtht_deliverables>=5;""")
    if resultValue > 0: #check if empty
        res = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]        
        return render_template('result.html', field_names=field_names, res=res)
    else:
        return render_template('empty.html')

app.secret_key='mysecretkey'

@app.route('/modify')
def modify():
    return render_template('CRUD-menu.html')

#ORGANIZATION

@app.route('/organization')
def organization():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM Organization')
    data=cur.fetchall()
    return render_template('modify_organization.html', org=data)

@app.route('/add_org', methods=['POST'])
def add_org():
    if request.method=='POST':
        organization_id=request.form['organization_id']
        organization_name=request.form['organization_name']
        abbreviation=request.form['abbreviation']
        street_name=request.form['street_name']
        street_number=request.form['street_number']
        postal_code=request.form['postal_code']
        city=request.form['city']
        organization_type=request.form['organization_type']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO Organization(organization_id, organization_name, abbreviation, street_name, street_number, postal_code, city, organization_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (organization_id, organization_name, abbreviation, street_name, street_number, postal_code, city, organization_type))
        mysql.connection.commit()
        flash('ORGANIZATION ADDED')
    return redirect(url_for('organization'))


@app.route('/delete_org/<string:id>')
def delete_org(id):
    #return format(title) formattitle= title
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM Organization where organization_id=%s', (id,))
    mysql.connection.commit()
    flash('DELETED')
    return redirect(url_for('organization'))


@app.route('/edit_org/<id>')
def edit_org(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM Organization WHERE organization_id=%s', (id,))
    data=cur.fetchall()
    return render_template('edit-org.html', org=data[0])

@app.route('/update_org/<id>', methods=['POST'])
def update_org(id):
    if request.method=='POST':
        organization_id=request.form['organization_id']
        organization_name=request.form['organization_name']
        abbreviation=request.form['abbreviation']
        street_name=request.form['street_name']
        street_number=request.form['street_number']
        postal_code=request.form['postal_code']
        city=request.form['city']
        organization_type=request.form['organization_type']
        cur=mysql.connection.cursor()
        cur.execute("""
            UPDATE Organization
            SET organization_id=%s,
                organization_name=%s,
                abbreviation=%s,
                street_name=%s,
                street_number=%s,
                postal_code=%s,
                city=%s, 
                organization_type=%s
            WHERE organization_id= %s
        """, (organization_id, organization_name, abbreviation, street_name, street_number, postal_code, city, organization_type, id))
        mysql.connection.commit()
        flash('UPDATED')
        return redirect(url_for('organization'))

#RESEARCHER

@app.route('/researcher')
def researcher():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM Researcher')
    data=cur.fetchall()
    return render_template('modify_researcher.html', res=data)

@app.route('/add_res', methods=['POST'])
def add_res():
    if request.method=='POST':
        researcher_id=request.form['researcher_id']
        organization_id=request.form['organization_id']
        forename=request.form['forename']
        surname=request.form['surname']
        sex=request.form['sex']
        birthdate=request.form['birthdate']
        starting_work_day=request.form['starting_work_day']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO Researcher(researcher_id, organization_id, forename, surname, sex, birthdate, starting_work_day) VALUES (%s, %s, %s, %s, %s, %s, %s)', (researcher_id, organization_id, forename, surname, sex, birthdate, starting_work_day))
        mysql.connection.commit()
        flash('RESEARCHER ADDED')
    return redirect(url_for('researcher'))


@app.route('/delete_res/<string:id>')
def delete_res(id):
    #return format(title) formattitle= title
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM Researcher where researcher_id=%s', (id,))
    mysql.connection.commit()
    flash('DELETED')
    return redirect(url_for('researcher'))


@app.route('/edit_res/<id>')
def edit_res(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM Researcher WHERE researcher_id=%s', (id,))
    data=cur.fetchall()
    return render_template('edit-res.html', res=data[0])

@app.route('/update_res/<id>', methods=['POST'])
def update_res(id):
    if request.method=='POST':
        researcher_id=request.form['researcher_id']
        organization_id=request.form['organization_id']
        forename=request.form['forename']
        surname=request.form['surname']
        sex=request.form['sex']
        birthdate=request.form['birthdate']
        starting_work_day=request.form['starting_work_day']
        cur=mysql.connection.cursor()
        cur.execute("""
            UPDATE Researcher
            SET researcher_id=%s,
                organization_id=%s,
                forename=%s,
                surname=%s,
                sex=%s,
                birthdate=%s,
                starting_work_day=%s
            WHERE researcher_id= %s
        """, (researcher_id, organization_id, forename, surname, sex, birthdate, starting_work_day, id))
        mysql.connection.commit()
        flash('UPDATED')
        return redirect(url_for('researcher'))



#PROJECT

@app.route('/project')
def project():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM Project')
    data=cur.fetchall()
    return render_template('modify_project.html', proj=data)

@app.route('/add_proj', methods=['POST'])
def add_proj():
    if request.method=='POST':
        project_id=request.form['project_id']
        title=request.form['title']
        summary=request.form['summary']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        funding=request.form['funding']
        evaluation_date=request.form['evaluation_date']
        grade=request.form['grade']
        organization_id=request.form['organization_id']
        program_id=request.form['program_id']
        executive_id=request.form['executive_id']
        supervisor_id=request.form['supervisor_id']
        evaluator_id=request.form['evaluator_id']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO Project(project_id, title, summary, start_date, end_date, funding, evaluation_date, grade, organization_id, program_id, executive_id, supervisor_id, evaluator_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (project_id, title, summary, start_date, end_date, funding, evaluation_date, grade, organization_id, program_id, executive_id, supervisor_id, evaluator_id))
        mysql.connection.commit()
        flash('PROJECT ADDED')
    return redirect(url_for('project'))


@app.route('/delete_proj/<string:id>')
def delete_proj(id):
    #return format(title) formattitle= title
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM Project where project_id=%s', (id,))
    mysql.connection.commit()
    flash('DELETED')
    return redirect(url_for('project'))


@app.route('/edit_proj/<id>')
def edit_proj(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM Project WHERE project_id=%s', (id,))
    data=cur.fetchall()
    return render_template('edit-proj.html', proj=data[0])

@app.route('/update_proj/<id>', methods=['POST'])
def update_proj(id):
    if request.method=='POST':
        project_id=request.form['project_id']
        title=request.form['title']
        summary=request.form['summary']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        funding=request.form['funding']
        evaluation_date=request.form['evaluation_date']
        grade=request.form['grade']
        organization_id=request.form['organization_id']
        program_id=request.form['program_id']
        executive_id=request.form['executive_id']
        supervisor_id=request.form['supervisor_id']
        evaluator_id=request.form['evaluator_id']
        cur=mysql.connection.cursor()
        cur.execute("""
            UPDATE Project
            SET project_id=%s,
                title=%s,
                summary=%s,
                start_date=%s,
                end_date=%s,
                funding=%s,
                evaluation_date=%s,
                grade=%s, 
                organization_id=%s,
                program_id=%s,
                executive_id=%s,
                supervisor_id=%s,
                evaluator_id=%s
            WHERE project_id= %s
        """, (project_id, title, summary, start_date, end_date, funding, evaluation_date, grade, organization_id, program_id, executive_id, supervisor_id, evaluator_id, id))
        mysql.connection.commit()
        flash('UPDATED')
        return redirect(url_for('project'))








if __name__ == "__main__":
    app.run(debug = True)
