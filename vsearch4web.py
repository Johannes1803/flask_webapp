from flask import Flask, render_template, request, escape
from vsearch import search_4_letters

app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    """Write the request and the results returned by search_4_letters to a log file.
    """
    with open('vsearch.log', 'a') as log:
        print(str(dir(req)), res, file=log)


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    """Perform search for letters and render results on screen.

    The user enters letters to look for and the phrase to be searched.
    Use data from request, compute the result in search_4_results and
    render results ons screen.
    """
    title = 'Your search results!'
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search_4_letters(phrase, letters))
    log_request(request, results)
    return render_template(
                    'results.html', the_title=title,
                    the_phrase=phrase,
                    the_letters=letters,
                    the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    """Render entry page on screen.

    Provide form element for user to enter search request.
    """
    return render_template(
                        'entry.html',
                        the_title='Welcome to search 4 letters on the web!')

@app.route('/viewlog')
def view_the_log() -> str:
    with open('vsearch.log') as log:
        contents = log.read()
    return escape(contents)


if __name__ == '__main__':
    app.run(debug=True)
