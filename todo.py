from flask import Flask, render_template, request

app = Flask(__name__)

# ---- TEMPORARY placeholder data, just so the templates have something to render. ----
# Replace all of this once your models + database are wired up.
DUMMY_EXERCISES = [
    {"id": 1, "name": "Bench Press"},
    {"id": 2, "name": "Squat"},
    {"id": 3, "name": "Deadlift"},
]

DUMMY_WORKOUTS = [
    {
        "date": "2026-09-08",
        "notes": "Felt strong today",
        "sets": [
            {"exercise": "Bench Press", "reps": 8, "weight": 135},
            {"exercise": "Bench Press", "reps": 6, "weight": 145},
        ],
    }
]
# ---------------------------------------------------------------------------------


@app.route("/")
def index():
    # TODO: replace DUMMY_WORKOUTS with a real DB query, e.g.
    # workouts = Workout.query.filter_by(user_id=current_user_id).order_by(Workout.date.desc()).all()
    return render_template("index.html", workouts=DUMMY_WORKOUTS)


@app.route("/log", methods=["GET", "POST"])
def log_workout():
    if request.method == "POST":
        # TODO: read request.form, create a Workout + SetEntry row(s), commit to DB,
        # then redirect to index instead of just re-rendering the form.
        pass
    return render_template("log_workout.html", exercises=DUMMY_EXERCISES)


@app.route("/progress")
def progress():
    # TODO: read request.args.get("exercise_id"), query SetEntry history for it,
    # run your trend/plateau detection, and pass real data + the LLM suggestion
    # into the template instead of the static placeholders.
    return render_template("progress.html", exercises=DUMMY_EXERCISES)


if __name__ == "__main__":
    app.run(debug=True)
