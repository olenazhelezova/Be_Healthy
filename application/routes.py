from application import app
from flask import redirect, render_template, request, session, flash, get_flashed_messages, Response, jsonify
from flask_session import Session
from application.search import food_search, recipe_search
from application.database import get_connection
from .helpers import apology, check_email, check_password, login_required, get_bmi, metric_weight, metric_height, get_category
from werkzeug.security import check_password_hash, generate_password_hash
import json

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/home")
@app.route("/")
def index():
    """con = get_connection()
    cur = con.cursor()
    user_id = session["user_id"]
    if user_id:
        if request.method == 'POST':
            if request.form["add_food"]:
                cur.execute("INSERT INTO food_diary (user_id, food_name, date, meal, weight, fat, carbs, prot, cals) VALUES (user_id, item["name"], ?, ?, ?, ?, ?, ?, ?),", () )
        cur.close()
"""
    query = request.args.get("query")
    data = None
    if query != None:
        data = food_search(query)
    if data is not None and len(data) < 1:
        return render_template("index.html")

    
    return render_template("index.html", data = data, query = query)


@app.route("/recipes")
def recipes():
    query = request.args.get("query")
    data = None
    if query != None:
        data = recipe_search(query)
    if data is not None and len(data) < 1:
        return render_template("recipes.html")
    if data is not None:
        for i in range(len(data)):
                data[i]['servings'] = data[i]['servings'].lower()
                data[i]['ingredients'] = data[i]['ingredients'].lower().split("|")
                data[i]['id'] = i
    return render_template("recipes.html", data = data, query = query)


@app.route("/login", methods=["GET", "POST"])
def login():
        session.clear()
        con = get_connection()
        cur = con.cursor()
        if request.method == "POST":
            if not request.form.get("email"):
                return apology("please provide your email", 403)
            if not request.form.get("password"):
                return apology("please provide your password", 403)
            res = cur.execute("SELECT * FROM users WHERE email = ?", [request.form.get("email")]).fetchone()
            if res is None or not check_password_hash(res['hash'], request.form.get("password")):
                return apology("invalid email and/or password", 403)
            session["user_id"] = res["id"]
            cur.close()
            return redirect("/")
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    con = get_connection()
    cur = con.cursor()
    user_input = request.args.get("q")
    foods = cur.execute("SELECT name FROM food_list WHERE name LIKE :in || '%' LIMIT 7", {'in': user_input}).fetchall()
    food_list = list(map(lambda x: x.lower(), list(map(lambda a : a[0], foods))))
    resp = Response(json.dumps(list(food_list)))
    resp.headers['Content-Type'] = 'application/json'
    con.commit()
    return resp


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    con = get_connection()
    cur = con.cursor()
    if request.method == "POST":
        if not request.form.get("email"):
            return apology("please provide your email", 400)
        if not request.form.get("username"):
            return apology("please provide your username", 400)
        if not request.form.get("password") or not request.form.get("confirmation") or request.form.get("password") != request.form.get("confirmation"):
            return apology("input is blank or the passwords do not match", 400)
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        is_email_exist = cur.execute("SELECT * FROM users WHERE email = ?", [email]).fetchall()
        if len(is_email_exist) != 0:
            return apology("this email is registered", 400)
        if check_email(email) is None:
            return apology("email is invalid", 400)
        if check_password(password) == None:
            return apology("password must be 8-16 characters and include at least one lowercase letter, one uppercase letter, digit and symbol", 400)
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        cur.execute("INSERT INTO users (email, username, hash) VALUES (?, ?, ?)", (email, username, hash))
        con.commit()
        user_id = cur.lastrowid
        session["user_id"] = user_id
        return redirect("/")
    return render_template("register.html")


@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    if request.method == "POST":
        if not request.form.get("weight"):
            return apology("please provide your weight", 403)
        if not request.form.get("height"):
            return apology("please provide your height", 403)
        if not request.form.get("weight_ms"):
            return apology("please choose weight measurement system", 403)
        if not request.form.get("height_ms"):
            return apology("please choose height measurement system", 403)
        weight = request.form.get("weight")
        weight_ms = request.form.get("weight_ms")
        height = request.form.get("height")
        height_ms = request.form.get("height_ms")
        try:
            _weight = float(weight)
            _height = float(height)
            if _weight < 0 or _height < 0 or weight_ms not in ("kg", "lb") or height_ms not in("cm", "in"):
                raise ValueError
            if weight_ms == "lb":
                 _weight = metric_weight(_weight)
            if height_ms == "in":
                _height = metric_height(_height)
        except ValueError:
            return apology("please provide correct data", 400)
        else:
            index = get_bmi(_weight, _height)
            category = get_category(index)
        return render_template("bmi.html", index = index, category=category, weight=weight, height=height, weight_ms=weight_ms, height_ms=height_ms)
    return render_template("bmi.html")

@app.route("/diary")
@login_required
def diary():
    return render_template("diary.html")


@app.route("/validate-email", methods=["POST"])
def validate_registration():
    con = get_connection()
    cur = con.cursor()
    if request.method == "POST":
        email_adress = request.get_json()["email"]
        user = cur.execute("SELECT * FROM users WHERE email = ?", [email_adress]).fetchone()
        con.commit()
        if user:
            return jsonify({"user_exists": "true"})
        else:
            return jsonify({"user_exists": "false"})


@app.route("/validate-password", methods=["POST"])
def validate_login_password():
    con = get_connection()
    cur = con.cursor()
    if request.method == "POST":
        email_adress = request.get_json()["email"]
        password = request.get_json()["password"]
        user = cur.execute("SELECT * FROM users WHERE email = ?", [email_adress]).fetchone()
        con.commit()
        if user is None or not check_password_hash(user['hash'], password):
            return jsonify({"user_password": "false"})
        else:
            return jsonify({"user_password": "true"})


