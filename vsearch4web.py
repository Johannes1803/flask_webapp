from flask import Flask,render_template, request
from vsearch import search_4_letters

app = Flask(__name__)


@app.route('/search4', methods=['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search_4_letters(phrase, letters))
    return render_template( 'results.html',
                            the_title='Your search results!',
                            the_phrase=phrase,
                            the_letters=letters,
                            the_results=results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                            the_title='Welcome to search 4 letters on the web!')

app.run(debug=True)
