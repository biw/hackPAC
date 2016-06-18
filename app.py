import forms  # this is the local file forms.py

import sqlite3
import logging
import os
import json

from werkzeug.serving import run_simple
from flask import Flask, render_template, request
from flask_api import status
from logging import Formatter, FileHandler


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
basedir = os.path.abspath(os.path.dirname(__file__))
db_url = os.path.join(basedir, 'database.db')

# Login required decorator.
#
# def login_required(test):
#    @wraps(test)
#    def wrap(*args, **kwargs):
#        if 'logged_in' in session:
#            return test(*args, **kwargs)
#        else:
#            flash('You need to login first.')
#            return redirect(url_for('login'))
#    return wrap
#
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    # create_posts()
    posts = get_posts_2()
    return render_template('pages/placeholder.home.html', posts=posts)


@app.route('/dashboard')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = forms.LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = forms.RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = forms.ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


# route to change which post the user is voting for
@app.route("/api/vote", methods=["POST"])
def vote():

    conn = sqlite3.connect(db_url)
    # try to parse the form inputs as an int
    # if something is not correct, return a 400
    try:
        vote_id = int(request.form["vote_id"])
        user_id = int(request.form["user_id"])
    except:
        return "", status.HTTP_400_BAD_REQUEST

    # create a cursor to edit the database
    cursor = conn.cursor()

    # update the vote of the user
    cursor.execute('''UPDATE users SET vote_id=? WHERE user_id=?''',
                   (vote_id, user_id,))

    # commit the change to the db
    cursor.close()
    conn.commit()
    conn.close()

    # return 202
    return "", status.HTTP_202_ACCEPTED


# route to get the most recent posts
@app.route("/api/get_posts", methods=["GET"])
def get_posts():

    conn = sqlite3.connect(db_url)
    # to start: we are only going to be able to query this to get the
    # top voted posts (in the future we may add more ways)
    try:
        print(request.args.get)
        count = int(request.args.get("count"))
    except:
        return "", status.HTTP_400_BAD_REQUEST

    cursor = conn.cursor()

    cursor.execute('''SELECT id, user_id, url,
        description, vote_count FROM posts ORDER BY vote_count DESC
        LIMIT ?''', (count,))

    results = cursor.fetchall()
    conn.close()

    return json.dumps(results, sort_keys=True,
                      indent=4, separators=(",", ": ")),
    status.HTTP_202_ACCEPTED


@app.route("/api/get_post", methods=["GET"])
def get_post():

    conn = sqlite3.connect(db_url)
    try:
        post_id = int(request.args.get("post_id"))
    except:
        return "", status.HTTP_400_BAD_REQUEST

    cursor = conn.cursor()

    cursor.execute('''SELECT id, user_id, url, description, vote_count FROM
        posts WHERE id=?''', (post_id,))

    results = cursor.fetchone()
    conn.close()

    return json.dumps(results, sort_keys=True,
                      indent=4, separators=(",", ": ")),
    status.HTTP_202_ACCEPTED


@app.route("/api/get_user_post", methods=["GET"])
def get_user_post():

    conn = sqlite3.connect(db_url)
    try:
        user_id = int(request.args.get("user_id"))
    except:
        return "", status.HTTP_400_BAD_REQUEST

    cursor = conn.cursor()

    cursor.execute('''SELECT id, user_id, url, description, vote_count FROM
        posts WHERE user_id=?''', (user_id,))

    results = cursor.fetchone()
    conn.close()

    return json.dumps(results, sort_keys=True,
                      indent=4, separators=(",", ": ")),
    status.HTTP_202_ACCEPTED


@app.route("/api/create_post", methods=["POST"])
def create_post():

    conn = sqlite3.connect(db_url)
    try:
        post_url = request.form["post_url"]
        user_id = int(request.form["user_id"])
    except:
        return "", status.HTTP_400_BAD_REQUEST

    conn.close()
    return None


def get_posts_2():

    conn = sqlite3.connect(db_url)
    # to start: we are only going to be able to query this to get the
    # top voted posts (in the future we may add more ways)
    # try:
    #     print(request.args.get)
    #     count = int(request.args.get("count"))
    # except:
    #     return "", status.HTTP_400_BAD_REQUEST

    count = 9

    cursor = conn.cursor()

    cursor.execute('''SELECT id, user_id, url,
        description, vote_count FROM posts ORDER BY vote_count DESC
        LIMIT ? , ?''', (2,count))

    results = cursor.fetchall()
    conn.close()
    print results
    return results,
    status.HTTP_202_ACCEPTED

def create_posts():
    db = sqlite3.connect(db_url);
    db.execute('''INSERT INTO posts (user_id, url, description, vote_count) VALUES (?,?,?,?) ''', [1, 'https://www.nrdc.org/issues/water-pollution', "It's about time we got serious about drinking water", 102])
    db.execute('''INSERT INTO posts (user_id, url, description, vote_count) VALUES (?,?,?,?) ''', [2, 'http://www.cnn.com', "Iowa is about to stop paying for the homeless. WTF", 99])
    
    db.commit()
# @app.route
# # Error handlers.
# @app.errorhandler(500)
# def internal_error(error):
#     # db_session.rollback()
#     return render_template('errors/500.html'), 500


# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('errors/404.html'), 404

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    run_simple("0.0.0.0", 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)
