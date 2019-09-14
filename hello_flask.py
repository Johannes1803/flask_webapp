from flask import Flask
from vsearch import search_4_letters

app = Flask(__name__)

@app.route('/')
def hello() -> str:
    return 'Hello World from Flask!'

@app.route('/search4')
def do_search() -> str:
    return str(search_4_letters('life, the universe and everything!', 'eiru, !'))

app.run()
