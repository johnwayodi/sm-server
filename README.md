# Store Manager API

[![Coverage Status](https://coveralls.io/repos/github/johnwayodi/sm-api-v2/badge.svg?branch=develop)](https://coveralls.io/github/johnwayodi/sm-api-v2?branch=develop)
[![Build Status](https://travis-ci.org/johnwayodi/sm-api-v2.svg?branch=develop)](https://travis-ci.org/johnwayodi/sm-api-v2)
[![Maintainability](https://api.codeclimate.com/v1/badges/c23849e92db44dd7a9b2/maintainability)](https://codeclimate.com/github/johnwayodi/sm-api-v2/maintainability)
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/faa1bb2518cd81a3e91d)


##Testing and Usage
To test the application locally, first configure the environment as follows:
2. Install [PostgreSQL] if not already installed and ensure it is up and running.
2. Ensure [Python3]() is installed
2. Create a folder on your computer, once in the newly created repository, clone the project by 
running the following command:
    
    `git clone https://github.com/johnwayodi/sm-api-v2.git`
3. Install [virtualenv](https://virtualenv.pypa.io/en/latest/) which will aid in the creation of a vitual environment.
Once virtual environment is installed, create a new virtual environment named *venv*
    
    `virtualenv venv`
4. Once the virtual environment is created, activate it using the following command: 
    
    `source venv/bin/activate`  
5. Once the virtualenv is activated, the **requirements.txt** file contains the various requirements.
Run the following command to install all the requirements for the application.
    
    `pip install -r requirements.txt` 
6. Set up the environment variables, 
    
        export JWT_SECRET_KEY=""
        export API_SECRET_KEY=""
        export DATABASE_NAME=""
        export DATABASE_HOST=""
        export DATABASE_USER=""
        export DATABASE_PASS=""

7. After all is set, run the application, export the application and pass the following command:
        
        flask run
## Endpoints
The API exposes the following endpoints the
1. ####Auth Endpoints
    The `/auth` endpoint allow the registration of users and a login route to allow registered
    users to log into the application 
    <table style="width:100%">
      <tr>
        <td>POST</td>
        <td>/auth/register</td>
        <td>Register new user, only admin user can register</td>
      </tr>
      <tr>
        <td>POST</td>
        <td>/auth/login</td>
        <td>Users can login to the system, only successful when users are in the database</td>
      </tr>
    </table>

2. ####Category Endpoints
    The `/category` endpoint allows all the CRUD operations on the category items.
    <table style="width:100%">
      <tr>
        <td>POST</td>
        <td>/categories</td>
        <td>Add new category, only accessible to the admin</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/categories</td>
        <td>Retrieve all categories, only accesible by admin</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/categories/{category_id}</td>
        <td>Retrieve a single category, only accesible by admin</td>
      </tr>
      <tr>
        <td>PUT
        <td>/categories/{category_id}</td>
        <td>Update a specific category, only accesible by admin</td>
      </tr>
      <tr>
        <td>DELETE
        <td>/categories/{category_id}</td>
        <td>Remove a category, only accesible by admin</td>
      </tr>
    </table>

3. ####Product Endpoints
    The `/products` endpoint allows all CRUD operations on product items
    <table style="width:100%">
      <tr>
        <td>POST</td>
        <td>/products</td>
        <td>Add new product, only accessible to the admin</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/products</td>
        <td>Retrieve all products</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/products/{product_id}</td>
        <td>Retrieve a single category, only accesible by admin</td>
      </tr>
      <tr>
        <td>PUT
        <td>/products/{product_id}</td>
        <td>Update a specific product, only accessible to admin</td>
      </tr>
      <tr>
        <td>DELETE
        <td>/products/{product_id}</td>
        <td>Remove a product, only accesible by admin</td>
      </tr>
    </table>

4. ####Sales Endpoints
    The `/sales` endpoint allows all CRUD operations on sale items
    <table style="width:100%">
      <tr>
        <td>POST</td>
        <td>/sales</td>
        <td>Add new sale, only accessible to the attendant</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/sales</td>
        <td>Retrieve all sales</td>
      </tr>
      <tr>
        <td>GET</td>
        <td>/sales/{sale_id}</td>
        <td>Retrieve a single sale, displays a list of sold products in the sale</td>
      </tr>
    </table>
 
##Technologies used
The following software tools were used in the development of this application:
1. [Python](https://www.python.org/): Programming language.
1. [Flask](http://flask.pocoo.org/): The underlying web framework.
2. [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/): For the development of the API.
3. [Flasgger](https://github.com/rochacbruno/flasgger): For the generation of the API Docs. 
4. [Pytest](https://docs.pytest.org/en/latest/): For testing and debugging.
5. [Coveralls](https://coveralls.io/) and [Code Climate](https://codeclimate.com/): For tracking and covering of testing. 
6. [Pylint](https://www.pylint.org/): For code analysis.
7. [Postman](https://www.getpostman.com/): For Manual Testing and generation of Documentation.
8. [PostgreSQL](https://www.postgresql.org/): Database. 
_TODO_: _update readme_.
