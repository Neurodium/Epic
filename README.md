# P12 -EpicEvent CMR
 API with a collection of endpoints used to manage Clients and their contracts in order to create Events

# Clone project
git clone https://github.com/Neurodium/Epic.git

# Setup virtual environment
python -m venv venv/

# Activate virtual environment
source venv/bin/activate

# Install dependencies
run pip install -r src/requirements.txt

#Install PostgreSQL for your distribution
go to: https://www.postgresql.org/download/

#Setup the database:
- run ShellSQL to create the database: follow the instructions corresponding to your OS: https://www.postgresqltutorial.com/install-postgresql/
- Modify settings.py to put the parameters corresponding to your database
  - Change the NAME if your database name is not the default postgres
  - Change the USER if you do not user postgres
  - Change the password to the one you have chosen

# Initialize database
 run manage.py migrate

# Launch Server
run manage.py runserver

# Create superuser
run manage.py createsuperuser

# Django application access
Get the API collection from Postman:  https://documenter.getpostman.com/view/17160432/UVsPPQBd<br>
Import the collection in your respository

# Django Admin features
Access to django admin using the superuser account
3 Groups have been created: Manager, Sales, Support

- Manager Group:
   - Users have rights to create, update, view and delete users
   - Users have rights to update, view clients, contracts and events

- Sales Group:
   - Users have rights to view, create clients, contracts and events
   - Users havec rights to update clients assigned to them and their related contracts and events

- Support Group:
   - Users have rights to view clients, contracs and events
   - Users have rights to update events their assigned to

# Features: Endpoint list:
1. [Login] HTTP METHOD: POST: http://127.0.0.1:8000/login/<br>
&nbsp;&nbsp;Log into your account with your credentials 
  
2. [User list] HTTP METHOD: GET: http://127.0.0.1:8000/user/<br>
&nbsp;&nbsp;List of users

3. [User creation] HTTP METHOD: POST: http://127.0.0.1:8000/user/<br>
&nbsp;&nbsp;Create user
  
4. [User update] HTTP METHOD: PUT: http://127.0.0.1:8000/user/<username/<br>
&nbsp;&nbsp;Update user

5. [User delete] HTTP METHOD: DELETE: http://127.0.0.1:8000/user/<username/<br>
&nbsp;&nbsp;Delete user

6. [User details] HTTP METHOD: GET: http://127.0.0.1:8000/user/<username/<br>
&nbsp;&nbsp;User details
  
