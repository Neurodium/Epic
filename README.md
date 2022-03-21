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
  - Change the PASSWORD to the one you have chosen

# Initialize database
 run python manage.py migrate

# Launch Server
run python manage.py runserver

# Create superuser
run python manage.py createsuperuser

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
## Login
[Login] HTTP METHOD: POST: http://127.0.0.1:8000/login/<br>
&nbsp;&nbsp;Log into your account with your credentials and get your user token

## User Management [Restricted to Manager Group Users]
1. [User list] HTTP METHOD: GET: http://127.0.0.1:8000/user/<br>
&nbsp;&nbsp;List of users

2. [User creation] HTTP METHOD: POST: http://127.0.0.1:8000/user/<br>
&nbsp;&nbsp;Create user
  
3. [User update] HTTP METHOD: PUT: http://127.0.0.1:8000/user/<username/<br>
&nbsp;&nbsp;Update user

4. [User delete] HTTP METHOD: DELETE: http://127.0.0.1:8000/user/<username/<br>
&nbsp;&nbsp;Delete user

5. [User details] HTTP METHOD: GET: http://127.0.0.1:8000/user/<username/<br>
&nbsp;&nbsp;User details

## Client Management:
- Endpoints restricted to authentified users:
  1. [Client list] HTTP METHOD: GET: http://127.0.0.1:8000/client/<br>
   &nbsp;&nbsp;List of clients
   
  2. [Client details] HTTP METHOD: GET: http://127.0.0.1:8000/client/<company_name>/<br>
   &nbsp;&nbsp;Client details
   
- Endpoints restricted to Sales client owner and Manager Group users:
   [Client update] HTTP METHOD: PUT: http://127.0.0.1:8000/client/<company_name>/<br>
   &nbsp;&nbsp;Update client
   
- Endpoints restricted to Sales Group users:
   [Client create] HTTP METHOD: POST: http://127.0.0.1:8000/client/<br>
   &nbsp;&nbsp;Create client
   

## Contract Management:
- Endpoints restricted to authentified users:
   1. [Contract list] HTTP METHOD: GET: http://127.0.0.1:8000/contract/<br>
   &nbsp;&nbsp;List of contracts
   
   2. [Contract details] HTTP METHOD: GET: http://127.0.0.1:8000/contract/<contract_id>/<br>
   &nbsp;&nbsp;Contract details
   
- Endpoints restricted to Sales client owner or Manager Group users:
   [Contract update] HTTP METHOD: PUT: http://127.0.0.1:8000/contract/<contract_id>/<br>
   &nbsp;&nbsp;Update contract
   
- Endpoints restricted to Sales Group users:
   [Contract create] HTTP METHOD: POST: http://127.0.0.1:8000/contract/<br>
   &nbsp;&nbsp;Create contract
   
  

## Event Management:
- Endpoints restricted to authentified users:
   1. [Event list] HTTP METHOD: GET: http://127.0.0.1:8000/event/<br>
   &nbsp;&nbsp;List of events
   
   2. [Event details] HTTP METHOD: GET: http://127.0.0.1:8000/event/<event_id>/<br>
   &nbsp;&nbsp;Event details
   
- Endpoints restricted to Sales client owner, Event Support owner, or Manager Group users:
   [Event update] HTTP METHOD: PUT: http://127.0.0.1:8000/event/<event_id>/<br>
   &nbsp;&nbsp;Update event
   
- Endpoints restricted to Sales Group users:
   [Event create] HTTP METHOD: POST: http://127.0.0.1:8000/event/<br>
   &nbsp;&nbsp;Create event
   

## Manager Group Users Specific endpoints:
   1. [Client Missing Sales] HTTP METHOD: GET: http://127.0.0.1:8000/api/client/nosales/<br>
   &nbsp;&nbsp;List of Clients where no sales contact have been assigned
   
   2. [Missing Event Support] HTTP METHOD: GET: http://127.0.0.1:8000/api/event/nosupport/<br>
   &nbsp;&nbsp;List of Events where no support contact have been assigned
   
   
## Sales Group Users Specific endpoints:
   1. [Potential Clients] HTTP METHOD: GET: http://127.0.0.1:8000/api/client/potential/<br>
   &nbsp;&nbsp;List of Clients which have not signed any contract
   
   2. [All Coming Events] HTTP METHOD: GET: http://127.0.0.1:8000/api/comingevent/<br>
   &nbsp;&nbsp;List of all coming events
   
   3. [Client Coming Events] HTTP METHOD: GET: http://127.0.0.1:8000/api/comingevent/<client_company_name>/<br>
   &nbsp;&nbsp;List of all coming events for a specific client
   
   

## Support Group Users Specific endpoints:
   [My Events] HTTP METHOD: GET: http://127.0.0.1:8000/api/event/supportevent/<br>
   &nbsp;&nbsp;List of Events assigned to the user
