import os
from decimal import Decimal

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#define the key
app.config["SECRET_KEY"] = "pingas"
#add database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#initialize the database
db = SQLAlchemy(app)

#create models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

class Exercises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    muscle_group = db.Column(db.String(50))

class Workouts(db.Model):
    sets = db.relationship('Set_Entries', backref='workout')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Set_Entries(db.Model):
    exercise = db.relationship('Exercises')

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    set_count = db.Column(db.Integer)
    rep = db.Column(db.Integer)
    weight = db.Column(db.Numeric(6,2))

#routes

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    workouts = Workouts.query.filter_by(
        user_id = session["user_id"]
    ).order_by(Workouts.id.desc()).all()

    return render_template("index.html", workouts= workouts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        attempted_password = request.form["password"]
        user = Users.query.filter_by(username=request.form["username"]).first()

        if user is None:
            return render_template("login.html", error="No account with that email exists")
        if check_password_hash(user.password, attempted_password):
            session["user_id"] = user.id
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Incorrect Password")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return render_template("signup.html", error="Passwords don't match")

        if Users.query.filter_by(username=username).first():
            return render_template("signup.html", error="Username already exists")

        if Users.query.filter_by(email=email).first():
            return render_template("signup.html", error="Email already exists")

        hashed = generate_password_hash(password)

        new_user = Users(username=username, email=email, password=hashed)
        db.session.add(new_user)
        db.session.commit()
    return render_template("login.html")

@app.route("/log", methods=["GET", "POST"])
def log_workout():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        exercises = Exercises.query.all()

    if request.method == "POST":

        date_str = request.form["date"]
        notes = request.form["notes"]
        exercise_ids = request.form.getlist("exercise[]")
        sets_list = request.form.getlist("sets[]")
        reps_list = request.form.getlist("reps[]")
        weights_list = request.form.getlist("weight[]")

        date = datetime.strptime(date_str, "%Y-%m-%d")

        new_workout = Workouts(user_id=session["user_id"], date=date, notes=notes)
        db.session.add(new_workout)
        db.session.commit()


        for exercise_id, sets_val, reps_val, weight_val in zip(exercise_ids, sets_list, reps_list, weights_list):
            if exercise_id.startswith("new:"):
                new_name = exercise_id[len("new:"):]
                existing = Exercises.query.filter_by(name=new_name).first()
                if existing is None:
                    existing = Exercises(name=new_name)
                    db.session.add(existing)
                    db.session.commit()  # commit now so existing.id is real
                resolved_exercise_id = existing.id
            else:
                resolved_exercise_id = int(exercise_id)

            new_set = Set_Entries(
                workout_id=new_workout.id,
                exercise_id=resolved_exercise_id,
                set_count=int(sets_val),
                rep=int(reps_val),
                weight=Decimal(weight_val)
            )
            db.session.add(new_set)
        db.session.commit()


        return redirect(url_for("index"))

    return render_template("log_workout.html", exercises= exercises)

@app.route("/progress")
def progress():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    exercise_id = request.args.get("exercise_id")

    exercises = Exercises.query.all()

    if exercise_id is None:
        return render_template("progress.html", exercises=exercises, sets=None, chart_dates = [], chart_weights = [], trend=None)

    sets = (Set_Entries.query.join(Workouts).
            filter(Set_Entries.exercise_id == exercise_id, Workouts.user_id == session["user_id"]).
            order_by(Workouts.date).
            all())

    chart_dates = []
    chart_weights = []
    for entry in sets:
        chart_dates.append(entry.workout.date.strftime("%Y-%m-%d"))
        chart_weights.append(float(entry.weight))

    trend = None
    if len(sets) >= 2:
        if sets[-1].weight > sets[-2].weight:
            trend = "improving"
        elif sets[-1].weight < sets[-2].weight:
            trend = "declining"
        else:
            trend = "steady"

    return render_template(
        "progress.html",
        exercises=exercises,
        sets=sets,
        selected_id=exercise_id,
        chart_dates=chart_dates,
        chart_weights=chart_weights,
        trend=trend
    )


default_exercises = [
    ("Bench Press", "Chest"),
    ("Squat", "Legs"),
    ("Deadlift", "Back"),
    ("Overhead Press", "Shoulders"),
    ("Barbell Row", "Back"),
    ("Bicep Curls", "Arms")
]

def seed_exercises():
    for name, muscle_group in default_exercises:
        existing = db.session.query(Exercises).filter_by(name=name).first()
        #print(type(existing))
        if existing is None:
            db.session.add(Exercises(name=name, muscle_group=muscle_group))
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Exercises.query.count() == 0:
            seed_exercises()

    # When done debugging, you can set debug=False for production
    # app.run(debug=False)

    # If testing on multiple machines:
    app.run('0.0.0.0', port=5000, debug=True)