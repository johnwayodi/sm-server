# Store Manager API
[![Coverage Status](https://coveralls.io/repos/github/johnwayodi/sm-api-v2/badge.svg?branch=develop)](https://coveralls.io/github/johnwayodi/sm-api-v2?branch=develop)
[![Build Status](https://travis-ci.org/johnwayodi/sm-api-v2.svg?branch=develop)](https://travis-ci.org/johnwayodi/sm-api-v2)
[![Maintainability](https://api.codeclimate.com/v1/badges/c23849e92db44dd7a9b2/maintainability)](https://codeclimate.com/github/johnwayodi/sm-api-v2/maintainability)

API for Store Manager Application

## Testing
Test the api can be done using a variety of api testing tools, however [Postman](https://www.getpostman.com/) is suggested.


#### Endpoints
The api exposes the following endpoints:

#### `/auth/register`

Register new users in the system. Can only register two types of users, _*admin*_ and _*attendant*_

Example: Register an _admin_ user.

    { 
        "username":"jack",
	    "password":"tester",
	    "role":"admin"
    }

#### `/auth/login`
User can log into the system.

*note*: only registered users are able to login, if a login is successsful, a *jwt token* is returned in the response, this token has to be included in the header in order to access the other endpoints of the api.

Example:

    { 
        "username":"jack",
	    "password":"tester"
    }


#### `/api/v1/products`
1. GET `api/v1/products` both admin and attendant users can get products in inventory
2. GET `api/v1/products/<product_id>` get a single product and display its details
3. DELETE `api/v1/products/<product_id>` deletes a product from the inventory, only admin user can delete a product
4. POST `api/v1/products` add new product to inventory, only users can add products to inentory
        
        {
	        "name":"Phone",
	        "description":"a cool device to own",
	        "price": 10000,
	        "category": "electronics",
	        "stock": 500,
	        "min_stock": 50
        }

#### `/api/v1/sales`
1. GET `api/v1/sales` both admin and attendant users can get sale records
2. GET `api/v1/sales/<product_id>` get a single sale record and display its details
3. POST `api/v1/sales` create a new sale record, only attendants can create sale records

    For a sale to occur, the _product_ids_ specified have to already be in the inventory. The 
    _*count*_ is the number of units of the product to be sold
    
    Example: 

        {
	        "products":{
		        "1":{
			        "product_id":1,
			        "count":2 },
		        "2":{
			        "product_id":2,
			        "count":10 }
		        }
        }


#### `/api/v1/users`

Display all the users registered in the application

