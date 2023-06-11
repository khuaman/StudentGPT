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


@app.get('/api/questions')
def get_questions():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM questions')
    questions = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(questions)


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


@app.route('/')
def home():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(debug=True, port=4000)