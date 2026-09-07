import os, random, sqlite3
from functools import wraps
from datetime import date
from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretpoweruserkey")

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = 'static/assets/'

DB_PATH = os.getenv("DATABASE_PATH", "blogposts.db")

def db_execute(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        if query.strip().upper().startswith("SELECT"):
            return [dict(row) for row in cur.fetchall()]
        return cur.lastrowid

db_execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, hash TEXT NOT NULL)")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users = db_execute("SELECT * FROM users WHERE username = ?", (username,))
        if len(users) != 1 or not check_password_hash(users[0]["hash"], password):
            return redirect("/")
        session["user_id"] = users[0]["id"]
        return redirect("/upload")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.html"), 404

@app.errorhandler(500)
def post_not_found(e):
    return render_template("notfound.html"), 500

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    posts = db_execute("SELECT * FROM posts ORDER BY id DESC LIMIT 4")
    topics = db_execute("SELECT DISTINCT tags FROM posts ORDER BY id DESC LIMIT 20")
    return render_template("index.html", posts=posts, topics=topics)

@app.route("/posts/<int:id>/delete", methods=["POST"])
@login_required
def delete_post(id):
    db_execute("DELETE FROM posts WHERE id = ?", (id,))
    return redirect("/posts")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/posts")
def posts():
    return render_template("postslist.html", posts=db_execute("SELECT * FROM posts ORDER BY id DESC"))

@app.route('/posts/<int:id>/')
def display_post(id):
    posts = db_execute("SELECT * FROM posts WHERE id = ?", (id,))
    if not posts:
        return render_template("notfound.html"), 404
    return render_template('post.html', id=id, post=posts[0])

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "GET":
        return render_template('upload.html')
    else:
        imgsrc = "static/assets/helloworld.png"
        try:
            file = request.files["thumbnail"]
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                imgsrc = "static/assets/" + filename
        except Exception as e:
            print("No files attached")
        title = request.form.get("title")
        subtext = request.form.get("subtext")
        body = request.form.get("body")
        tags = request.form.get("topic")
        datetime = date.today().strftime("%B %d, %Y")
        db_execute("INSERT INTO posts (title, subtext, body, tags, imgsrc, datetime) VALUES(?, ?, ?, ?, ?, ?)", (title, subtext, body, tags, imgsrc, datetime))
        return render_template("upload.html")

@app.route("/topics")
def showtopics():
    return render_template("topics.html", posts=db_execute("SELECT DISTINCT tags FROM posts"))

@app.route('/topics/<string:topic>/')
def display_topics(topic):
    posts = db_execute("SELECT * FROM posts WHERE tags = ? ORDER BY id DESC", (topic,))
    if not posts:
        return render_template("notfound.html"), 404
    return render_template("specificpostslist.html", posts=posts, thetopic=topic)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
