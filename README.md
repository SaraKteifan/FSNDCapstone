# FSNDCapstone
## Motivation for the project
Capstone Project for Full Stack Nano Degree by One Million Jordanian Coders and Udacity, it resembles an Acting Agency.

## URL location for the hosted API
https://acting-agency-3kf7.onrender.com/

JWT tokens are available in postman file for 3 different roles.

## Project dependencies, local development and hosting instructions,
To run the project localy you need to have Python, I have Python 3.11.3.

Some key dependencies used:

- [Flask](http://flask.pocoo.org/) 

- [SQLAlchemy](https://www.sqlalchemy.org/) 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) 

## Detailed instructions for scripts to set up authentication, install any project dependencies and run the development server.
1. Create your virtual environment (optional)
2. Install all required dependencies using pip by running:

```bash
pip install -r requirements.txt
```
3. With Postgres running, create a database:

```bash
createdb capstone
```

4. Set the required environment variables, including:
    - DATABASE_URL
    - TEST_DATABASE_URL
    - AUTH0_DOMAIN
    - API_AUDIENCE
    - TEST_TOKEN

5. run the server:
```bash
python app.py
```

## Documentation of API behavior and RBAC controls
### API Endpoints

`GET '/movies'`

- Fetches all the movies.
- Request Arguments: None
- Returns: An object with an array of movies and success as true.

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "1994",
            "title": "Leon"
        },
        {
            "id": 2,
            "release_date": "2010",
            "title": "Shutter Island"
        }
    ],
    "success": true
}
```

`GET '/actors'`

- Fetches all actors.
- Request Arguments: None
- Returns: An object with an array of actors and success as true.

```json
{
    "actors": [
        {
            "age": 45,
            "gender": " male",
            "id": 1,
            "movie_id": 1,
            "name": "Jean Reno"
        },
        {
            "age": 13,
            "gender": " female",
            "id": 2,
            "movie_id": 1,
            "name": "Natalie Portman"
        }
    ],
    "success": true
}
```

`POST '/movies'`

- Sends a post request in order to add a new movie.
- Request Arguments: 
```json
{
    "title": "Barbie",
    "release_date": "2023"
}
```
- Returns: the id of the newly created movie and success as true.

```json
{
    "created": 14,
    "success": true
}
```

`POST '/actors'`

- Sends a post request in order to add a new actor.
- Request Arguments: 
```json
{
    "name":"Margot Robbie",
    "age":25,
    "gender":"female",
    "movie_id":6
}
```
- Returns: The id of the newly created actor and success as true.

```json
{
    "created": 15,
    "success": true
}
```

`PATCH '/movies/${id}'`

- Edits a specified movie using the id of it.
- Request Arguments: id - integer and
```json
{
    "title": "Oppenheimer"
}
```
- Returns: An object with the status code of the request as 200 and success as true.

```json
{
    "status-code": 200,
    "success": true,
}
```

`PATCH '/actors/${id}'`

- Edits a specified actor using the id of it.
- Request Arguments: id - integer and
```json
{
    "name": "Leonardo DiCapprio"
}
```
- Returns: An object with the status code of the request as 200 and success as true.

```json
{
    "status-code": 200,
    "success": true,
}
```

`DELETE '/movies/${id}'`

- Deletes a specified movie using the id of it.
- Request Arguments: id - integer
- Returns: An object with the id of the deleted movie and success as true.

```json
{
  "deleted": 5,
  "success": true
}
```

`DELETE '/actors/${id}'`

- Deletes a specified actor using the id of it.
- Request Arguments: id - integer
- Returns: An object with the id of the deleted actor and success as true.

```json
{
  "deleted": 5,
  "success": true
}
```

### This project includes three rules for the users:
    - Casting Assistant
        * Can view actors and movies
    -Casting Director
        * All permissions a Casting Assistant has and…
        * Add or delete an actor from the database
        * Modify actors or movies
    - Executive Producer
        * All permissions a Casting Director has and…
        *Add or delete a movie from the database