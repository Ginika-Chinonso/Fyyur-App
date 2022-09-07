import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources = {r"*/api/*":{"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    all_questions = Question.query.all()
    formatted_questions = {question.format() for question in all_questions}
    all_categories = Category.query.all()
    formatted_categories = {category.format() for category in all_categories}
    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'categories': formatted_categories
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET', ['POST']])
  def get_questions():
    if request.method == 'GET':
      page = request.args.get('page', 1, type=int)
      categories = Category.query.all()
      formatted_categories = {category.format() for category in categories}
      questions = Question.query.all()
      formatted_questions = {question.format() for question in questions}
      return jsonify({
        'success': True,
        'questions': formatted_questions,
        # 'totalQuestions': len(questions),
        'categories': formatted_categories,
        # 'currentCategory': 2
      })
    
    if request.method == 'POST':
      question = request.json.data('question')
      answer = request.json.data('answer')
      difficulty = request.json.data('difficulty')
      category = request.json.data('category')

      question = Question(question = question, answer = answer, difficulty = difficulty, category = category)

      question.insert()

      return jsonify({
        'success': True,
      })






  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    question = Question.query.filter_by(id=id).all()
    question.delete()

    return jsonify({
      'success': True,
      'question_id': question.id,
      'message': 'This question has been deleted'
    })




  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/add', methods=['POST'])
  def add_question():
    question = request.get_json()['question']
    answer = request.get_json()['answer']
    difficulty = request.get_json()['difficulty']
    category = request.get_json()['category']

    question = Question(question = question, answer = answer, difficulty = difficulty, category = category)
    categories = Category.query.all()
    formatted_categories = {category.format() for category in categories}

    question.insert()

    return jsonify({
      'success': True,
      'categories': formatted_categories
    })
    






  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # @app.route('/questions/', methods=['POST'])
  # def search():
  #   search_string = request.query_string()
  #   question = Question.query.filter_by(Question.question.ilike('%' + search_string + '%')).all()

  #   return jsonify({
  #     'question': question
  #   })



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'This resource was not found'
    }), 404
  

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'This request can not be processed'
    }), 422

  return app

    