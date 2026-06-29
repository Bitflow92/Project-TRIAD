from flask import Flask, request, jsonify, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "/data/triad.db"

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

@app.route("/")
def index():
    return render_template_string("""
    <h1>Project TRIAD</h1>
    <p>Rynier's Ironman Gym Companion</p>
    <p>You can do it!</p>
    <a href="/log">View workout log</a>
    """)

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

@app.route("/api/logs")
def logs():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("SELECT * FROM exercise_logs ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/log")
def view_log():
    with sqlite3.connect(DB) as con:
        rows = con.execute("""
        SELECT created_at, session, exercise, set_no, weight, reps, rpe, notes
        FROM exercise_logs
        ORDER BY id DESC
        """).fetchall()

    html = "<h1>Workout Log</h1><table border='1' cellpadding='6'>"
    html += "<tr><th>Date</th><th>Session</th><th>Exercise</th><th>Set</th><th>Weight</th><th>Reps</th><th>RPE</th><th>Notes</th></tr>"
    for r in rows:
        html += "<tr>" + "".join(f"<td>{x or ''}</td>" for x in r) + "</tr>"
    html += "</table><p><a href='/'>Back</a></p>"
    return html
