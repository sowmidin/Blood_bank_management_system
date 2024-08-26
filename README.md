# Blood bank management app


This is an API for managing blood donors, inventory, hospital requests. It is built using Flask, Flask-Restx, Flask-JWT-Extended, and SQLAlchemy.


## Table of Contents

- [Blood bank management API]
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Setup](#setup)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
    - [Admins](#admins)
    - [User](#users)
    - [Donor Manager](#donormanager)
    - [Inventory](#inventory)
  - [Usage](#usage)
    - [Register a User:](#register-a-user)
    - [Login:](#login)
    - [Manage Donors,Inventory,Hospital request:](#manage-admins-user-donormanager-inventory-donor)

## Requirements

- Python 3.8+
- SQLite (for local development)

## Installation

1. Clone the repository:

   git clone https://github.com/yourusername/Blood_bank_management_system.git
   cd Blood_bank_management_system



## Setup

Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install the dependencies:
```bash
pip install -r requirements.txt
```
Create a .env file in the root directory and add the following environment variables:

env
```bash
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///alumni.db
```

Initialize the database:

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
## Running the Application

Run the Flask application:

```bash
flask run
```
The API will be available at http://127.0.0.1:5000/api.

## API Endpoints
### Authentication

Register: POST /api/auth/register

Request Body:
 
 ```JSON
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "string"
}
```

Response:
 
 
 ```JSON
{
  "message": "User registered successfully"
}
```
Login: POST /api/auth/login

Request Body:
 
 
 ```JSON
{
  "email": "string",
  "password": "string"
}
```
Response:
 
 
 ```
JSON{
  "access_token": "string"
}
```

### Donors

Get All Donors: GET /donors/

Response:
 
```JSON
[
 {
  "id": "int",
  "name": "string",
  "age": "int",
  "blood_group": "string",
  "email_id": "string"
}
]
```

Create Admin: POST /donors/

Request Body:
 
 
 ```JSON
{
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "password": "string"
}
```
Response:
 
 
 ```JSON
[
  {
    "id": 3,
    "name": "Radha",
    "age": 30,
    "blood_group": "AB+",
    "email_id": "radha@gmail.com"
  },
  {
    "id": 4,
    "name": "Geetha",
    "age": 25,
    "blood_group": "O-",
    "email_id": "geetha@gmail.com"
  }
]
```

Get Donor by ID: GET /donors/{id}

Response:
  
 ```JSON
{
    "id": 4,
    "name": "Geetha",
    "age": 25,
    "blood_group": "O-",
    "email_id": "geetha@gmail.com"
  }
```

Update Admin by ID: PUT /donors/{id}

Request Body:
  
 ```JSON
{
  "username": "string",
  "email": "string",
  "company_id": "integer",
  "password": "string"
}
```

Response:
  
 ```JSON
{
  "message": "Donor details updated successfully"
}
```

Delete Admin by ID: DELETE /donors/{id}

Response: 
 
 ```JSON
{
  "message": "Donor deleted successfully"
}
```

### Inventory

Get All Blood inventory details: GET /inventory/

Response: 

```JSON
[
  {
    "blood_group": "AB+",
    "units": 2
  },
  {
    "blood_group": "B+",
    "units": 4
  },
  {
    "blood_group": "A+",
    "units": 0
  }
]
```

Create HR: POST /inventory/

Request Body:
  
 ```JSON
{
  "blood_group": "string",
  "units": "int
}
```

Response: 
 
 ```JSON
{
  "message": "Inventory updated successfully for <blood group>"
}
```

Get blood inventory details by ID: GET /inventory/{id}

Response:
  
 ```JSON
{
  "blood_group": "string",
  "units": "int
}
```

Update blood inventory by ID: PUT /inventory/{id}

Request Body:
  
 ```JSON
{
  "blood_group": "str",
  "units": "int"
}
```

Response:
  
 ```JSON
{
  "message":  "Inventory blood group details for <BLOOD_GROUP> and units <QUANTITY> successfully updated"
}




### Hospital requests for blood 

POST query for blood type and units needed : POST /donors/

Request body:

```JSON
{
  "blood_type": "string",
  "units_needed": "int"
}
```

Response

```JSON
{"message": "Blood requests for <blood group> - <quantity> units purchased successfully"}

```

## Usage
### Register a User:

Use the /api/auth/register endpoint to register a user,admin,donor manager
Provide the username, email, password, role in the request body.

### Login:

Use the /api/auth/login endpoint to obtain a JWT token.
Provide the username and password in the request body.
Use the JWT token in the Authorization header with the Bearer scheme to access protected endpoints.


