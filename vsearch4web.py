from flask import Flask, render_template, request, escape
from vsearch import search_4_letters
from DBcm import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'quakA!',
                          'database': 'vsearchlogDB', }


def log_request(req: 'flask_request', res: str) -> None:
    """Write the request and the results returned by
       search_4_letters to a mysql database.
    """
    with UseDatabase(app.config['dbconfig']) as cursor:
        # the string representing the sql query
        sql = """
                insert into log
                (phrase, letters, ip, browser_string, results)
                values
                (%s, %s, %s, %s, %s)"""
        # the values substituted into the query string
        sql_tuple = (req.form['phrase'], req.form['letters'],
                     req.remote_addr, req.user_agent.browser, res, )
        # perform query
        cursor.execute(sql, sql_tuple)


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
    rendered = render_template(
        'results.html',
        the_title=title,
        the_phrase=phrase,
        the_letters=letters,
        the_results=results)

    return rendered


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
def view_the_log() -> 'html':
    """Display the request data in a human readable html table."""
    with UseDatabase(app.config['dbconfig']) as cursor:
        sql = """select phrase, letters, ip, browser_string, results
        from log
        """
        # contents is a list of tuples
        cursor.execute(sql)
        contents = cursor.fetchall()

    titles = ('Phrase','Letters', 'Remote_addr', 'User_agent', 'Results')
    return render_template(
        'viewlog.html',
        the_title='View Log',
        the_row_titles=titles,
        the_data=contents)


if __name__ == '__main__':
    app.run(debug=True)
