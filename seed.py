"""
seed.py — populates the Exercises table with a starter list.

Note: Database seeding is the process of automatically populating a database with an initial set of data

Fill in the pseudocode blocks below yourself — the structure/order matters
more than the exact syntax, and you've already written this same pattern
in main.py (query -> check -> create -> commit).
"""

from main import app, db, Exercises

default_exercises = [
    ("Bench Press", "Chest"),
    ("Squat", "Legs"),
    ("Deadlift", "Back"),
    ("Overhead Press", "Shoulders"),
    ("Barbell Row", "Back"),
    ("Bicep Curls", "Arms")
]

# 3. Write a function that does the actual seeding.
#    For each (name, muscle_group) pair:
#       - check whether an Exercise with that name already exists
#         (case-insensitive check, same idea as the .ilike() approach
#          you used for user-added exercises)
#       - if it does NOT exist: create a new Exercises row and add it
#         to the session
#       - if it already exists: skip it (don't re-insert, don't error)
#    After the loop, commit once.
#
#    def seed_exercises():
#        for name, muscle_group in default_exercises:
#            existing = <query Exercises where name matches, case-insensitive>
#            if existing is None:
#                <create Exercises(name=name, muscle_group=muscle_group)>
#                <add to db.session>
#        <db.session.commit()>

def seed_exercises():
    for name, muscle_group in default_exercises:
        existing = db.session.query(Exercises).filter_by(name=name).first()
        print(type(existing))
        if existing is None:
            db.session.add(Exercises(name=name, muscle_group=muscle_group))
    db.session.commit()

# 4. Only run the seeding when this file is executed directly
#    (not when it's imported elsewhere), and make sure it runs inside
#    an app context so db.session actually knows which app/db to use.
#
#    if __name__ == "__main__":
#        with app.app_context():
#            seed_exercises()
#            print("Done seeding exercises.")

if __name__ == "__main__":
    with app.app_context():
        seed_exercises()
        print("Done")

# ---------------------------------------------------------------------
# Optional, once the above works: fold this into main.py instead of
# running it as a separate script.
#
# Right where main.py currently does:
#     with app.app_context():
#         db.create_all()
#
# add a check like:
#     if Exercises.query.count() == 0:
#         seed_exercises()
#
# That way a brand-new db.sqlite3 always starts populated, and you
# don't have to remember to run seed.py manually. You'd need to move
# (or import) default_exercises/seed_exercises so main.py can see them.
# ---------------------------------------------------------------------