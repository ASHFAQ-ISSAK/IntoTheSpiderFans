Flask User Management API

Introduction
This project is a Flask-based API for user management. It provides endpoints to create, retrieve, update, and delete user records in a SQLite database. It utilizes Flask-Restful for creating RESTful APIs and Flask-SQLAlchemy for database management.

Features
User Registration: Users can create new accounts by providing a username, email, and password.
User Authentication: Passwords are securely hashed and stored in the database. Users can authenticate themselves by providing their credentials.
User Retrieval: Retrieve information about a specific user by their user ID.
User Update: Update user details such as username and email.
User Deletion: Delete a user from the database.
Prerequisites
Python 3.7 or higher
Flask
Flask-Restful
Flask-SQLAlchemy
Werkzeug
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/your-repository.git
Navigate to the project directory:

bash
Copy code
cd your-repository
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Set up the database:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Start the application:

bash
Copy code
flask run
The API will be accessible at http://localhost:5000.

API Endpoints
POST /users: Create a new user.
GET /users: Retrieve all users.
GET /users/<int:user_id>: Retrieve a specific user.
PUT /users/<int:user_id>: Update a specific user.
PATCH /users/<int:user_id>: Partially update a specific user.
DELETE /users/<int:user_id>: Delete a specific user.
License
This project is licensed under the MIT License.
