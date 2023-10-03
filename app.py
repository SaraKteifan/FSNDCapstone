import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from flask_cors import CORS
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    with app.app_context():
        setup_db(app)
    CORS(app)

    # End Points

    @app.route("/")
    def Welcome():
        return "Welcome to Udacity Acting Agency!!"

    @app.route("/movies")
    @requires_auth('get:movies')
    def get_movies():
        movies_query = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in movies_query]

        return jsonify(
            {
                "success": True,
                "movies": movies,
            }
        )

    @app.route("/actors")
    @requires_auth('get:actors')
    def get_actors():
        actors_query = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in actors_query]

        return jsonify(
            {
                "success": True,
                "actors": actors,
            }
        )

    @app.route("/movies", methods=["POST"])
    @requires_auth('post:movies')
    def add_movie():
        body = request.get_json()

        title = body.get("title", None)
        release_date = body.get("release_date", None)

        if title is None or release_date is None:
            abort(400)

        movie = Movie(title=title, release_date=release_date)
        movie.insert()

        return jsonify(
            {
                "success": True,
                "created": movie.id,
            }
        )

    @app.route("/actors", methods=["POST"])
    @requires_auth('post:actors')
    def add_actor():
        body = request.get_json()

        name = body.get("name", None)
        age = body.get("age", None)
        gender = body.get("gender", None)
        movie_id = body.get("movie_id", None)

        if name is None or age is None or gender is None or movie_id is None:
            abort(400)

        actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
        actor.insert()

        return jsonify(
            {
                "success": True,
                "created": actor.id,
            }
        )

    @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    @requires_auth('edit:movies')
    def edit_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        body = request.get_json()

        title = body.get("title", None)
        release_date = body.get("release_date", None)

        if title:
            movie.title = title
        if release_date:
            movie.release_date = release_date

        movie.update()

        return jsonify({
            "status-code": 200,
            "success": True,
            })

    @app.route('/actors/<int:actor_id>', methods=["PATCH"])
    @requires_auth('edit:actors')
    def edit_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        body = request.get_json()

        name = body.get("name", None)
        age = body.get("age", None)
        gender = body.get("gender", None)
        movie_id = body.get("movie_id", None)

        if name:
            actor.name = name
        if age:
            actor.age = age
        if gender:
            actor.gender = gender
        if movie_id:
            actor.movie_id = movie_id

        actor.update()

        return jsonify({
            "status-code": 200,
            "success": True,
            })

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.delete()

        return jsonify(
            {
                "success": True,
                "deleted": movie_id,
            }
        )

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):

        actor = Actor.query.filter(Actor.id == actor_id)\
            .one_or_none()

        if actor is None:
            abort(404)

        actor.delete()

        return jsonify(
            {
                "success": True,
                "deleted": actor_id,
            }
        )

    # Error Handlers

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
                }),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
                }),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False,
                "error": 400,
                "message": "bad request"
                }),
            400,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed"
                }),
            400,
        )

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response

    return app


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
