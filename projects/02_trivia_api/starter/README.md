# Full Stack API Final Project


## Full Stack Trivia

This Trivia project made by udacity allows users to play a trivia game. Students in the FSND program were tasked to structure plan, implement, and test an API allowing it to perfoarm the following: 

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


## Getting Started

### install dependinces
This project requires the installation of pip3, python3, Nodejs and Node Package Manager (NPM). 

### Backend
The [./backend](https://github.com/acrawan/FSND/tree/master/projects/02_trivia_api/starter/backend/README.md) directory contains a completed Flask and SQLAlchemy server. 
Please refer to the instructions provided by udacity at [README within ./backend](./backend/README.md) regardig the set up of the backend. 
to run the backend: 
```bash
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development # enables debug mode
$ flask run
``` 
### Frontend

The [./frontend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. 
Please refer to the instructions provided by udacity at [README within ./frontend](./frontend/README.md) regardig the set up of the frontend. 
to start the project: 
```bash
npm start
```

## Endpoints

#### GET '/categories'

```bash 
Sample: curl http://127.0.0.1:5000/categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET '/questions?page=${integer}'

```bash 
Sample: 
- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories. 
{
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

#### GET '/categories/${id}/questions'

``` bash
Sample: curl http://127.0.0.1:5000/categories/6/questions
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string
{
  "current_category": "Sports",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

#### POST '/questions'

```bash 
Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": " Would you weigh more or less on Mars?", "answer": "less", "difficulty": 1, "category": "1" }'
- Sends a post request in order to **add a new question**
- Request Body: 
{
    'question':  'Would you weigh more or less on Mars?',
    'answer':  'less',
    'difficulty': 1,
    'category': 1,
}
- Returns: returns the total number of questions and id of added question. 
{
  "created": 24, 
  "success": true,
  "total_questions": 20
}
```

#### DELETE '/questions/${id}'

```bash 
Sample: curl -X DELETE http://127.0.0.1:5000/questions/24
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: returns the id of the question deleted.
{
  "deleted": 24,
  "success": true,
  "total_questions": 19
}
```

#### POST '/questions'

```bash 
Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "palace"}'
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
{
    'searchTerm': 'palace'
}
- Returns: any array of questions, a number of totalQuestions that met the search term
{
  "questions": [
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### POST '/quizzes'

```bash 
Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [13, 15], "quiz_category": {"type": "Geography", "id": "3"}}'
- Sends a post request in order to get the next question 
- Request Body: 
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
- Returns: a single new question object 
{
  "question": {
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
  },
  "success": true
}
```

## contributers
- 
