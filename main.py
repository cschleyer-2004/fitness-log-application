from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

'''
flask_db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
'''


@app.route("/")
def index():
    #return render_template("index.html", workouts=DUMMY_WORKOUTS)
    return render_template("index.html")


@app.route("/log", methods=["GET", "POST"])
def log_workout():
    #if request.method == "POST":
    #    return render_template("log_workout.html", exercises=DUMMY_EXERCISES)
    return render_template("log_workout.html")


@app.route("/progress")
def progress():
    #return render_template("progress.html", exercises=DUMMY_EXERCISES)
    return render_template("progress.html")


if __name__ == '__main__':
    # When done debugging, you can set debug=False for production
    #app.run(debug=False)

    # If testing on multiple machines:
    app.run('0.0.0.0', port=5000, debug=True)