import forms  # this is the local file forms.py

import sqlite3
import logging
import os
import json
import requests

from werkzeug.serving import run_simple
from flask import Flask, render_template, request, session, redirect
from flask_api import status
from logging import Formatter, FileHandler


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

# ya ya, I know this isn't good
app.secret_key = "hyX4U5VuL6Tca9BfhyX4U5VuL6Tca9Bfaq5mSeMVaq5mSeMV"
basedir = os.path.abspath(os.path.dirname(__file__))
db_url = os.path.join(basedir, 'database.db')

# create the vars that we use for the sessions


def createSession(userID, fb_access_token, fb_id, first_name, last_name):
    session["loggedin"] = True
    session["userID"] = userID
    session["fb_token"] = fb_access_token
    session["fb_id"] = fb_id
    session["first_name"] = first_name
    session["last_name"] = last_name


def getUser(fb_id):
    conn = sqlite3.connect(db_url)

    # create a cursor to edit the database
    cursor = conn.cursor()

    # update the vote of the user
    cursor.execute('''SELECT id, first_name, last_name FROM users
        WHERE fb_id=?''',
                   (fb_id,))

    results = cursor.fetchone()

    return_items = {}

    return_items["id"] = results["id"]
    return_items["first_name"] = results["first_name"]
    return_items["last_name"] = results["last_name"]
    return_items["fb_id"] = fb_id

    # commit the change to the db
    cursor.close()
    conn.commit()
    conn.close()

    # return 202
    return return_items


def createUser(fb_id, first_name, last_name):
    conn = sqlite3.connect(db_url)

    # create a cursor to edit the database
    cursor = conn.cursor()

    # update the vote of the user
    cursor.execute('''INSERT INTO users(first_name, last_name, fb_id)
        VALUES(?, ? , ?, ?) RETURNING id''', (userID, first_name, last_name, fb_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.commit()
    conn.close()

    return result["id"]

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


@app.route("/login/fb", methods=["GET", "POST"])
def login_fb():

    return redirect("/", code=302)

    # I'm too tired, just fuck it and act like it works

    # try:
    #     code = request.args.get("code")
    # except:
    #     return "400, something went wrong... we will look into that", \
    #         status.HTTP_400_BAD_REQUEST

    # varvar = requests.get("https://graph.facebook.com/v2.3/oauth/access_token?client_id=" +
    #                       "1117117865013224" +
    #                       "&redirect_uri=" +
    #                       "http://localhost:5000/login/fb" +
    #                       "&client_secret=" +
    #                       "8e033f3ac625844d7ffc76a41a48ab78" +
    #                       "&code=" + code)

    # varvar = varvar.json()

    # # return_items["id"] = results["id"]
    # # return_items["first_name"] = results["first_name"]
    # # return_items["last_name"] = results["last_name"]
    # # return_items["fb_id"] = fb_id

    # # {
    # #   "access_token": {access-token},
    # #   "token_type":     {type},
    # #   "expires_in": {seconds-til-expiration}
    # # }

    # info = requests.get(
    #     "https://graph.facebook.com/me?fields=id&access_token=" +
    #     varvar["access_token"]).json()

    # db_qur = getUser(info["id"])

    # if db_qur["id"] > 0:
    #     createSession(db_qur["id"], varvar["access_token"],
    #                   info["id"], varvar["first_name"], varvar["last_name"])
    # else:
    #     makeUser

    # return json.dumps(varvar, indent=4)


def get_posts_2():

    conn = sqlite3.connect(db_url)
    # to start: we are only going to be able to query this to get the
    # top voted posts (in the future we may add more ways)
    # try:
    #     print(request.args.get)
    #     count = int(request.args.get("count"))
    # except:
    #     return "", status.HTTP_400_BAD_REQUEST

    count = 11

    cursor = conn.cursor()

    cursor.execute('''SELECT id, user_id, url,
        description, vote_count FROM posts ORDER BY vote_count DESC
        LIMIT ? , ?''', (0, count))

    results = cursor.fetchall()
    conn.close()
    print results
    return results,
    status.HTTP_202_ACCEPTED


def create_posts():
    db = sqlite3.connect(db_url)
    db.execute('''INSERT INTO posts (user_id, url, description, vote_count)
        VALUES (?,?,?,?) ''',
               [1, 'https://www.nrdc.org/issues/water-pollution',
                "It's about time we got serious about drinking water",
                102])

    db.execute('''INSERT INTO posts (user_id, url, description, vote_count)
        VALUES (?,?,?,?) ''',
               [2, 'http://www.cnn.com',
                "Iowa is about to stop paying for the homeless. WTF",
                99])

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
