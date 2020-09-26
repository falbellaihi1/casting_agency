import os
import unittest
import json


from src.app import create_app
from src.models import setup_db, db, Movies, Actors


def get_headers(role):  # return headers based on role
    auth = ''
    if (role == 'ep'):
        executive_producer = os.environ.get('executive_producer')
        auth = executive_producer
    if (role == 'ca'):
        casting_assistant = os.environ.get('casting_assistant')
        auth = casting_assistant
    if (role == 'cd'):
        casting_director = os.environ.get('casting_director')
        auth = casting_director

    headers = {'authorization': 'Bearer {}'.format(auth)}

    return headers


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency  test case"""

    # According to python docs for unit testing  the order of executing tests is determined with respect of strings ordering
    # meaning I could name tests functions in that respect to control the execution order : test exuctive director order create get edit
    # ' Note The order in which the various tests will be run is determined by sorting the test method names
    # with respect to the built-in ordering for strings
    # https://docs.python.org/3/library/unittest.html
    # '

    @classmethod
    def setUpClass(self):
        """Excuted in the beginning of the test, the target of this test is that all tests run in order at once """
        """Define test variables and initialize src."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://postgres:0000@{}/{}".format('localhost:5432', self.database_name)

        # binds the src to the current context
        self.new_actor = {"name": "Markos24", "age": 23, "gender": "Male"}
        self.new_movie = {"title": "the real stuff", "release_date": "08/20/2020"}
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            db.init_app(self.app)
            # create all tables
            db.drop_all()
            db.create_all()

    def setUp(self):
        """Executed before each test prepares lists of roles that has permissions to do certain actions in the src"""

        self.role_create_delete_actor = ['ep', 'cd']  # set up roles that has permissions to create and delete actors
        self.role_modify_movie_actor = ['ep', 'cd']  # set up roles that has permissions to modify movie and actor
        self.role_view_actors_movies = ['ep', 'cd', 'ca']  # set up roles that has permissions to view actors and movie
        self.role_delete_movie_401 = ['cd', 'ca']  # set up roles that does not have permissions to delete movie

    def tearDown(self):
        """Executed after each test"""

    def test_a_create_actors(self):
        """Testing create actor, if success, actor should be created in db, tests end point successful and tests role

        executive_producer and casting_director
        """
        for role in range(len(self.role_create_delete_actor)):
            header = (self.role_create_delete_actor[role])
            res = self.client().post('/actors', json=self.new_actor, headers=get_headers(header))
            data = json.loads(res.data)
            # print(self.role_create_delete_actor[role] ,'who can create --?',data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['actors'])

    def test_b_create_movie(self):
        """Testing create actor, if success, actor should be created in db
        also tests role executive_producer role who has permission to create a movie
        """
        # print('create movie')
        res = self.client().post('/movies', json=self.new_movie, headers=get_headers('ep'))
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_c_get_movies(self):

        """Testing get movies for success of each point and for role executive_producer, this should return the list of movies
        tests successful endpoint && all roles
        """
        # print('get movies')
        for role in range(len(self.role_view_actors_movies)):
            header = (self.role_view_actors_movies[role])
            res = self.client().get('/movies', headers=get_headers(header))
            data = json.loads(res.data)
            # print(self.role_view_actors_movies[role] ,'who can view --?',data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['movies'])

    def test_d_get_actors(self):
        """Testing get actors

        tests successful endpoint && all roles
        """
        # print('get actor')
        for role in range(len(self.role_view_actors_movies)):
            header = (self.role_view_actors_movies[role])
            res = self.client().get('/actors', headers=get_headers(header))
            data = json.loads(res.data)
            # print(self.role_view_actors_movies[role] ,'who can view --?',data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['actors'])

    def test_e_edit_actor(self):
        """Testing edit actor, if success, actor should be edited in db"""
        # print('edit actor ')
        for role in range(len(self.role_modify_movie_actor)):
            header = self.role_modify_movie_actor[role]
            res = self.client().patch('/actors/1', json={"name": "new edited name", "email": "new edited email"},
                                      headers=get_headers(header))
            data = json.loads(res.data)
            # print(self.role_modify_movie_actor[role], 'who can edit ---- >',data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['actors'])

    def test_f_edit_movie(self):
        # print('edit movie')
        """Testing edit actor movie, if success, actor should be edited in db"""
        for role in range(len(self.role_modify_movie_actor)):
            header = self.role_modify_movie_actor[role]
            res = self.client().patch('/movies/1', json={"title": "new edited title", "release_date": "08/20/2020"},
                                      headers=get_headers(header))
            data = json.loads(res.data)
            # print(self.role_modify_movie_actor[role], 'who can edit ---- >', data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['movies'])

    def test_g_delete_movie(self):
        """Testing delete movie method, this test should delete the movie from  db, if success it will return 200"""
        # print('delete')

        res = self.client().delete('/movies/1', headers=get_headers('ep'))
        data = json.loads(res.data)
        # print('eo is able to delete movie ---->', data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(movie, None)

    def test_h_delete_actor(self):
        """Testing delete actor method, this test should delete the actor from  db, if suceess it will return 200"""
        # print('delete')
        actor_id = 1  # id to try get customer from db, and is set to 2 at the end of the for loop to get the next actor in db
        for role in range(len(self.role_create_delete_actor)):
            header = (self.role_create_delete_actor[role])
            res = self.client().delete('/actors/' + str(actor_id), headers=get_headers(header))
            data = json.loads(res.data)
            # print(self.role_create_delete_actor[role], ' who can deletee ---> ', data)
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['deleted'])
            self.assertEqual(actor, None)
            actor_id = 2

        ### Errors ###

    def test_404_delete_movie(self):
        """Testing 404 delete actor method should return 404"""
        # print('delete')
        res = self.client().delete('/movies/100000000', headers=get_headers('ep'))
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_404_delete_actor(self):
        """Testing delete actor method, this test should delete the actor from  db, if suceess it will return 200"""
        # print('delete')
        res = self.client().delete('/actors/100000000', headers=get_headers('ep'))
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_404_edit_actor(self):
        # print('404 actor')
        """Testing RBAC for editing a actor"""
        res = self.client().patch('/actors/100000000', json={"name": "new edited name", "email": "new edited email"},
                                  headers=get_headers('ep'))
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_404_edit_movie(self):
        """Testing 404 for editing a actor"""
        res = self.client().patch('/movies/100000000', json={"title": "title", "release_date": ""},
                                  headers=get_headers('ep'))
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_401_get_actor(self):
        """Testing get 401 actors"""
        # print('get actor')
        res = self.client().get('/actors', headers='')
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_401_get_movie(self):
        """Testing get 401 movies"""
        # print('get movie')
        res = self.client().get('/actors', headers='')
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_401_edit_movie(self):
        # print('RBAC 401')
        """Testing RBAC for editing a movie"""
        res = self.client().patch('/movies/1', json={"title": "new edited title", "release_date": ""},
                                  headers=get_headers('ca'))
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_401_edit_actor(self):
        # print('RBAC 401 actor')
        """Testing RBAC for editing a movie"""
        res = self.client().patch('/actors/1', json={"name": "new edited name", "email": "new edited email"},
                                  headers=get_headers('ca'))
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_401_delete_actor(self):
        """Testing RBAC for role ca to delete actor, it should return 401"""
        # print('RBAC 401 DELETE')
        res = self.client().delete('/actors/1', headers=get_headers('ca'))
        data = json.loads(res.data)
        # print(data)
        # actor = Actors.query.filter(Actors.id == 1).one_or_none()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_401_create_movie(self):
        """Testing create actor, if fail, actor should be not be created in db as the role trying to create is casting director who does not have permission
        """
        # print('create movie')
        res = self.client().post('/movies', json=self.new_movie, headers=get_headers('cd'))
        data = json.loads(res.data)
        # print('casting director cannot create movie --->', data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_401_delete_movie(self):
        """Testing 404 delete actor method should return 404"""
        # print('delete')
        for role in range(len(self.role_delete_movie_401)):
            headers = self.role_delete_movie_401[role]
            res = self.client().delete('/movie', headers=get_headers(headers))
            data = json.loads(res.data)
            # print('role : ', self.role_delete_movie_401[role], ' cannot delete ----> ', data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertTrue(data['message'])


if __name__ == "__main__":
    unittest.main()
