# ELIDEK--DB-project
This is a project for the Databases course. The purpose of this project is to create a SQL database, where the ELIDEK organisation will store data. Then we create a backend, which will run on localhost, and a basic frontend to perform queries on this data.

In the database we store information on:
- Projects of ELIDEK
- Organisations that manage projects
- Researchers
- Programs that finance the projects
- Research fields for the projects
- Managers
(see in Docs for more info)

Through the app a user can:

- filter the projects on start/end date, duration or manager
- see the projects on which a researcher is working
- the projects and researcher working on a specific field the last year
- which organisations have the same number of projects for 2 consecutive years with at leat 10 projects per year
- which projects cover more than one field and which pair of fields is the more often
- which researchers, younger than 40 years old, work in the biggest number of projects and what is that number
- top 5 managers that have given the biggest financing

I use Python's Flask for the backend and basic HTML with some JS for the frontend.
  **HOW TO USE:**
First go to MySQL Workbench and run the sql scripts (add the trigger manually to the Works_in table).
Then open the project folder in your IDE and create a file db.yaml with contents:
mysql_host: 'localhost'
mysql_user: 'root'
mysql_password: [password of MySQL Workbench]
mysql_db: 'elidek'

Afterwards, run the db_flask_app.py file and open your browser in localhost to interact with the application.
