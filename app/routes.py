from flask import render_template, request, Response, g
from app import app, db_connect

@app.before_request
def before_request():
    # Initiates db connection
    g.connect = db_connect.Connect('my_psswd~')
    g.database, g.cursor = g.connect.connect()

@app.after_request
def after_request(response):
    g.database.close()
    return response

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/entry')
def entry():
    return render_template('entry.html')

@app.route('/entry', methods=['POST'])
def entry_post():
    entry = request.get_json()
    reply = g.connect.entry(entry)
    return reply

@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def search_post():
    post_response = request.get_json()
    response_header = list(post_response)[0]
    db_response = "None"
    try:
        db_response = {
            'search': g.connect.retrieve,
            'deleteEntry': g.connect.delete_entry
        }[response_header](post_response[response_header])
    except Exception as e:
        print("Error: {}".format(e))
    return db_response
