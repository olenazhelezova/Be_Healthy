from application import app
from flask import redirect, render_template, request, session, flash, get_flashed_messages, Response, jsonify
from flask_session import Session
from application.search import food_search, recipe_search
from application.database import get_connection
from .helpers import apology, check_email, check_password, login_required, get_bmi, metric_weight, metric_height, get_category
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import json

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.errorhandler(404)
def not_found(e):
    return render_template('apology.html', message="Page not found", code="404")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/home")
@app.route("/")
@app.route("/index")
def index():
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
            return apology("Password must be at least 8 characters, include lowercase, uppercase, digit and symbol", 400)
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
    user_id = session["user_id"]
    current_date = datetime.now()
    current_date = f'{current_date.day}.{current_date.month}.{current_date.year}'
    date = request.args.get('date', current_date)
    con = get_connection()
    cur = con.cursor()
    breakfast = cur.execute("SELECT id, food_name, weight, fat, carbs, prot, cals FROM food_diary WHERE user_id=? AND meal=? AND date=?", [user_id, "Breakfast", date]).fetchall()
    total_breakfast = cur.execute("SELECT SUM(fat) as fat, SUM(carbs) as carbs, SUM(prot) as prot, SUM(cals) as cals FROM food_diary WHERE user_id=? AND meal=? AND date=?", [user_id, "Breakfast", date]).fetchone()
    lunch = cur.execute("SELECT id, food_name, weight, fat, carbs, prot, cals FROM food_diary WHERE user_id=? AND meal=? AND date=?", [user_id, "Lunch", date]).fetchall()
    total_lunch = cur.execute("SELECT SUM(fat) as fat, SUM(carbs) as carbs, SUM(prot) as prot, SUM(cals) as cals FROM food_diary WHERE user_id=? AND meal=? AND date=?", [user_id, "Lunch", date]).fetchone()
    dinner = cur.execute("SELECT id, food_name, weight, fat, carbs, prot, cals FROM food_diary WHERE user_id=? AND meal=? AND date=?", [user_id, "Dinner", date]).fetchall()
    total_dinner = cur.execute("SELECT SUM(fat) as fat, SUM(carbs) as carbs, SUM(prot) as prot, SUM(cals) as cals FROM food_diary WHERE user_id=? AND meal=? AND date=?", [user_id, "Dinner", date]).fetchone()
    other = cur.execute("SELECT id, food_name, weight, fat, carbs, prot, cals FROM food_diary WHERE user_id=? AND meal=? AND date=?", [user_id, "Snacks/other", date]).fetchall()
    total_other = cur.execute("SELECT SUM(fat) as fat, SUM(carbs) as carbs, SUM(prot) as prot, SUM(cals) as cals FROM food_diary WHERE user_id=? AND meal=? AND date=?", [user_id, "Snacks/other", date]).fetchone()
    total = cur.execute("SELECT SUM(fat) as fat, SUM(carbs) as carbs, SUM(prot) as prot, SUM(cals) as cals FROM food_diary WHERE user_id=? AND date=?", [user_id, date]).fetchone()
    data = {"Breakfast": breakfast, "Lunch": lunch, "Dinner": dinner, "Snacks/other": other}
    total_data = {"Breakfast": total_breakfast, "Lunch": total_lunch, "Dinner": total_dinner, "Snacks/other": total_other}
    total_per_day = total 
    con.commit()
    return render_template("diary.html", data=data, total_data=total_data, date=date, total_per_day=total_per_day)


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

@app.route("/food-search-diary", methods=["GET"])
def food_search_diary():
    query = request.args.get('query')
    data = None
    if query != None:
        data = food_search(query)
    if data is not None and len(data) < 1:
        return jsonify([])
    return jsonify(data)

@app.route("/add-food", methods=["POST"])
def add_food():
    if request.method == "POST":
        con = get_connection()
        cur = con.cursor()
        user_id = session["user_id"]
        food_data = request.get_json()
        food_name = food_data["data"]["name"]
        date = food_data["date"]
        meal = food_data["meal"]
        weight = int(food_data["data"]["serving_size_g"])
        fat = round(float(food_data["data"]["fat_total_g"]), 1)
        carbs = round(float(food_data["data"]["carbohydrates_total_g"]), 1)
        prot = round(float(food_data["data"]["protein_g"]), 1)
        cals = int(food_data["data"]["calories"])
        print(user_id, food_name, date, meal, weight, fat, carbs, prot, cals)
        cur.execute("INSERT INTO food_diary (user_id, food_name, date, meal, weight, fat, carbs, prot, cals) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [user_id, food_name, date, meal, weight, fat, carbs, prot, cals])
        con.commit()
        return jsonify({"food_added": True})
    return jsonify({"food_added": False})


@app.route('/delete', methods=['GET'])
def delete():
    con = get_connection()
    cur = con.cursor()
    id = request.args.get("id")
    cur.execute("DELETE FROM food_diary WHERE id = ?", [id])
    con.commit()
    return redirect(request.referrer or "diary.html")
    