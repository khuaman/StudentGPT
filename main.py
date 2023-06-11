from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras
from os import environ
from dotenv import load_dotenv

import openai

load_dotenv()


app = Flask(__name__)


DATABASE_URL = environ.get('DATABASE_URL')
API_KEY = environ.get('API_KEY')
openai.api_key = API_KEY  # Reemplaza con tu clave de API de OpenAI, no dejes la mia que se acaba mi saldo :(

def get_db_connection():
    conn = connect(DATABASE_URL)
    return conn

from flask import Flask, render_template, request
import openai

app = Flask(__name__)
openai.api_key = API_KEY
conversations = []

"""
    This function retrieves all questions from a database and returns them as a JSON object.
    :return: A JSON representation of all the rows in the "questions" table of the database.
"""
@app.get('/api/questions')
def get_questions():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM questions')
    questions = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(questions)

"""
    This function creates a new question and generates an answer using OpenAI's API, then stores the
    question and answer in a database and returns the newly created question.
    :return: The function `create_questions()` creates a new question by receiving a JSON object with
    the question and the desired model to use for generating the answer. If the model is not one of the
    possible models, it defaults to `text-davinci-003`. The function then uses OpenAI's API to generate
    an answer to the question using the specified model. The answer is then inserted into a database
    table
    """
@app.post('/api/questions')
def create_questions():
    new_question = request.get_json()
    question = new_question['question']
    posible_models = ['gpt-4', 'gpt-3.5-turbo', 'text-davinci-003', 'code-davinci-edit-001']
    model = new_question['model']

    if model not in posible_models:
        model = posible_models[2]

    response = openai.Completion.create(
        engine = model,
        prompt = question,
        temperature = 0.5,
        max_tokens = 150,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0.6
    )
    
    answer = response.choices[0].text.strip()

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('INSERT INTO questions (question, answer) VALUES (%s, %s) RETURNING *', 
                (question, answer))
    new_create_question  = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_create_question)

"""
    This function deletes a question from a database by its ID and returns the deleted question as a
    JSON object.
    
    :param id: The id parameter is a variable that represents the unique identifier of the question that
    needs to be deleted from the database. It is passed as a parameter in the URL of the API endpoint
    :return: This code is implementing a DELETE endpoint for a Flask API that deletes a question from a
    database based on its ID. The function returns a JSON response containing the deleted question if it
    exists in the database, or a message indicating that the question was not found if it does not
    exist.
    """
@app.delete('/api/questions/<id>')
def delete_question(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('DELETE FROM questions WHERE id = %s RETURNING *', (id, ))
    question = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if question is None:
        return jsonify({'message' : 'Question not found'}), 404
    
    return jsonify(question)

"""
    This function retrieves a question from a database by its ID and returns it as a JSON object.
    
    :param id: The parameter `id` is a variable that represents the unique identifier of a question in
    the database. It is used in the URL path to retrieve a specific question by its ID
    :return: The function `get_questions_by_id` returns a JSON representation of a single question from
    the database with the specified `id`. If the question is not found, it returns a JSON error message
    with a 404 status code.
"""
@app.get('/api/questions/<id>')  
def get_questions_by_id(id):
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM questions WHERE id = %s', (id, ))
    question = cur.fetchone()

    #Validando por si no existe el registro
    if question is None:
        return jsonify({'message' : 'Question not found'}), 404
    
    return jsonify(question)

"""
    This function returns the index.html file located in the static folder when the user navigates to
    the home route.
    :return: The `home()` function returns the contents of the `index.html` file located in the `static`
    folder.
"""
@app.route('/')
def home():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(debug=True, port=4000)