from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "/instance/triad.db"


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS exercise_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            session TEXT,
            exercise TEXT,
            set_no INTEGER,
            weight TEXT,
            reps TEXT,
            rpe TEXT,
            notes TEXT
        )
        """)


init_db()


EXERCISES = [
    {"session": "A", "name": "Plate Loaded Pulldown", "machine": "Pulldown", "target": "40 kg", "sets": 3, "reps": 8, "cue": "Drive elbows to hips"},
    {"session": "A", "name": "Pullover", "machine": "Pullover", "target": "20 kg", "sets": 3, "reps": 10, "cue": "Keep ribs down"},
    {"session": "A", "name": "Seated Cable Row", "machine": "Low Row #2", "target": "35 kg", "sets": 3, "reps": 8, "cue": "Squeeze shoulder blades"},
    {"session": "A", "name": "Chest Press", "machine": "Chest Press #2", "target": "30 kg", "sets": 3, "reps": 8, "cue": "Control return"},
    {"session": "A", "name": "Shoulder Press", "machine": "Shoulder Press #2", "target": "20 kg", "sets": 3, "reps": 8, "cue": "Do not lock elbows"},
    {"session": "A", "name": "Triceps Pushdown", "machine": "Functional Trainer", "target": "22.5 kg", "sets": 3, "reps": 10, "cue": "Elbows fixed"},
    {"session": "A", "name": "Face Pull", "machine": "Functional Trainer", "target": "Light", "sets": 2, "reps": 15, "cue": "Pull to forehead"},
    {"session": "A", "name": "External Rotation", "machine": "Functional Trainer", "target": "Light", "sets": 2, "reps": 15, "cue": "Rotate shoulder only"},
    {"session": "A", "name": "Pallof Press", "machine": "Functional Trainer", "target": "Light", "sets": 3, "reps": 12, "cue": "Resist rotation"},
    {"session": "B", "name": "Deadlift Machine", "machine": "Deadlift", "target": "40 kg", "sets": 3, "reps": 8, "cue": "Brace core"},
    {"session": "B", "name": "Hip Thrust", "machine": "Hip Thrust", "target": "40 kg", "sets": 3, "reps": 10, "cue": "Squeeze glutes"},
    {"session": "B", "name": "Leg Press", "machine": "Leg Press #2", "target": "70 kg", "sets": 3, "reps": 8, "cue": "Full range"},
    {"session": "B", "name": "Hack Squat", "machine": "Hack Squat", "target": "20 kg", "sets": 3, "reps": 8, "cue": "Heels down"},
    {"session": "B", "name": "Leg Curl", "machine": "Leg Curl", "target": "40 kg", "sets": 3, "reps": 8, "cue": "Slow lowering"},
    {"session": "B", "name": "Standing Calf Raise", "machine": "Standing Calf Raise", "target": "65 kg", "sets": 4, "reps": 12, "cue": "Pause top and bottom"},
    {"session": "B", "name": "Farmer's Carry", "machine": "Dumbbells", "target": "20 kg/hand", "sets": 3, "reps": "30 m", "cue": "Walk tall"},
    {"session": "Both", "name": "Front Plank", "machine": "Floor", "target": "60 sec", "sets": 3, "reps": "60 sec", "cue": "Ribs down"},
    {"session": "Both", "name": "Side Plank", "machine": "Floor", "target": "30 sec/side", "sets": 3, "reps": "30 sec", "cue": "Straight line"},
    {"session": "Both", "name": "Dead Hang", "machine": "Pull-up Bar", "target": "30 sec", "sets": 3, "reps": "30 sec", "cue": "Relax shoulders"},
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gym")
def gym():
    return render_template("gym.html", exercises=EXERCISES)


@app.route("/api/log", methods=["POST"])
def save_log():
    data = request.json
    with sqlite3.connect(DB) as con:
        con.execute("""
        INSERT INTO exercise_logs
        (created_at, session, exercise, set_no, weight, reps, rpe, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(timespec="seconds"),
            data.get("session"),
            data.get("exercise"),
            data.get("set_no"),
            data.get("weight"),
            data.get("reps"),
            data.get("rpe"),
            data.get("notes"),
        ))
    return jsonify({"status": "saved"})


@app.route("/log")
def view_log():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("""
        SELECT created_at, session, exercise, set_no, weight, reps, rpe, notes
        FROM exercise_logs
        ORDER BY id DESC
        """).fetchall()
    return render_template("log.html", rows=rows)