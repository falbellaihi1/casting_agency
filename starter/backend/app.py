import json
import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import setup_db, create_db, Actors, Movies
from auth.auth import AuthError, requires_auth
from datetime import datetime

def create_app(test_config=None):  # create app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)
   # app.secret_key = os.environ.get('SECRET_KEY')
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
        try:
            get_actors = Actors.query.all()
            formatted_actors = [artist.format() for artist in get_actors]

            return jsonify({
                "success": True,
                "actors": [formatted_actors]
            })
        except Exception as e:
            print(e)
            abort(404)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            get_movies = Movies.query.all()
            formatted_movies = [movies.format() for movies in get_movies]

            return jsonify({
                "success": True,
                "movies": [formatted_movies]
            })
        except Exception as e:
            print(e)
            abort(404)

    @app.route('/actor/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        try:

            actor = Actors.query.filter(Actors.id == id).one_or_none()

            if not actor:
                abort(404)

            else:
                actor.delete()
                return jsonify({
                    "success": True,
                    "deleted": id,
                })
        except Exception as e:
            print(e)
            abort(404)


    @app.route('/movie/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        try:

            movie = Movies.query.filter(Movies.id == id).one_or_none()

            if not movie:
                abort(404)

            else:
                movie.delete()
                return jsonify({
                    "success": True,
                    "deleted": id,
                })
        except Exception as e:
            print(e)
            abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(playload):  # CUSTOMER ID NEEDS TO BE PASSED HERE,
        try:

            new_actor = Actors(name=request.json.get('name'), age=request.json.get('age'),
                               gender=request.json.get('gender'))
            Actors.insert(new_actor)
            query_actor = Actors.query.filter(Actors.id == new_actor.id).one_or_none()
            return jsonify({
                "success": True,
                "actors": [query_actor.format()]
            })

        except Exception as e:
            print(e)
            abort(401)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(playload):  # CUSTOMER ID NEEDS TO BE PASSED HERE,
        try:
            json_str_date = request.json.get('release_date')
            release_date = datetime.strptime(json_str_date,'%m/%d/%Y')
            print(release_date)
            new_movie = Movies(title=request.json.get('title'), release_date=release_date)
            Actors.insert(new_movie)
            query_movies = Movies.query.filter(Movies.id == new_movie.id).one_or_none()
            return jsonify({
                "success": True,
                "movies": [query_movies.format()]
            })

        except Exception as e:
            print(e)
            abort(401)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(payload, id):
        print('tyhis')
        try:
            actors = Actors.query.filter(Actors.id == id).one_or_none()
            if not actors:
                abort(404)
            actors.name = request.json.get('name')
            actors.email = request.json.get('email')
            Actors.update(actors)
            updated_actors = Actors.query.filter(Actors.id == id).one_or_none()

            return jsonify({
                "success": True,
                "actors": [updated_actors.format()]
            })
        except Exception as e:
            print(e)
            abort(401)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies(payload, id):
        try:
            movie = Movies.query.filter(Movies.id == id).one_or_none()
            if not movie:
                abort(404)
            movie.name = request.json.get('title')
            movie.email = request.json.get('release_date')
            Movies.update(movie)
            updated_movie = Movies.query.filter(Movies.id == id).one_or_none()

            return jsonify({
                "success": True,
                "movies": [updated_movie.format()]
            })
        except Exception as e:
            print(e)
            abort(401)











    ## Error Handling
    '''
    Example error handling for unprocessable entity
    '''

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
    @TODO implement error handlers using the @app.errorhandler(error) decorator
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



# if __name__ == "__main__":
#     create_app().run()
if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=8080, debug=True)