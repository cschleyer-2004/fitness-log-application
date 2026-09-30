from decimal import Decimal

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

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

@app.route("/")
def index():
    workouts = Workouts.query.filter_by(user_id = 1).order_by(Workouts.id.desc()).all()
    return render_template("index.html", workouts= workouts)

@app.route("/log", methods=["GET", "POST"])
def log_workout():
    if request.method == "GET":
        exercises = Exercises.query.all()

    if request.method == "POST":
        '''
        # 1. Pull the submitted values out of the form
        #    - date and notes are still single values
        #    - exercise/sets/reps/weight now come in as LISTS, one entry per
        #      "Add" click, since the JS submits them as exercise[], sets[], etc.
        #    - use request.form.getlist(...) instead of request.form[...] for those
        date_str = get "date" from request.form
        notes = get "notes" from request.form
        exercise_ids = getlist "exercise[]" from request.form
        sets_list = getlist "sets[]" from request.form
        reps_list = getlist "reps[]" from request.form
        weights_list = getlist "weight[]" from request.form
        '''

        date_str = request.form["date"]
        notes = request.form["notes"]
        exercise_ids = request.form.getlist("exercise[]")
        sets_list = request.form.getlist("sets[]")
        reps_list = request.form.getlist("reps[]")
        weights_list = request.form.getlist("weight[]")

        '''
        # 2. Convert types where needed
        #    - date_str comes in as a string, your model wants a DateTime
        #    - the four lists above still hold everything as strings -
        #      conversion now happens per-item, inside the loop in step 4,
        #      since each list can hold more than one entry
        '''
        date = datetime.strptime(date_str, "%Y-%m-%d")

        '''
        # 3. Create the parent row first
        new_workout = Workouts(user_id=1, date=<converted date>, notes=notes)
        add new_workout to db.session
        commit  # <-- must commit here so new_workout.id actually exists
        '''
        new_workout = Workouts(user_id=1, date=date, notes=notes)
        db.session.add(new_workout)
        db.session.commit()

        '''
        # 4. Now create ONE child row PER entry the user added, referencing
        #    the parent's real id.
        #    - zip() walks all four lists together, position by position,
        #      so item 0 of each list belongs to the same "Add" click,
        #      item 1 of each list belongs to the next one, and so on
        #    - convert each item's types inside the loop
        for exercise_id, sets_val, reps_val, weight_val in zip(exercise_ids, sets_list, reps_list, weights_list):
            new_set = Set_Entries(
                workout_id=new_workout.id,
                exercise_id=<converted to int>,
                set_count=<converted to int>,
                rep=<converted to int>,
                weight=<converted to decimal>
            )
            add new_set to db.session
        commit once, after the loop finishes
        '''
        for exercise_id, sets_val, reps_val, weight_val in zip(exercise_ids, sets_list, reps_list, weights_list):
            new_set = Set_Entries(
                workout_id=new_workout.id,
                exercise_id=int(exercise_id),
                set_count=int(sets_val),
                rep=int(reps_val),
                weight=Decimal(weight_val)
            )
            db.session.add(new_set)
        db.session.commit()

        '''
        # 5. Don't fall through to render_template - redirect instead
        redirect to index route
        '''
        return redirect(url_for("index"))

    return render_template("log_workout.html", exercises=exercises)

@app.route("/progress")
def progress():

    '''
    # 1. Get the exercise to show progress for
    #    - read "exercise_id" from the query string (request.args)
    #    - it'll arrive as a string or None if not provided
    exercise_id = get "exercise_id" from request.args, default None
    '''

    exercise_id = request.args.get("exercise_id")


    '''   
    # 2. Get the list of all exercises (for a dropdown so the user can pick one)
    '''
    exercises = Exercises.query.all()

    '''
    # 3. Decide what to do if no exercise_id was given yet
    #    - e.g. just render the page with the exercise list, no history yet
    '''
    if exercise_id is None:
        return render_template("progress.html", exercises=exercises, sets=None)

    '''
    # 4. Otherwise, convert exercise_id to int and query the history
    #    - join Set_Entries -> Workouts so you can filter by user and order by date
    #    - filter: Set_Entries.exercise_id == exercise_id AND Workouts.user_id == 1
    #    - order_by: Workouts.date ascending (so progress reads chronologically)
    '''
    sets = (Set_Entries.query.join(Workouts).
            filter(Set_Entries.exercise_id == exercise_id, Workouts.user_id == 1).
            order_by(Workouts.date).
            all())

    '''
    # 5. (Optional, later) run trend/plateau detection on `sets`
    #    - e.g. compare weight/reps over the last N sessions
    '''

    '''
    # 6. Pass exercises + sets (+ selected exercise_id) into the template
    '''

    return render_template("progress.html", exercises=exercises, sets=sets, selected_id=exercise_id)


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