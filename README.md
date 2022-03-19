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

# Initialize database
 run manage.py migrate

# Launch Server
run manage.py runserver

# Django application access
Get the API collection from Postman:  https://documenter.getpostman.com/view/17160432/UVXeqcUR<br>
Import the collection in your respository

# Features: Endpoint list:
1. [Register] HTTP METHOD: POST: http://127.0.0.1:8000/signup/<br>
&nbsp;&nbsp;Create your account
  
2. [Login] HTTP METHOD: POST: http://127.0.0.1:8000/login/<br>
&nbsp;&nbsp;Log into your account with your credentials 
  
3. [User Projects list] HTTP METHOD: GET: http://127.0.0.1:8000/projects/<br>
&nbsp;&nbsp;List of projects where user is author or contributor
  
4. [Create Project] HTTP METHOD: POST: http://127.0.0.1:8000/projects/<br>
&nbsp;&nbsp;Create a project
  
5. [Get Project Details] HTTP METHOD: GET: http://127.0.0.1:8000/projects/<project_id>/<br>
&nbsp;&nbsp;Retrieve details of a project

6. [Update Project] HTTP METHOD: PUT: http://127.0.0.1:8000/projects/<project_id>/<br>
&nbsp;&nbsp;Change the details of a project
  
7. [Delete Project] HTTP METHOD: DELETE: http://127.0.0.1:8000/projects/<project_id>/<br>
&nbsp;&nbsp;Delete a project

8. [Add Contributor] HTTP METHOD: POST: http://127.0.0.1:8000/projects/<project_id>/users/<br>
&nbsp;&nbsp;Add a contributor to a project

9. [Get Project's Users list] HTTP METHOD: GET: http://127.0.0.1:8000/projects/<project_id>/users/<br>
&nbsp;&nbsp;Retrieve the list of users of a project

10. [Remove Contributor] HTTP METHOD: DELETE: http://127.0.0.1:8000/projects/<project_id>/users/<user_id>/<br>
&nbsp;&nbsp;Remove a contributor from a project

11. [Retrieve issues list] HTTP METHOD: GET: http://127.0.0.1:8000/projects/<project_id>/issues/<br>
&nbsp;&nbsp;Get the list of issues of a project

12. [Create New Issue] HTTP METHOD: POST: http://127.0.0.1:8000/projects/<project_id>/issues/<br>
&nbsp;&nbsp;Create a new issue for a project

13. [Update issue] HTTP METHOD: PUT: http://127.0.0.1:8000/projects/<project_id>/issues/<issue_id>/<br>
&nbsp;&nbsp;Update an issue

14. [Delete issue] HTTP METHOD: DELETE: http://127.0.0.1:8000/projects/<project_id>/issues/<issue_id>/<br>
&nbsp;&nbsp;Delete an issue

15. [Add Comment] HTTP METHOD: POST: http://127.0.0.1:8000/projects/<project_id>/issues/<issue_id>/comments/<br>
&nbsp;&nbsp;Add Comment to an Issue

16. [Retrieve Comments' list] HTTP METHOD: GET: http://127.0.0.1:8000/projects/<project_id>/issues/<issue_id>/comments/<br>
&nbsp;&nbsp;Retrieve list of comments of an issue on a project

17. [Update Comment] HTTP METHOD: PUT: http://127.0.0.1:8000/projects/<project_id>/issues/<issue_id>/comments/<comment_id>/<br>
&nbsp;&nbsp;Update a comment

18. [Delete Comment] HTTP METHOD: DELETE: http://127.0.0.1:8000/projects/<project_id>/issues/<issue_id>/comments/<comment_id>/<br>
&nbsp;&nbsp;Delete a comment

19. [Delete Comment] HTTP METHOD: GET: http://127.0.0.1:8000/projects/<project_id>/issues/<issue_id>/comments/<comment_id>/<br>
&nbsp;&nbsp;Retrieve details of a comment 
