import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format('postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.question = {"question":"Name an African country in West Africa you know", "answer":"Nigeria", "difficulty":"1", "category":"3"}
        self.searchTerm = {"searchTerm":"team"}
        self.quizParam = {"previous_questions":[], "quiz_category": {"type":"Science", "id":"1"}}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_categories_endpoint(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)

    def test_questions_enpoint(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

    def test_search_endpoint(self):
        res = self.client().post('/questions', json=self.searchTerm)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_question(self):
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)
        self.assertTrue(data['success'])

    def test_questions_by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        self.assertTrue(data['success'])

    def test_quizzes_endpoint(self):
        res = self.client().post('/quizzes', json=self.quizParam)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_not_found(self):
        res = self.client().get('/question')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 404)

    def test_unprocessable(self):
        res = self.client().post('/questions/3')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()