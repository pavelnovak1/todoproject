from database import db
from flask import session, render_template, request, redirect, Blueprint, g


bp = Blueprint("application", __name__)
@bp.route("/add/", methods=["GET", "POST"])
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
    database = db.db_connect()
    user = database.execute("SELECT * FROM Users where id = ?", (user_id,)).fetchone()
    if not user:
        session.clear()
        redirect("/")

    if request.method == "POST":
        title = request.form.get("title")
        deadline = request.form.get("deadline")
        importance = request.form.get("importance")
        try:
            print((int(user_id), title, deadline, importance))
            database = db.db_connect()
            database.execute("INSERT INTO Tasks (author, description, deadline, importance) VALUES"
                             "(?, ?, ?, ?)", (int(user_id), title, deadline, importance))
            database.commit()
            resp = redirect("/menu/")
        except Exception as e:
            resp = render_template("add_item.html", warn=True, warnmessage=e)
        return resp
    return render_template("add_item.html", warn=False, warnmessage="")


@bp.route("/show/")
def show():
    user_id = session["user_id"]
    if not user_id:
        session.clear()
        redirect("/")
    database = db.db_connect()
    user = database.execute("SELECT * FROM Users where id = ?", (user_id,)).fetchone()
    if not user:
        session.clear()
        redirect("/")

    tasks = database.execute("SELECT description, deadline, importance FROM Tasks WHERE author = ?",
                             (int(user_id),)).fetchall()
    return render_template("show_all.html", tasks=tasks)


@bp.route("/menu/")
def menu():
    """
    Main menu page handler
    :return: Main menu page
    """
    user_id = session["user_id"]
    if not user_id:
        session.clear()
        redirect("/")
    database = db.db_connect()
    user = g.user
    return render_template("menu.html", username=user["username"])


@bp.route("/")
def index():
    """
    Main page
    :return: Redirects to login page
    """
    return redirect("/login/")

