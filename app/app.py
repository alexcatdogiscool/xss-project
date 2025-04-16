from flask import Flask, request, render_template, redirect, session, url_for
import sqlite3


app = Flask(__name__)

app.secret_key = "s3cret"


def get_db():
    conn = sqlite3.connect("user_db")
    conn.row_factory = sqlite3.Row
    return conn



@app.before_request
def setup():
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, display TEXT)")
    db.commit()

@app.route('/')
def index():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    if 'user_id' in session:
        user_id = session['user_id']
        return render_template("index.html", user_id=user_id)
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?", (request.form['username'], request.form['password'])).fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            db.execute("INSERT INTO users (username, password, display) VALUES (?, ?, '')", (request.form['username'], request.form['password']))
            db.commit()
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
def profile(user_id):
    db = get_db()
    if request.method == "POST" and 'user_id' in session and (session['user_id'] == user_id or session['user_id'] == 1):
        db.execute("UPDATE users SET display=? WHERE id=?", (request.form['display'], user_id))
        db.commit()
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    #return render_template("index.html")
    return render_template("profile.html", user=user)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)