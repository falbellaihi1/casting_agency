
import os
import unittest
import json
from app import create_app
from models import setup_db, Actors, db, Movies


def get_headers():
    auth = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNjV0szM2VDZkN4VHczMUo2aHFsWiJ9.eyJpc3MiOiJodHRwczovL2ZhbGJlbGxhaWhpMS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDQ5NzkyMDQ1NjEyNDY5MjgxNzAiLCJhdWQiOlsiY2FzdGluZ2FnZW5jeSIsImh0dHBzOi8vZmFsYmVsbGFpaGkxLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDA0Njc1MTUsImV4cCI6MTYwMDU1MzkxMiwiYXpwIjoicEV2b3MzbzVaRzZNVGlUU1FhVDEyaEROT0VzR0pJalIiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.XhLVmIbhrTkw9P9iuEpfbsbdRyjp7o5i1GnkDNsHXQT6aYpALm1lCiBsl5hbLIIYwqwZRBdCdYJQpkdgVxE4JSQ_ODR6uSf72YCaNUv9nctuwi1Llsybe2c_xI8nIn--zgPOJD0dih2y37NfXnzpCCDrwaoQiTc7zNadVAq15_1wYvxNCMf7I9OQzqfn1U0y2vsoiYt2AUJO730ROjmkn1bkmjE0754pKjBFtLIBxFAun0mtWBjtm8OFq8eXNnwy-FnrWty57ceXc8LKHz_oMQBxSH0Nudn8_U51k2uelXlG3pCyk0nZtny4dus5p9UiFcFRLpgypw-VJyMvbg8hAw'
    headers = {'authorization': 'Bearer {}'.format(auth)}

    return headers

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency  test case"""

    print('init')


    @classmethod
    def setUpClass(self):
        """Excuted in the beginning of the test, the target of this test is that all tests run in order at once """
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://postgres:0000@{}/{}".format('localhost:5432', self.database_name)

        # binds the app to the current context
        self.new_actor = {"name":"Markos24", "age":23, "gender":"Male"}
        self.new_movie = {"title":"the real stuff", "release_date":"08/20/2020"}
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            print('tst')
            db.init_app(self.app)
            # create all tables
            db.drop_all()
            db.create_all()



    def setUp(self):
        """Executed before reach test"""

    def tearDown(self):
        """Executed after reach test"""


    def test_a_get_movies(self):

        """Testing get movies"""
        print('get movies')
        res = self.client().get('/movies', headers=get_headers())
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_b_get_actors(self):
        """Testing get actors"""
        print('get actor')
        res = self.client().get('/actors', headers=get_headers())
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_c_create_actors(self):
        """Testing create actor, if success, actor should be created in db"""
        print('create actor')
        res = self.client().post('/actors', json=self.new_actor, headers=get_headers())
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_d_create_movie(self):
        """Testing create actor, if success, actor should be created in db"""
        print('create movie')
        res = self.client().post('/movies', json=self.new_movie, headers=get_headers())
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_e_edit_actor(self):
        """Testing edit actor, if success, actor should be edited in db"""
        print('edit actor ')
        res = self.client().patch('/actors/1', json={"name":"new edited name", "email":"new edited email"}, headers=get_headers())
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_f_edit_movie(self):
        print('edit movie')
        """Testing edit actor movie, if success, actor should be edited in db"""
        res = self.client().patch('/movies/1', json={"title":"new edited title", "release_date":"08/20/2020"}, headers=get_headers())
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    def test_g_delete_movie(self):
        """Testing delete movie method, this test should delete the movie from  db, if success it will return 200"""
        print('delete')
        res = self.client().delete('/movie/1', headers=get_headers())

        data = json.loads(res.data)
        print(data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(movie,None)


    def test_h_delete_actor(self):
        """Testing delete actor method, this test should delete the actor from  db, if suceess it will return 200"""
        print('delete')
        res = self.client().delete('/actor/1', headers=get_headers())
        data = json.loads(res.data)
        print(data)
        actor = Actors.query.filter(Actors.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(actor,None)

if __name__ == "__main__":
    unittest.main()