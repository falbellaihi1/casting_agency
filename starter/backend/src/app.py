import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from .models import setup_db, create_db, Actors, Movies
from .auth.auth import AuthError, requires_auth
from datetime import datetime


def create_app(test_config=None):  # create src
    app = Flask(__name__)
    setup_db(app)
    # CORS(src)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    create_db()

    @app.after_request
    def after_request(response):  # after request header decorators
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        """ endpoint to retrieve all actors in the database, requiring permission get:actors. Returns formatted actors if successful"""
        try:
            retrieve_actors = Actors.query.all()  # get all actors from database
            formatted_actors = [artist.format() for artist in retrieve_actors]  # loop and format result

            return jsonify({
                "success": True,
                "actors": [formatted_actors]
            })
        except Exception as e:

            abort(401)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        """ endpoint to retrieve all movies in the database, requiring permission get:movies. Returns formatted movies if successful"""
        try:
            retrieve_movies = Movies.query.all()  # get all actors from database
            formatted_movies = [movies.format() for movies in retrieve_movies]  # loop and format result

            return jsonify({
                "success": True,
                "movies": [formatted_movies]
            })
        except Exception as e:
            abort(401)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        """ endpoint to delete an actors from the database, requiring permission delete:actors. Returns id of deleted
        actor if successful """
        try:
            actor = Actors.query.filter(Actors.id == id).one_or_none()  # retrieve actor from database
            if not actor:  # if returned none abort 404
                abort(404)
            else:
                actor.delete()  # delete actor
                return jsonify({
                    "success": True,
                    "deleted": id,
                })
        except Exception as e:
            abort(404)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        """ endpoint to delete a movie from the database, requiring permission delete:movies. Returns id of deleted
               movie if successful """
        try:
            movie = Movies.query.filter(Movies.id == id).one_or_none()  # get the movie from database
            if not movie:  # if none abort 404
                abort(404)
            else:
                movie.delete()  # delete movie
                return jsonify({
                    "success": True,
                    "deleted": id,
                })
        except Exception as e:
            abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(playload):
        try:
            if request.json.get('name') == "" or request.json.get('age') == "" or request.json.get('gender') == "":
                abort(422)  # unprocessable values abort 422
            new_actor = Actors(name=request.json.get('name'), age=request.json.get('age'),
                               gender=request.json.get('gender'))  # set the values
            Actors.insert(new_actor)  # insert the actor
            query_actor = Actors.query.filter(Actors.id == new_actor.id).one_or_none()  # retrieve the actor from
            # database
            return jsonify({
                "success": True,
                "actors": [query_actor.format()]
            })

        except Exception as e:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(playload):
        """ endpoint to create a movie in the database, requiring permission post:movies. Returns the formatted
               movie if successful """
        try:
            if request.json.get('title') == "" or request.json.get('release_date') == "":
                abort(422)  # unprocessable values abort 422
            json_str_date = request.json.get('release_date')
            release_date = datetime.strptime(json_str_date, '%m/%d/%Y')  # convert into date format
            new_movie = Movies(title=request.json.get('title'), release_date=release_date)  # set the values
            Actors.insert(new_movie)  # insert the movie
            query_movies = Movies.query.filter(Movies.id == new_movie.id).one_or_none()  # retrieve the inserted movie
            return jsonify({
                "success": True,
                "movies": [query_movies.format()]
            })

        except Exception as e:

            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(payload, id):
        """ endpoint to edit a actor in the database, requiring permission patch:actor. returns the formatted actor
        if successful """
        error = 404  # define error variable
        try:

            actors = Actors.query.filter(Actors.id == id).one_or_none()  # retrieve the actor from database
            if not actors:
                error = 404  # if none, abort 404
                abort(error)
            if request.json.get('name') == "" or request.json.get('age') == "" or request.json.get('gender') == "":
                error = 422  # unprocessable values abort 422
                abort(error)
            actors.name = request.json.get('name')
            actors.email = request.json.get('email')
            actors.gender = request.json.get('gender')
            Actors.update(actors)
            updated_actors = Actors.query.filter(Actors.id == id).one_or_none()  # get updated actor

            return jsonify({
                "success": True,
                "actors": [updated_actors.format()]
            })
        except Exception as e:
            abort(error)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies(payload, id):
        """ endpoint to edit a movies in the database, requiring permission patch:movies. returns the formatted movies
                if successful """
        error = 404  # define error variable
        try:
            movie = Movies.query.filter(Movies.id == id).one_or_none()  # retrieve movie from database
            if not movie:  # if returned none abort
                error = 404
                abort(error)
            if (request.json.get('title') == "" or request.json.get('release_date') == ""):
                error = 422  # set error to 422 as the values are unprocessable
                abort(error)
            json_str_date = request.json.get('release_date')
            release_date = datetime.strptime(json_str_date, '%m/%d/%Y')  # get the date in date format
            movie.title = request.json.get('title')
            movie.release_date = release_date
            Movies.update(movie)
            updated_movie = Movies.query.filter(Movies.id == id).one_or_none()  # retrieve the updated movie

            return jsonify({
                "success": True,
                "movies": [updated_movie.format()]
            })
        except Exception as e:
            abort(error)

    ## Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(401)
    def authorization(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "you do not have the permissions to do this action"
        }), 401

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
    @TODO implement error handler for 404
        error handler should conform to general task above 
    '''
    '''
    @TODO implement error handlers using the @src.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                 jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):

        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above 
    '''

    @app.errorhandler(AuthError)
    def auth_error(error):  # handle auth errors and returns it as json
        print('tb')
        print(error.status_code)
        print(error.error)
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error

        }), error.status_code

    return app



