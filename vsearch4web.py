from flask import Flask, render_template, request
from vsearch import search_4_letters

app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req, res, file=log)


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search_4_letters(phrase, letters))
    return render_template(
                    'results.html', the_title='Your search results!',
                    the_phrase=phrase,
                    the_letters=letters,
                    the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template(
                        'entry.html',
                        the_title='Welcome to search 4 letters on the web!')


if __name__ == '__main__':
    app.run(debug=True)
