import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

database_path = os.environ['TEST_DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

test_token = os.environ['TEST_TOKEN']


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.headers = {'Authorization': f'Bearer {test_token}'}

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client().get("/movies", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_get_actors(self):
        res = self.client().get("/actors", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_404_get_actors_typo(self):
        res = self.client().get("/acters", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_add_new_movie(self):
        res = self.client().post('/movies', headers=self.headers, json={
            "title": "Silenced",
            "release_date": "2011"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_add_new_actor(self):
        res = self.client().post('/actors', headers=self.headers, json={
            "name": "Gong Yoo",
            "age": 39,
            "gender": "male",
            "movie_id": 7,
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_400_missing_value_in_add_movie(self):
        res = self.client().post('/movies', headers=self.headers, json={
            "title": "Silenced",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "bad request")

    def test_400_missing_value_in_add_actor(self):
        res = self.client().post('/actors', headers=self.headers, json={
            "name": "Gong Yoo",
            "age": 39,
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "bad request")

    def test_edit_movie(self):
        res = self.client().patch("/movies/1", headers=self.headers, json={
            "title": "Leon"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_edit_actor(self):
        res = self.client().patch("/actors/1", headers=self.headers, json={
            "age": "40"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_actor_is_none_in_edit_actor(self):
        res = self.client().patch("/actors/1000", headers=self.headers, json={
            "age": "40"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_404_movie_is_none_in_edit_movie(self):
        res = self.client().patch("/movies/1000", headers=self.headers, json={
            "release_date": "1999"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_movie(self):
        res = self.client().delete("/movies/3", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 3)

    def test_delete_actor(self):
        res = self.client().delete("/actors/4", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 4)

    def test_404_if_movie_does_not_exist(self):
        res = self.client().delete("/movies/1000", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_404_if_actor_does_not_exist(self):
        res = self.client().delete("/actors/1000", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
