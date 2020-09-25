import unittest
import json

from src.app import create_app
from src.models import setup_db, db, Movies, Actors


def get_headers(role):  # return headers based on role
    auth = ''
    if (role == 'ep'):
        executive_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNjV0szM2VDZkN4VHczMUo2aHFsWiJ9.eyJpc3MiOiJodHRwczovL2ZhbGJlbGxhaWhpMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY2NWYyZWJhNTExZmUwMDZiNzgzYTFiIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTYwMTA0NTIwNSwiZXhwIjoxNjAxMTMxNjA1LCJhenAiOiJwRXZvczNvNVpHNk1UaVRTUWFUMTJoRE5PRXNHSklqUiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.rNPxuaV9jzaFuCgq7pAbkICWQp_e9A9Qy-KfmAb74xRje20bTGRL-MpIbW8a-6dpUMcSfRt87zRj9L-WyMHv15OfiLiOcN70mMFwpu22z-i39nmViVMKiQsu6G4xu9Kjvz5w2xvaxgXXJHcQAIl0FFMm5DsUMjoV7tAubNUv0bg0X9HjHuFdYL9rgHChkb1aZufIgR82o6eRkqH_EcqV3pwu2ihe5MoEoCeTc5gmXiiVijVUq-Z35T7kHszejllB17-386vtCIKUWhSRhG-J7VwGrwVbFfKm4wP3Ph8sAyCGXpukwFlfrrS62Jh2rgBFyVUpcY_a21wSwJ6y_LH49g'
        auth = executive_producer
    if (role == 'ca'):
        casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNjV0szM2VDZkN4VHczMUo2aHFsWiJ9.eyJpc3MiOiJodHRwczovL2ZhbGJlbGxhaWhpMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY2NWYyOWEyNWRkMTQwMDc4ZmY0MzFiIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTYwMTA0NTgwOSwiZXhwIjoxNjAxMTMyMjA5LCJhenAiOiJwRXZvczNvNVpHNk1UaVRTUWFUMTJoRE5PRXNHSklqUiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.jT4Me3t0HgO2pHwTAWfBfOT79aenDdBIIdBMSjLvBr8T7zSRoIK5xgXPl2SL5N6MatEYurrX9uo0O4TzLDm4W1UgkIse72XT6fz_tMIAv77fht7T5DDurAVqFxuyfxsKUdZ_ULcv7Rk32b_t4INPQp9-dK5reJzBmwmMN3_-l5YimaWwaeeoCCfMOLU-eQrZOhG7fxKn8CdJSwT3LSFes5cbJ2hCcbaaP3BfcvosHCML4Q1xwJSwq2JKhWWGFBB3L_v0yMosVd_0PWeVynCCAZrXm3fWy6HyLeg6y2Ho2WbBgDTGuR1d4FCV4bkqtJ2JQu9s6buJ__OCYfj8Peu8xw'
        auth = casting_assistant
    if (role == 'cd'):
        casting_director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNjV0szM2VDZkN4VHczMUo2aHFsWiJ9.eyJpc3MiOiJodHRwczovL2ZhbGJlbGxhaWhpMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY2NWYyNDM4MTU1MWYwMDZlNDE2OGJiIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTYwMTA0NTg0NywiZXhwIjoxNjAxMTMyMjQ3LCJhenAiOiJwRXZvczNvNVpHNk1UaVRTUWFUMTJoRE5PRXNHSklqUiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.FVTS8wak711VwbUQUHdIau02eRUxXf_u4aDGEGNGO50gLsR3VQ9NawBw8E0TI4AKjPJC1tyT72zhjGP4sCv7kMbzJSxFF7p--g8DtsWbvtCYWKKAqpcG65IEmx_L_bCMtzyA1LSoBvk_jChKyt-QPfQAA3suv-hLcjkiNpmpveosSG9PZ6XTNn8JAAe1b2vXwOGzza4FgxrIxMS_oBT52TAhYmlp6uHTwjUO0zck7xg3jN78xv_9ge4nCJ39YAymxhOb1kucIaaZzGRU91OXNDGs3VuefrXjrs5JJDQzuPlYR_3efA5zA0CWrP5JmlywAJiTebB3UtiJ9aBk7wNocQ'
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
