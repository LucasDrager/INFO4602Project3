import logging
from pathlib import Path
import random
import sqlite3
from typing import Any, Dict
from flask import Flask, Response, redirect, request, render_template

app = Flask(__name__)
app.secret_key = "a28c041dd48ac23a" 

DATABASE_FILE = "database.sqlite3"

# If the database does not exist yet, create it.
db_file = Path(DATABASE_FILE)
if not db_file.is_file() or db_file.stat().st_size == 0:
    schema = Path("schema.sql").read_text()
    db = sqlite3.connect(DATABASE_FILE)
    cur = db.executescript(schema)
    db.commit()
    cur.close()

def new_connection():
    def make_dicts(cursor: sqlite3.Cursor, row: sqlite3.Row) -> Dict[str, Any]:
            return {cursor.description[idx][0]: value for idx, value in enumerate(row)}
    con = sqlite3.connect(DATABASE_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = make_dicts
    return con

def get_current_user():
    session_token = request.cookies.get("session_token")
    if not session_token:
        return None

    with new_connection() as con:
        # This SQL statement is a bit more complex: it returns the username of the user who
        # corrosponds to the session token's user ID
        user = con.execute("SELECT username FROM users "
            "INNER JOIN session_tokens ON users.user_id=session_tokens.user_id "
            "WHERE session_token=?", [session_token]).fetchone()
        if not user:
            return None
    
    return user["username"]

@app.route("/")
def index():
    """
    Show the main page which displays a list of posts to the user.
    """
    username = get_current_user()
    if username is None:
        return redirect("/login")

    search_term = request.args.get("search", "").replace("<","&lt;").replace(">","&gt;")
    page = request.args.get("page", 1, type=int)

    with new_connection() as con:
        sql = "SELECT * FROM threads WHERE title LIKE ?"
        con.execute(sql, (f"%{search_term}%",))
        page = request.args.get("page", 1, type=int)
        # Calculate how many pages worth of threads there are
        THREADS_PER_PAGE = 5
        total_threads = con.execute("SELECT COUNT(*) FROM threads WHERE title LIKE ?", [f"%{search_term}%"]).fetchone()["COUNT(*)"]
        max_page = int(total_threads) // THREADS_PER_PAGE + 1

        # Retreive only the specific threads for the page the user is currently on
        thread_sql = "SELECT thread_id, title, author FROM threads WHERE title LIKE ? LIMIT ? OFFSET ?"
        thread_params = [f"%{search_term}%", THREADS_PER_PAGE, (page-1) * THREADS_PER_PAGE]
        threads = con.execute(thread_sql, thread_params).fetchall()

    return render_template(
        "index.html",
        username=username,
        threads=threads,
        page=page,
        max_page=max_page,
        total_threads=total_threads,
        search=search_term)

@app.route("/thread/<thread_id>")
def thread(thread_id: str):
    """
    Show a specific thread.
    """
    username = get_current_user()
    if username is None:
        return redirect("/login")

    with new_connection() as con:
        # Find the thread with this ID and return the first result
        sql = "SELECT thread_id, title, author, body FROM threads WHERE thread_id = ?"
        thread_data = con.execute(sql, (thread_id,)).fetchone()

        if not thread_data:
            return "That thread does not exist"

        replies = con.execute("SELECT author, body FROM replies WHERE thread_id=?", [thread_id]).fetchall()

    return render_template("thread.html", username=username, thread=thread_data, replies=replies)

@app.route("/reply", methods=["POST"])
def reply():
    username = get_current_user()
    thread_id = request.form.get("thread_id", type=int)
    message = request.form["message"]

    if username is None:
        return redirect("/login")
    if thread_id is None:
        return "Invalid thread ID"

    with new_connection() as con:
        con.execute(
            "INSERT INTO replies (author, thread_id, body) VALUES (?, ?, ?)", [username, thread_id, message]
        )
        con.commit()

    return redirect(f"/thread/{thread_id}")

@app.route("/create_thread", methods=["GET"])
def create_thread_get():
    username = get_current_user()
    if username is None:
        return redirect("/login")

    return render_template("create_thread.html", username=username)

@app.route("/create_thread", methods=["POST"])
def create_thread_post():
    username = get_current_user()
    if username is None:
        return redirect("/login")

    title = request.form["title"].replace("<","&lt;").replace(">","&gt;")
    body = request.form["body"].replace("<","&lt;").replace(">","&gt;")

    with new_connection() as con:
        new_thread = con.execute(
            "INSERT INTO threads (author, title, body) VALUES (?, ?, ?) RETURNING thread_id", [username, title, body]
        ).fetchone()

    return redirect(f"/thread/{new_thread['thread_id']}")

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    with new_connection() as con:
        user = con.execute(
            "SELECT user_id FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

    if not user:
        return "Username or password is incorrect"
    
    # Generate a random number to use as the session token.
    SESSION_TOKEN_LENGTH = 16 # bytes
    session_token = random.randbytes(SESSION_TOKEN_LENGTH).hex()

    with new_connection() as con:
        con.execute(
            "INSERT INTO session_tokens (session_token, user_id) VALUES (?, ?)", [session_token, user["user_id"]]
        )
        con.commit()

    resp = redirect("/")
    resp.set_cookie("session_token", session_token, httponly=False)
    return resp

@app.route("/create_account", methods=["GET"])
def create_account_get():
    return render_template("create_account.html")

@app.route("/create_account", methods=["POST"])
def create_account_post():
    username = request.form["username"]
    password = request.form["password"]

    with new_connection() as con:
        user = con.execute(
            "SELECT * FROM users WHERE username=?", [username]
        ).fetchone()
        if user:
            return "A user with that username already exists!"

        con.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", [username, password]
        )
        con.commit()

    return redirect("/login")

@app.route("/logout", methods=["GET"])
def logout():
    resp = redirect("/")
    resp.delete_cookie("session_token")
    return resp

app.run(port=8000, debug=True)