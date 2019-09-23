""" Flask webapp building the backend of a small website.

Allow users to search for letters in a phrase.
Store requests in a databse and render as human-readable html.

How to invoke:
    >>>> python vsearch4web.py
"""
from time import sleep
from threading import Thread
from flask import Flask, render_template, request, session, copy_current_request_context
from vsearch import search_4_letters
from db_cm import UseDatabase, ConnectionError, CredentialsError, SQLError
from checker import check_logged_in


app = Flask(__name__)
app.secret_key = "astaLaOsoBebe49!"

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'quakA!',
                          'database': 'vsearchlogDB', }


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    """Perform search for letters in phrase and render results on screen.

    The user enters a phrase and letters in a form. Extract data from form,
    call search_4_letters on it to compute the contained letters.
    Render results.
    Catch various likely errors and log them in the terminal. Hide scary error
    messages from user.
    """
    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        """Write the request and the results returned by
           search_4_letters to a mysql database.
        """
        sleep(15)  # line mimicks delay of database
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
    title = 'Your search results!'
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search_4_letters(phrase, letters))
    try:
        t = Thread(target=log_request, args=(request, results))
        t.start()
    except Exception as err:
        print('****** Logging failed with this error: ', str(err))
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
@check_logged_in
def view_the_log() -> 'html':
    """Display the request data in a human readable html table.
    Catch various error messages and log them on the terminal. Hide scary error
    messages from user.
    """
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            sql = """select phrase, letters, ip, browser_string, results
            from log
            """
            # contents is a list of tuples
            cursor.execute(sql)
            contents = cursor.fetchall()
            # contents_escaped = [[escape(entry) for entry in tuple]
            #                    for tuple in contents]

        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template(
            'viewlog.html',
            the_title='View Log',
            the_row_titles=titles,
            the_data=contents)

    except ConnectionError as err:
        print('Database switched on? Err: ', str(err))
    except CredentialsError as err:
        print('Password and/ or username seem to be incorrect. Err: ',
              str(err))
    except SQLError as err:
        print('The SQL code has errors. Err: ', str(err))
    except Exception as err:
        print('Sth went wrong.', str(err))
    return 'Error'


@app.route('/login')
def do_login() -> str:
    """Perform user login."""
    session['logged_in'] = True
    return 'You are now logged in.'


@app.route('/logout')
def do_logout() -> str:
    """Perform user logout."""
    session.pop('logged_in')
    return 'You are now logged out.'


if __name__ == '__main__':
    app.run(debug=True)
