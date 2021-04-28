from database import db
from flask import session, render_template, request, redirect, Blueprint, flash, g
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__)


@bp.before_app_request
def verify_login():
    user_id = session.get("user_id")

    if not user_id:
        g.user = None
    else:
        g.user = db.db_connect().execute("SELECT username FROM Users WHERE id = ?", (user_id,)).fetchone()


@bp.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("login")
        passwd = request.form.get("passwd")
        passwd_verify = request.form.get("passwd_verify")
        database = db.db_connect()
        user = database.execute("SELECT * FROM Users where username = ?", (name,)).fetchone()
        if user:
            flash(f"Username {name} is already registered")
            print(f"Attempt on register new user {name} who is already registered")
            return render_template("register.html")
        if passwd != passwd_verify:
            flash("Passwords are different")
            print(f"Passwords {passwd} and {passwd_verify} are different")
            return render_template("register.html")
        database.execute("INSERT INTO Users (username, pwd_hash) VALUES (?, ?)", (name, generate_password_hash(passwd)))
        database.commit()
        print(f"Registration of user {name} successful")
        return redirect("/login/")
    return render_template("register.html")


@bp.route("/login/", methods=["GET", "POST"])
def login():
    """
    Login page
    :return: Redirects to menu page after successfull authentication.
    """
    if request.method == "POST":
        name = request.form.get("login")
        passwd = request.form.get("passwd")
        database = db.db_connect()
        user = database.execute("SELECT * FROM Users where username = ?", (name,)).fetchone()
        if user:
            if not check_password_hash(user['pwd_hash'], passwd):
                flash("Incorrect password")
                print("Wrong password {passwd} for user {name}")
                return render_template("login.html")
        else:
            database.execute("INSERT INTO Users (username, pwd_hash) VALUES (?,?)",
                             (name, generate_password_hash(passwd)))
            database.commit()
            user = database.execute("SELECT * FROM Users where username = ?", (name,)).fetchone()
        session.clear()
        session['user_id'] = user['id']
        return redirect("/menu/")

    return render_template("login.html")


@bp.route("/logout/")
def logout():
    session.clear()
    print(f"User {g.user} successfully logged out")
    return redirect("/login/")
