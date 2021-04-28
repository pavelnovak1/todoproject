import datetime
import random

from flask import Flask, render_template, request, make_response, redirect

import to_do_storage as storage
from storage_handler import load, save

CURRENTLY_LOGGED_IN = {}
app = Flask(__name__)


def get_info(sid):
    """
    Extract information about user from session ID.
    :param sid: Session ID cookie
    :return: User name, session ID and To Do list for a given user. None, user is not logged in yet.
    """
    for name, info in CURRENTLY_LOGGED_IN.items():
        if info[0] == sid:
            return name, info[0], info[1]
    return None


@app.route("/add/", methods=["GET", "POST"])
def add():
    """
    Add new item to To Do list
    :return: In the case of GET request, return new form. In the case of POST request, save new item and redirects back
    to main menu.
    """
    user = request.cookies.get("SESSION-ID")
    username, sid, to_do_list = get_info(user)
    if not username:
        return render_template("index.html", wrong=False)

    if request.method == "GET":
        resp = make_response(render_template("add_item.html", warn=False, warnmessage=""))
    else:
        try:
            title = request.form.get("title")
            deadline = datetime.datetime.strptime(request.form.get("deadline"), "%Y-%m-%d")
            importance = request.form.get("importance")

            to_do_list.add_item(title, deadline, importance)
            resp = redirect("/menu/")
        except Exception as e:
            resp = make_response(render_template("add_item.html", warn=True, warnmessage=e))
    resp.set_cookie("SESSION-ID", user)
    return resp


@app.route("/menu/")
def menu():
    """
    Main menu page handler
    :return: Main menu page
    """
    user = request.cookies.get("SESSION-ID")
    username, sid, to_do_list = get_info(user)
    if not username:
        return redirect("/")

    resp = make_response(render_template("menu.html", username=username))
    resp.set_cookie("SESSION-ID", user)
    return resp


@app.route("/exit/")
def exit():
    """
    Logout procedure
    :return: Redirects back to main page and logout user
    """
    user = request.cookies.get("SESSION-ID")
    username, sid, to_do_list = get_info(user)
    if username:
        save(to_do_list, username)
        CURRENTLY_LOGGED_IN.pop(username)

    resp = redirect("/")
    resp.delete_cookie("SESSION-ID")
    return resp


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main page
    :return: Redirects to menu page after successfull authentication.
    """
    name = request.form.get("login")
    passwd = request.form.get("passwd")
    if name is None or passwd is None:
        return render_template("index.html", wrong=False)
    to_do_list = load(name)
    if not to_do_list:
        to_do_list = storage.ToDoList(passwd)
    if not to_do_list.verify_passwd(passwd):
        return render_template("index.html", wrong=True)
    new_id = str(random.randrange(0, 100))
    if name in CURRENTLY_LOGGED_IN.keys():
        resp = make_response(render_template("menu.html", username=name))
        resp.set_cookie("SESSION-ID", CURRENTLY_LOGGED_IN[name][0])
        return resp
    CURRENTLY_LOGGED_IN[name] = (new_id, to_do_list)
    resp = redirect("/menu/")
    resp.set_cookie("SESSION-ID", new_id)
    return resp


def main():
    app.run()