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
  cors = CORS(app)

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
    all_categories = Category.query.all()
    formatted_categories = {category.id : category.type for category in all_categories}
    return jsonify({
      'success': True,
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
  @app.route('/questions', methods=["GET"])
  def get_questions():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = {category.id : category.type for category in categories}
    questions = Question.query.order_by(Question.id).all()
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + QUESTIONS_PER_PAGE
    paginated_questions = []
    for question in questions:
      paginated_questions.append(question.format())

    return jsonify({
      'success': True,
      'questions': paginated_questions[start:end],
      'totalQuestions': len(questions),
      'categories': formatted_categories,
      'currentCategory': None
    })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    question = Question.query.filter_by(id=id).first()
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
  @app.route('/questions', methods=["POST"])
  def post_questions():
    page = request.args.get('page', 1, type=int)
    body = request.get_json()
    question = body.get('question')
    answer = body.get('answer')
    difficulty = body.get('difficulty')
    category = body.get('category')
    search_string = body.get("searchTerm")

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    if search_string != None:
      start = (page - 1) * 10
      end = QUESTIONS_PER_PAGE
      questions = Question.query.filter(Question.question.ilike('%' + search_string + '%')).all()
      formatted_questions = []

      for question in questions:
        formatted_questions.append(question.format())

      return jsonify({
        'success' : True,
        'questions': formatted_questions[start:end],
        'total_questions': len(questions),
        'current_category': None
      })
    else:
      question = Question(question = question, answer = answer, difficulty = difficulty, category = category)

      question.insert()

      return jsonify({
        'success': True,
      })
    

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def questions_by_category(id):
    page = request.args.get('page', 1, type=int)
    questions = Question.query.filter_by(category=id).all()
    start = (page - 1) * 10
    end = QUESTIONS_PER_PAGE

    formatted_questions = []
    for question in questions:
      formatted_questions.append(question.format())

    return jsonify({
      'success': True,
      'questions': formatted_questions[start:end],
      'totalQuestions': len(questions),
      'currentCategory':id,
    })


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
  @app.route('/quizzes', methods=['POST'])
  def play():
    body = request.get_json()
    previous_questions = body.get('previous_questions')
    quiz_category = body.get('quiz_category')
    quiz_category_id = int(quiz_category['id'])
    available_questions = []

    if quiz_category_id == 0:
      questions = Question.query.all()
    else:
      questions = Question.query.filter_by(category = quiz_category_id).all()

    if len(previous_questions) == 0:
      for question in questions:
        available_questions.append(question.format())
    
    elif len(previous_questions) != 0:
      for question in questions:
        if question.id not in previous_questions:
          available_questions.append(question.format())

    if len(available_questions) != 0:
      current_question = random.choice(available_questions)
    else:
      current_question = False

    return jsonify({
      'success': True,
      'question': current_question
    })

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

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'This method is not allowed',
    }), 405


  return app

    