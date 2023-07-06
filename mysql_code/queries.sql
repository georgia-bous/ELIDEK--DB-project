#3.1
/* See all the researchers that work on a particular project, based on title */

SELECT Researcher.researcher_id, Researcher.forename, Researcher.surname FROM Researcher WHERE Researcher.researcher_id IN (SELECT Works_in.researcher_id FROM Works_in WHERE Works_in.project_id IN(SELECT Project.project_id FROM Project WHERE Project.project_id = 2));


/*Date if it wants to retrieve the researchers that work in a particular project*/
SELECT Researcher.researcher_id, Researcher.forename, Researcher.surname FROM Researcher WHERE Researcher.researcher_id IN (SELECT Works_in.researcher_id FROM Works_in WHERE Works_in.project_id IN(SELECT Project.project_id FROM Project WHERE Project.start_date ='2021-01-11'));

/*Duration*/
SELECT Researcher.researcher_id, Researcher.forename, Researcher.surname FROM Researcher WHERE Researcher.researcher_id IN (SELECT Works_in.researcher_id FROM Works_in WHERE Works_in.project_id IN(SELECT Project.project_id FROM Project WHERE DATEDIFF(Project.end_date, Project.start_date) <= 1000 ));


/*Date if it only wants to retrieve project  from date*/

SELECT Project.project_id, Project.title FROM Project WHERE Project.start_date = '2022-01-31';

/*Duration if it only wants to retrieve project from duration */

SELECT Project.project_id, Project.title FROM Project WHERE DATEDIFF(Project.end_date, Project.start_date) <= 730;


#3.2


#first
create view projects_per_researcher as
select r.researcher_id, r.surname, r.forename, p.project_id, p.title
from Researcher as r 
inner join Works_in as w on r.researcher_id=w.researcher_id
inner join Project as p on p.project_id=w.project_id
order by r.researcher_id;



#second
create view projects_per_organization as
select o.organization_id, o.organization_name, p.project_id, p.title
from Organization as o natural join Project as p
order by organization_id;


#3.3


#We assume that we know the Field's id
create or replace view famous_field as
select p.project_id, p.title, f.field_id, f.field_name
from Project as p
inner join Field_of_Project as fp on fp.project_id=p.project_id
inner join Scientific_field as f on f.field_id=fp.field_id
where datediff(curdate(), p.start_date)>0 and datediff(p.end_date, curdate())>0 AND f.field_name = "Mathematics";


create or replace view researcher_on_project as
select r.researcher_id, r.surname, r.forename, p.project_id, p.title
from Researcher as r
inner join Works_in as w on w.researcher_id= r.researcher_id
inner join Project as p on p.project_id=w.project_id;


select ff.field_id, ff.field_name, ff.project_id, ff.title, rp.researcher_id, rp.surname, rp.forename
from famous_field as ff
inner join researcher_on_project as rp on ff.project_id=rp.project_id
order by ff.field_id, rp.project_id;




#3.4


CREATE VIEW projects_per_organization_per_year (organization_id, organization_name, projects, yearr)
AS
SELECT org.organization_id, org.organization_name, count(*), YEAR(p.start_date) as yearr FROM Organization org
INNER JOIN Project p
ON org.organization_id = p.organization_id
GROUP BY org.organization_id, yearr;


SELECT i.organization_id, i.organization_name, i.yearr AS first_year, dupl.yearr AS second_year, i.projects AS projects_each_year
FROM projects_per_organization_per_year i, projects_per_organization_per_year dupl
WHERE i.organization_id = dupl.organization_id AND i.yearr = dupl.yearr -1 AND i.projects = dupl.projects AND i.projects >= 10;


#3.5


create view project_with_field as
select p.project_id, p.title, f.field_id, f.field_name
from Project as p
inner join Field_of_project as fp on fp.project_id=p.project_id
inner join Scientific_field as f on f.field_id=fp.field_id;



create view project_with_pair as
select pf1.project_id, pf1.title, pf1.field_name as f1_name, pf2.field_name as f2_name
from project_with_field as pf1
cross join project_with_field as pf2
where pf1.project_id =pf2.project_id and pf1.field_id >pf2.field_id
order by pf1.project_id;


select count(project_id) as val, f1_name, f2_name
from project_with_pair
group by f1_name, f2_name
order by val desc
limit 3;



#3.6

create view young_Researcher as
select researcher_id, surname, forename
from Researcher
where datediff(curdate(), birthdate)<14640;

create view active_Project as
select project_id, title
from Project
where datediff(curdate(), start_date)>0 and datediff(end_date, curdate())>0;

create view young_Researcher_on_active_Project as
select yr.researcher_id, yr.surname, yr.forename, ap.project_id
from young_Researcher as yr
inner join Works_in as w on yr.researcher_id=w.researcher_id
inner join active_Project as ap on w.project_id=ap.project_id;

create view active_projects_of_researcher as
select researcher_id, surname, forename, count(project_id) as active_projects
from young_Researcher_on_active_Project
group by researcher_id;

#select * from young_Researcher;
#select *from active_Project;

select researcher_id, surname, forename, active_projects
from active_projects_of_researcher
where active_projects=(select maxi 
						from (select max(active_projects) as maxi 
								from active_projects_of_researcher
								)as maximum);
                                
                                
#3.7

SELECT Executive.forename, Executive.surname, Project.funding, Organization.organization_name FROM Project
JOIN Executive ON Project.executive_id = Executive.executive_id
JOIN Organization ON Organization.organization_id = Project.project_id
WHERE Organization.organization_type = 'Company' AND Executive.executive_id IN( 
																SELECT Project.executive_id FROM Project 
                                                                WHERE Project.organization_id IN (
																	SELECT Organization.organization_id FROM Organization 
                                                                    WHERE Organization.organization_type = 'Company')  
																ORDER BY funding DESC) AND Project.organization_id IN (
																												SELECT Organization.organization_id FROM Organization 
                                                                                                                WHERE Organization.organization_type = 'Company');

#3.8

create view Projects_without_deliverables as
select project_id, title
from Project
where project_id not in (select Project.project_id from Project join Deliverable on Project.project_id=Deliverable.project_id);


select researcher_id, surname, forename, count(project_id) as proj_wtht_deliverables
from (select r.researcher_id, r.surname, r.forename, pwtd.project_id, pwtd.title
		from Researcher as r
		inner join Works_in as w on w.researcher_id=r.researcher_id
		inner join Projects_without_deliverables as pwtd on pwtd.project_id=w.project_id)as researcher_on_proj_wtht_deliv
group by researcher_id
having proj_wtht_deliverables>=5;