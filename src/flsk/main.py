import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from database import db
from flsk import app
from flask import session, render_template, request, redirect

CURRENTLY_LOGGED_IN = {}


def get_info(user):
    pass


@app.route("/add/", methods=["GET", "POST"])
def add():
    """
    Add new item to To Do list
    :return: In the case of GET request, return new form. In the case of POST request, save new item and redirects back
    to main menu.
    """
    user_id = session["user_id"]
    if not user_id:
        session.clear()
        redirect("/")
    database = db.db_connect(app)
    user = database.execute("SELECT * FROM Users where id = ?", (user_id,)).fetchone()
    db.db_close(app)
    if not user:
        session.clear()
        redirect("/")

    if request.method == "POST":
        title = request.form.get("title")
        deadline = request.form.get("deadline")
        importance = request.form.get("importance")
        try:
            print((int(user_id), title, deadline, importance))
            database = db.db_connect(app)
            database.execute("INSERT INTO Tasks (author, description, deadline, importance) VALUES"
                             "(?, ?, ?, ?)", (int(user_id), title, deadline, importance))
            database.commit()
            resp = redirect("/menu/")
        except Exception as e:
            resp = render_template("add_item.html", warn=True, warnmessage=e)
        finally:
            db.db_close(app)
            return resp

    return render_template("add_item.html", warn=False, warnmessage="")


@app.route("/show/")
def show():
    user_id = session["user_id"]
    if not user_id:
        session.clear()
        redirect("/")
    database = db.db_connect(app)
    user = database.execute("SELECT * FROM Users where id = ?", (user_id,)).fetchone()
    if not user:
        db.db_close(app)
        session.clear()
        redirect("/")

    tasks = database.execute("SELECT description, deadline, importance FROM Tasks WHERE author = ?",
                             (int(user_id),)).fetchall()
    print(tasks)
    return render_template("show_all.html", tasks=tasks)


@app.route("/menu/")
def menu():
    """
    Main menu page handler
    :return: Main menu page
    """
    user_id = session["user_id"]
    if not user_id:
        session.clear()
        redirect("/")
    database = db.db_connect(app)
    user = database.execute("SELECT * FROM Users where id = ?", (user_id,)).fetchone()
    db.db_close(app)
    return render_template("menu.html", username=user["username"])


@app.route("/end/")
def end():
    """
    Logout procedure
    :return: Redirects back to main page and logout user
    """
    session.clear()
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main page - login
    :return: Redirects to menu page after successfull authentication.
    """
    if request.method == "POST":
        name = request.form.get("login")
        passwd = request.form.get("passwd")
        database = db.db_connect(app)
        user = database.execute("SELECT * FROM Users where username = ?", (name,)).fetchone()
        db.db_close(app)
        if user:
            if not check_password_hash(user['pwd_hash'], passwd):
                return render_template("index.html", wrong=True)
        else:
            database = db.db_connect(app)
            database.execute("INSERT INTO Users (username, pwd_hash) VALUES (?,?)",
                             (name, generate_password_hash(passwd)))
            database.commit()
            user = database.execute("SELECT * FROM Users where username = ?", (name,)).fetchone()
            db.db_close(app)
        session.clear()
        session['user_id'] = user['id']
        return redirect("/menu/")

    return render_template("index.html", wrong=False)


def main():
    app.run()
