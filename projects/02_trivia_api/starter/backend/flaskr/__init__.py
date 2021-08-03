import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,questions):

  page = request.args.get('page', 1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE 
  end = start + QUESTIONS_PER_PAGE

  formatted_questions = [question.format() for question in questions]
  all_questions = formatted_questions[start:end]

  return all_questions
    

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @----------------TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app)

  '''
  @-----------------TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
 @-----------------TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():

    categories = Category.query.order_by(Category.type).all()

    if len(categories) == 0:
      abort(404)

    categories_list= {}
    for category in categories:
      categories_list[category.id] = category.type

    return jsonify({
      'success': True,
      'categories': categories_list
    }), 200


  '''
  @-----------------TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def retrieve_questions():

    questions = Question.query.order_by(Question.id).all()
    all_questions = paginate_questions(request, questions)
    if len(all_questions) == 0:
      abort(404)

    categories = Category.query.all()
    categories_list = {}
    for category in categories:
      categories_list[category.id] = category.type

    return jsonify({
      'success': True,
      'questions': all_questions,
      'total_questions': len(Question.query.all()),
      'categories': categories_list
    }), 200


  '''
  @-----------------TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id): 

    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      
      return jsonify({
        'success': True,
        'deleted': question_id, 
        'total_questions': len(Question.query.all())
      }), 200

    except:
      abort(422)

  '''
  @-----------------TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  ''' 
  '''
  @-----------------TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question(): 

    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty=  body.get('difficulty', None)
    search_term = body.get('searchTerm', None)

    try:               
      if search_term is not None:
        if search_term.isspace() or search_term=='': 
          raise

        search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        if (len(search_results) == 0):
          abort(404)

        questions = paginate_questions(request, search_results)

        return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(search_results)
        }), 200

      else: 

        if(not(new_question and new_answer and new_category and new_difficulty)):
          abort(404)
      
        question = Question(question= new_question, answer=new_answer, category=new_category, difficulty= new_difficulty )
        question.insert()

        questions = Question.query.order_by(Question.id).all()
        all_questions = paginate_questions(request, questions)

        return jsonify({
          'success': True,
          'created': question.id,
          'total_questions': len(Question.query.all())
        })

    except:
      abort(422)


  '''
  
 @-----------------TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def category_questions(category_id): 

    try: 
      category = Category.query.filter(Category.id == category_id).one_or_none()
      if (category is None):
        abort(404)

    
      questions = Question.query.filter(Question.category == category.id).all()
      all_questions = paginate_questions(request, questions)

      return jsonify({
        'success': True,
        'questions': all_questions,
        'total_questions': len(questions), 
        'current_category': category.type
      }), 200

    except: 
      abort(422)


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
  def play_quiz(): 

    body = request.get_json()
    previous_questions = body['previous_questions']
    quiz_category = body['quiz_category']

    if ((quiz_category is None) or (previous_questions is None)):
      abort(404)

    try:   

      if quiz_category['id']==0:
        questions= Question.query.all()
      else: 
        questions = Question.query.filter(Question.category == quiz_category['id']).all()

      formatted_questions = [question.format() for question in questions]

      new_questions= []      

      for question in formatted_questions:
        if question['id'] not in previous_questions:
          new_questions.append(question)

      next_question= None

      if len(new_questions) > 0:
        next_question = random.choice(new_questions)

      return jsonify({
        'success': True,
        'question': next_question
      }), 200

    
    except: 
      abort(422)
      

  '''

  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422
  
  return app

    