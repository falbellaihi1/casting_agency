# Casting Agency

# INTRODUCTION 


This Udacity Capstone project Casting Agency. Casting Agency models is a company that is responsible for creating movies and managing and assigning actors to those movies.
This system is created to simplify the process of managing movies and actors.


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and run the following:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

#### Environment Variables

Once ``requirements.txt`` installed all required dependencies source all environment variables by running the following

``` 
source setup.sh
```
*Note if you are on windows and using cmd, this will not work, instead use git bash, as windows does not have equivalent source command*

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


## Database Setup
With Postgres running and connected, create two databases by running  

*casting agency db*
```bash
dropdb casting_agency
createdb casting_agency

or use setupdb.sh making sure the pguser is set as well as the password 


```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:


```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

or windows 
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run

```




Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 



## Testing
To run the tests, run setupdb.sh or run the followingh:
```

dropdb casting_agency_test
createdb casting_agency_test
```
Then run test app

````
python test_app.py
````


## Getting Frontend Setup

### Installing Dependencies
#### Installing Node and NPM
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).
#### Installing Ionic Cli
The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI  is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).
#### Installing project dependencies
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
 run:
```bash
npm install
```
## Required Tasks

### Configure Enviornment Variables
Ionic uses a configuration file to manage environment variables. These variables ship with the transpiled software and should not include secrets.

- Open `./src/environments/environments.ts` and ensure each variable reflects the system you stood up for the backend.

- navigate to project directory and to starter>frontend using CMD/BASH

```bash
ionic serve
```
*Note do not use ionic serve in production, instead build ionic* [Checkout the Ionic docs to learn more](https://ionicframework.com/docs/cli/commands/build)




-BASE URL 
    - Backend URL
    
        
        http://127.0.0.1:5000/
   -frontend URL
   
        ```http://127.0.0.1:8100/```
        
        

##API usage requirements

To use the API, a user has to be authenticated, to do that
While flask is running ``flask run ``&& started ionic ``ionic serve`` 

navigate to ```http://127.0.0.1:8100/tabs/user-page``` 
* click login and use the following information for each role you would like to test
##Executive Producer
       Email: executiveproducer@example.com
       Password : executiveproducer@1
##Casting Assistant
       Email: castingassistant@example.com
       Password : castingassistant@1
##Casting Director 
       Email: castingdirector@example.com
       Password : castingdirector@1
     




##HTTP STATUS CODE SUMMARY AND FORMAT
- 200 OK

    * Everything is working as it should 



- 404 resource not found

example

``` DELETE actors/4``` (none existent actor)


Returns
   ``` {
      "error": 404,
      "message": "resource not found",
      "success": false
    }
```
 - 422 unprocessable
 
    * POST \movies   


    
        { // sending json POST request JSON
            "title" :"" , "release_date":""
         }
   
- returns 
   
```
    {
      "error": 422,
      "message": "unprocessable",
      "success": false
    }
```
- 405 method not allowed
     * COPY \movies 
        {
            "error": 405,
            "message":method not allowed,
            "success": False,
        }
       
           
            
- 500 Internal Server Error
        
        {
            "error": 500,
            "message":Internal Server Error,
            "success": False,
        }  







```

API DOCUMENTATION 

Endpoints
GET '/movies'
GET ...
POST ...
DELETE ...
```




#Movies
GET '/movies'
-General
    - Fetches a dictionary of movies in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: Authentication Bearer header 

    
    
   Send request using curl :

    * 
    
        curl --location --request GET 'http://example.com/movies' 
        --header 'Authorization: Bearer YOUR_TOKEN
   
   Response:     
```
    {
    "movies": [
        [
            {
                "id": 1,
                "release_date": "Sat, 08 Aug 2020 00:00:00 GMT",
                "title": "The greatest Movie"
        ]
    ],
    "success": true
}

```



POST ```'/movies```
- General
    - Requires authentication and permission of post:movies
    - Date format must be '%m/%d/%Y'
    
    Send request using curl :
 ```
       curl --location --request POST 'http://example.com/movies  \
      -header 'Authorization: Bearer YOUR_TOKEN\
      --header 'Content-Type: application/json' \
      --data-raw '{"title":"the real movie", "release_date":"2/8/2020"}'
```
   * Returns: the movie that was added

```{
    "movies": [
        {
            "id": 2,
            "release_date": "Sat, 08 Feb 2020 00:00:00 GMT",
            "title": "the real stuff"
        }
    ],
    "success": true
}
```

PATCH ```'/movies/<int:id>```
- General
    - Requires authentication and permission of patch:movies
    - Request Arguments: movie id
    - Date format must be '%m/%d/%Y'
 
 
   Send request using curl :
 
    
    
   
```   curl --location --request PATCH 'http://127.0.0.1:5000/movies/1' 
   --header 'Authorization: Bearer YOUR_TOKEN
  --header 'Content-Type: application/json' \
  --data-raw '{"title":"edited movie", "release_date":"08/08/2020"}'
```




- returns edited question
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Sat, 08 Aug 2020 00:00:00 GMT",
            "title": "edited movie"
        }
    ],
    "success": true
}
```


DELETE '/movie/<int:id>'
General
    - Requires authentication and permission of delete:movies
    - Request Arguments: movie id\
    
    
    
   Send request using curl :
    
            curl --location --request DELETE 'http://127.0.0.1:5000/movies/1' \
            --header 'Authorization: Bearer YOUR_TOKEN
   - Returns:. 
```
{
    "deleted": 1,
    "success": true
}
```

#Actors

POST '/Actor'
- General
    - Requires authentication and permission of post:actor
    - Request Arguments: permissions

Send request using curl :
 ```
    curl --location --request POST 'http://127.0.0.1:5000/actors' \
    --header 'Authorization: Bearer YOUR_TOKEN' \
    --header 'Content-Type: application/json' \
    --data-raw '{"name":"new actor", "age":30, "gender":"male"}'
``` 

- returns 
 
```
{
    "actors": [
        {
            "age": 30,
            "gender": "male",
            "id": 2,
            "name": "new actor"
        }
    ],
    "success": true
}
``` 
GET '/Actor'
- General
    - Requires authentication and permission of get:actor
    - Request Arguments: permissions

Send request using curl :
 ```
 curl --location --request GET 'http://127.0.0.1:5000/actors' 
--header 'Authorization: Bearer YOUR_TOKEN' '
``` 

- returns 
 
```
{
    "actors": [
        [
            {
                "age": 2,
                "gender": "female",
                "id": 1,
                "name": "old actor"
            },
            {
                "age": 30,
                "gender": "male",
                "id": 2,
                "name": "new actor"
            }
        ]
    ],
    "
``` 
PATCH '/Actor/<int:id>'
- General
    - Requires authentication and permission of get:actor
    - Request Arguments: permissions
    - Require Actor ID

Send request using curl :
 ```
curl --location --request PATCH 'http://127.0.0.1:5000/actors/1' \
--header 'Authorization: Bearer YOUR_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{"name":"I edited this", "age":23, "gender":"female"}'
``` 

- returns 
 
```
{
    "actors": [
        {
            "age": 2,
            "gender": "female",
            "id": 1,
            "name": "I edited this"
        }
    ],
    "success": true
}
```               
DELETE '/Actor/<int:id>'
- General
    - Requires authentication and permission of get:actor
    - Request Arguments: permissions
    - Require Actor ID

Send request using curl :
 ```
curl --location --request DELETE 'http://127.0.0.1:5000/actors/1' \
--header 'Authorization: Bearer YOUR_TOKEN' 

``` 

- returns 
 
```
{
    "deleted": 1,
    "success": true
}
```    

##Authors
Faisal Albellaihi

*Done With the use of Udacity README template*

#Achnowledgements
Team of Udacity
