from flask import Flask, request, jsonify
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
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    if request.form['question']:
        question = 'Yo: ' + request.form['question']

        response = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = question,
            temperature = 0.5,
            max_tokens = 150,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0.6
        )

        answer = 'AI: ' + response.choices[0].text.strip()

        conversations.append(question)
        conversations.append(answer)

        return render_template('index.html', chat = conversations)
    else:
        return render_template('index.html')

    

if __name__ == '__main__':
    app.run(debug=True, port=4000)