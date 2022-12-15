from flask import render_template
from flask import redirect, session
from functools import wraps
import re

def apology(message, code = 400):
    return render_template("apology.html", message = message, code = code)

def check_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return email

def check_password(pswd):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,16}$"
    res = re.search(reg, pswd)
    if res:
        return pswd

def get_bmi(w, h):
    _bmi = round(w/(pow(h/100, 2)), 2)
    return _bmi

def get_category(_index):
    if _index >= 40:
        return ("Morbidly obese.", 
        "Being morbidly obese not only is proven to cause physical issues such as diabetes, cancers, and cardiovascular disease, it can affect a person’s mental and emotional well-being as well.", 
        "The best weight loss technique for someone who is morbidly obese includes diet, exercise and therapy.")
    if _index >= 30:
        return ("Based upon your BMI score, you are possibly obese.",
        "You are at a much higher risk of developing chronic diseases and shortening your lifespan.",
        "The good news is that weight loss can reduce your level of risk. Even losing 5% of your body weight will reduce your risk dramatically.")
    if _index >=25:
        return ("Overweight.",
        "When your body mass index number is 25 or higher, it may indicate that you have too much weight in relation to your height.",
        "Being overweight raises the risk of developing a chronic disease.",
        "But even a small loss in weight will make a big difference towards gaining better health.")
    if _index >=18.5:
        return ("Normal weight. Congratulations!",
        "You appear to have an optimal amount of body fat.",
        "Our bodies use fat to maintain healthy emotional, mental and physical processing.",
        "You are therefore at a much lower risk for chronic diseases such as Type 2 Diabetes, high blood pressure and even heart disease.")
    else:
        return ("Underweight.",
        "When your body mass index is less than 18.5, it could indicate that you do not have enough body fat to sustain good health.",
        "This could lead to chronic fatigue, chronic illnesses, absence of menstruation, and might even indicate an eating disorder.")

def metric_weight(w):
    return round(w * 0.45359237, 2)

def metric_height(h):
    return round(h* 2.54, 2)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


