from flask import Flask, request, jsonify, render_template, Response, send_file, redirect, url_for, session
import sqlite3
from datetime import datetime
import csv
from functools import wraps
import hmac
import io
import os
import re

app = Flask(__name__)


def env_or_default(name, default):
    return os.environ.get(name) or default


DB = env_or_default("TRIAD_DB", "/instance/triad.db")

# Production deployments must set TRIAD_SECRET_KEY and both password environment
# variables. The fallback values below are temporary development defaults only.
app.secret_key = env_or_default("TRIAD_SECRET_KEY", "triad-development-secret-change-me")

USERS = {
    "Rynier": env_or_default("TRIAD_RYNIER_PASSWORD", "change-me-rynier"),
    "Wietz": env_or_default("TRIAD_WIETZ_PASSWORD", "change-me-wietz"),
}


def current_user():
    user = session.get("user")
    return user if user in USERS else None


@app.context_processor
def inject_current_user():
    return {"current_user": current_user()}


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def rynier_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = current_user()
        if not user:
            return redirect(url_for("login"))
        if user != "Rynier":
            return redirect(url_for("index"))
        return view(*args, **kwargs)

    return wrapped


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
        columns = [row[1] for row in con.execute("PRAGMA table_info(exercise_logs)").fetchall()]
        if "user" not in columns:
            con.execute("ALTER TABLE exercise_logs ADD COLUMN user TEXT")
        con.execute("""
        UPDATE exercise_logs
        SET user = 'Rynier'
        WHERE user IS NULL OR TRIM(user) = ''
        """)


init_db()


EXERCISES = [
    {
        "session": "A",
        "name": "Plate Loaded Pulldown",
        "machine": "Pulldown",
        "target": "40 kg",
        "sets": 3,
        "reps": 8,
        "image": "images/machines/plate_loaded_pulldown.jpg",
        "video": "https://www.youtube.com/results?search_query=plate+loaded+lat+pulldown+technique",
        "purpose": "Primary lat and upper-back strength",
        "cue": "Drive elbows down and towards your hips.",
        "mistakes": ["Leaning too far back", "Pulling only with the arms", "Shrugging the shoulders", "Using momentum"]
    },
    {
        "session": "A",
        "name": "Pullover",
        "machine": "Pullover",
        "target": "20 kg",
        "sets": 3,
        "reps": 10,
        "image": "images/machines/pullover.jpg",
        "video": "https://www.youtube.com/results?search_query=machine+pullover+proper+form",
        "purpose": "Swim-specific lat strength and underwater pull power",
        "cue": "Keep ribs down and pull towards your hips.",
        "mistakes": ["Arching the lower back", "Bending the elbows too much", "Using momentum", "Letting the shoulders shrug"]
    },
    {
        "session": "A",
        "name": "Seated Cable Row",
        "machine": "Low Row #2",
        "target": "35 kg",
        "sets": 3,
        "reps": 8,
        "image": "images/machines/low_row_2.jpg",
        "video": "https://www.youtube.com/results?search_query=seated+cable+row+proper+form",
        "purpose": "Mid-back and scapular strength",
        "cue": "Sit tall and squeeze the shoulder blades together.",
        "mistakes": ["Rounding the back", "Shrugging", "Jerking the weight", "Leaning too far back"]
    },
    {
        "session": "A",
        "name": "Chest Press",
        "machine": "Chest Press #2",
        "target": "30 kg",
        "sets": 3,
        "reps": 8,
        "image": "images/machines/chest_press_2.jpg",
        "video": "https://www.youtube.com/results?search_query=plate+loaded+chest+press+proper+form",
        "purpose": "Upper-body pressing balance and shoulder stability",
        "cue": "Control the return and keep shoulders down.",
        "mistakes": ["Letting the elbows flare too high", "Overextending the shoulders", "Bouncing the handles", "Rushing the return"]
    },
    {
        "session": "A",
        "name": "Shoulder Press",
        "machine": "Shoulder Press #2",
        "target": "20 kg",
        "sets": 3,
        "reps": 8,
        "image": "images/machines/shoulder_press_2.jpg",
        "video": "https://www.youtube.com/results?search_query=machine+shoulder+press+proper+form",
        "purpose": "Shoulder strength and upper-body durability",
        "cue": "Press smoothly without locking the elbows hard.",
        "mistakes": ["Locking out aggressively", "Shrugging", "Arching the lower back", "Training through shoulder pain"]
    },
    {
        "session": "A",
        "name": "Triceps Pushdown",
        "machine": "Functional Trainer",
        "target": "22.5 kg",
        "sets": 3,
        "reps": 10,
        "image": "images/machines/functional_trainer.jpg",
        "video": "https://www.youtube.com/results?search_query=rope+triceps+pushdown+proper+form",
        "purpose": "Triceps endurance for the finish of the freestyle pull",
        "cue": "Keep elbows fixed and finish with control.",
        "mistakes": ["Swinging the body", "Letting elbows drift forward", "Going too heavy", "Rushing the eccentric"]
    },
    {
        "session": "A",
        "name": "Face Pull",
        "machine": "Functional Trainer",
        "target": "Light",
        "sets": 2,
        "reps": 15,
        "image": "images/machines/functional_trainer.jpg",
        "video": "https://www.youtube.com/results?search_query=face+pull+proper+form",
        "purpose": "Rear delts, rotator cuff and shoulder health",
        "cue": "Pull towards your forehead with elbows high.",
        "mistakes": ["Going too heavy", "Shrugging", "Pulling too low", "Arching the back"]
    },
    {
        "session": "A",
        "name": "External Rotation",
        "machine": "Functional Trainer",
        "target": "Light",
        "sets": 2,
        "reps": 15,
        "image": "images/machines/functional_trainer.jpg",
        "video": "https://www.youtube.com/results?search_query=cable+external+rotation+proper+form",
        "purpose": "Rotator cuff strength and shoulder injury prevention",
        "cue": "Keep the elbow still and rotate only from the shoulder.",
        "mistakes": ["Using torso rotation", "Going too heavy", "Letting the elbow drift", "Rushing the movement"]
    },
    {
        "session": "A",
        "name": "Pallof Press",
        "machine": "Functional Trainer",
        "target": "Light",
        "sets": 3,
        "reps": 12,
        "image": "images/machines/functional_trainer.jpg",
        "video": "https://www.youtube.com/results?search_query=pallof+press+proper+form",
        "purpose": "Anti-rotation core strength",
        "cue": "Press straight out and resist rotation.",
        "mistakes": ["Rotating with the cable", "Holding the breath", "Standing too narrow", "Using too much weight"]
    },

    {
        "session": "B",
        "name": "Lat Pulldown",
        "machine": "Lat Machine",
        "target": "40 kg",
        "sets": 3,
        "reps": 8,
        "image": "images/machines/lat_machine.jpg",
        "video": "https://www.youtube.com/results?search_query=lat+pulldown+proper+form",
        "purpose": "Lat and upper-back strength to support swimming and posture",
        "cue": "Pull elbows down towards your ribs.",
        "mistakes": ["Leaning too far back", "Pulling with the arms only", "Shrugging the shoulders", "Using momentum"]
    },
    {
        "session": "B",
        "name": "Deadlift Machine",
        "machine": "Deadlift",
        "target": "40 kg",
        "sets": 3,
        "reps": 8,
        "image": "images/machines/deadlift_machine.jpg",
        "video": "https://www.youtube.com/results?search_query=deadlift+machine+proper+form",
        "purpose": "Posterior-chain strength for bike and run durability",
        "cue": "Brace your core and push through the floor.",
        "mistakes": ["Rounding the back", "Jerking from the bottom", "Using too much weight", "Not bracing properly"]
    },
    {
        "session": "B",
        "name": "Hip Thrust",
        "machine": "Hip Thrust",
        "target": "40 kg",
        "sets": 3,
        "reps": 10,
        "image": "images/machines/hip_thrust.jpg",
        "video": "https://www.youtube.com/results?search_query=hip+thrust+machine+proper+form",
        "purpose": "Glute strength for cycling power and running stride",
        "cue": "Squeeze the glutes at the top without arching.",
        "mistakes": ["Hyperextending the lower back", "Not reaching full hip extension", "Looking up", "Rushing the reps"]
    },
    {
        "session": "B",
        "name": "Leg Press",
        "machine": "Leg Press #2",
        "target": "70 kg",
        "sets": 3,
        "reps": 8,
        "image": "images/machines/leg_press_2.jpg",
        "video": "https://www.youtube.com/results?search_query=45+degree+leg+press+proper+form",
        "purpose": "Quad and glute strength for cycling power",
        "cue": "Use full range while keeping knees tracking over toes.",
        "mistakes": ["Using a shallow range", "Letting knees collapse inward", "Locking knees hard", "Lifting lower back from the pad"]
    },
    {
        "session": "B",
        "name": "Hack Squat",
        "machine": "Hack Squat",
        "target": "20 kg",
        "sets": 3,
        "reps": 8,
        "image": "images/machines/hack_squat.jpg",
        "video": "https://www.youtube.com/results?search_query=hack+squat+machine+proper+form",
        "purpose": "Quad and glute strength for run durability",
        "cue": "Keep heels down and lower under control.",
        "mistakes": ["Heels lifting", "Knees collapsing inward", "Too much weight too soon", "Bouncing at the bottom"]
    },
    {
        "session": "B",
        "name": "Leg Curl",
        "machine": "Leg Curl",
        "target": "40 kg",
        "sets": 3,
        "reps": 8,
        "image": "images/machines/leg_curl.jpg",
        "video": "https://www.youtube.com/results?search_query=seated+leg+curl+proper+form",
        "purpose": "Hamstring strength and knee protection",
        "cue": "Curl smoothly and lower slowly.",
        "mistakes": ["Swinging the weight", "Lifting the hips", "Dropping the weight", "Using short range"]
    },
    {
        "session": "B",
        "name": "Standing Calf Raise",
        "machine": "Standing Calf Raise",
        "target": "65 kg",
        "sets": 4,
        "reps": 12,
        "image": "images/machines/standing_calf_raise.jpg",
        "video": "https://www.youtube.com/results?search_query=standing+calf+raise+machine+proper+form",
        "purpose": "Calf and Achilles resilience for running durability",
        "cue": "Pause at the bottom stretch and at the top.",
        "mistakes": ["Bouncing", "Using partial range", "Bending the knees", "Moving too fast"]
    },
    {
        "session": "B",
        "name": "Farmer's Carry",
        "machine": "Dumbbells",
        "target": "20 kg/hand",
        "sets": 3,
        "reps": "30 m",
        "image": "",
        "video": "https://www.youtube.com/results?search_query=farmers+carry+proper+form",
        "purpose": "Grip, posture and core stability under load",
        "cue": "Walk tall with shoulders down.",
        "mistakes": ["Leaning sideways", "Shrugging", "Walking too fast", "Losing core brace"]
    },

    {
        "session": "Both",
        "name": "Front Plank",
        "machine": "Floor",
        "target": "60 sec",
        "sets": 3,
        "reps": "60 sec",
        "image": "",
        "video": "https://www.youtube.com/results?search_query=front+plank+proper+form",
        "purpose": "Core stiffness and whole-body posture",
        "cue": "Ribs down, glutes on, straight body line.",
        "mistakes": ["Hips sagging", "Holding the breath", "Looking up", "Chasing time with poor form"]
    },
    {
        "session": "Both",
        "name": "Side Plank",
        "machine": "Floor",
        "target": "30 sec/side",
        "sets": 3,
        "reps": "30 sec",
        "image": "",
        "video": "https://www.youtube.com/results?search_query=side+plank+proper+form",
        "purpose": "Lateral core and hip stability",
        "cue": "Lift hips and keep a straight line.",
        "mistakes": ["Hips dropping", "Rotating forward", "Neck tension", "Uneven sides"]
    },
    {
        "session": "Both",
        "name": "Dead Hang",
        "machine": "Pull-up Bar",
        "target": "30 sec",
        "sets": 3,
        "reps": "30 sec",
        "image": "",
        "video": "https://www.youtube.com/results?search_query=dead+hang+proper+form",
        "purpose": "Shoulder mobility, grip and decompression",
        "cue": "Relax the shoulders gently and breathe.",
        "mistakes": ["Forcing painful range", "Holding the breath", "Swinging", "Going to failure"]
    },
]


def get_recent_history(exercise_name, user, limit=3):
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("""
        SELECT created_at, session, exercise, set_no, weight, reps, rpe, notes
        FROM exercise_logs
        WHERE exercise = ?
          AND user = ?
        ORDER BY id DESC
        LIMIT ?
        """, (exercise_name, user, limit * 4)).fetchall()

    return [dict(r) for r in rows]


def parse_numeric_weight(weight):
    if weight is None:
        return None

    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*(?:kg)?\s*", str(weight), re.IGNORECASE)
    if not match:
        return None

    return float(match.group(1))


def parse_float(value):
    if value is None or value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


def format_number(value):
    if value is None:
        return "N/A"

    if float(value).is_integer():
        return str(int(value))

    return f"{value:.1f}"


def get_dashboard_data(user):
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        stats = con.execute("""
        SELECT
            COUNT(*) AS total_sets,
            COUNT(DISTINCT exercise) AS exercises_logged,
            MAX(created_at) AS last_workout
        FROM exercise_logs
        WHERE user = ?
        """, (user,)).fetchone()

        most_logged = con.execute("""
        SELECT exercise, COUNT(*) AS logged_sets
        FROM exercise_logs
        WHERE user = ?
        GROUP BY exercise
        ORDER BY logged_sets DESC, exercise ASC
        LIMIT 1
        """, (user,)).fetchone()

        latest = con.execute("""
        SELECT session
        FROM exercise_logs
        WHERE user = ?
        ORDER BY id DESC
        LIMIT 1
        """, (user,)).fetchone()

    latest_session = latest["session"] if latest else None
    suggested_session = "B" if latest_session == "A" else "A"

    return {
        "total_sets": stats["total_sets"],
        "exercises_logged": stats["exercises_logged"],
        "last_workout": stats["last_workout"][:10] if stats["last_workout"] else "No workouts yet",
        "most_logged_exercise": most_logged["exercise"] if most_logged else "No entries yet",
        "most_logged_sets": most_logged["logged_sets"] if most_logged else 0,
        "suggested_session": suggested_session,
        "suggested_label": f"Session {suggested_session}",
        "suggested_href": f"/gym?session={suggested_session}",
    }


def get_personal_best(exercise_name, user):
    with sqlite3.connect(DB) as con:
        rows = con.execute("""
        SELECT weight
        FROM exercise_logs
        WHERE exercise = ?
          AND user = ?
        """, (exercise_name, user)).fetchall()

    best = None
    for row in rows:
        numeric_weight = parse_numeric_weight(row[0])
        if numeric_weight is not None and (best is None or numeric_weight > best):
            best = numeric_weight

    return {
        "value": best,
        "label": f"{format_number(best)} kg" if best is not None else "No numeric PB yet",
    }


def get_previous_session_summary(exercise_name, user):
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        latest = con.execute("""
        SELECT substr(created_at, 1, 10) AS workout_date
        FROM exercise_logs
        WHERE exercise = ?
          AND user = ?
        ORDER BY id DESC
        LIMIT 1
        """, (exercise_name, user)).fetchone()

        if not latest:
            return None

        rows = con.execute("""
        SELECT created_at, weight, reps, rpe
        FROM exercise_logs
        WHERE exercise = ?
          AND user = ?
          AND substr(created_at, 1, 10) = ?
        ORDER BY id ASC
        """, (exercise_name, user, latest["workout_date"])).fetchall()

    weights = [parse_numeric_weight(r["weight"]) for r in rows]
    numeric_weights = [w for w in weights if w is not None]
    reps = [parse_float(r["reps"]) for r in rows]
    numeric_reps = [r for r in reps if r is not None]
    rpes = [parse_float(r["rpe"]) for r in rows]
    numeric_rpes = [r for r in rpes if r is not None]

    return {
        "date": latest["workout_date"],
        "best_weight": f"{format_number(max(numeric_weights))} kg" if numeric_weights else "No numeric weight",
        "total_sets": len(rows),
        "avg_reps": format_number(sum(numeric_reps) / len(numeric_reps)) if numeric_reps else "N/A",
        "avg_rpe": format_number(sum(numeric_rpes) / len(numeric_rpes)) if numeric_rpes else "N/A",
    }


def get_recommendation(exercise, user):
    rows = get_recent_history(exercise["name"], user, limit=1)

    if not rows:
        return {
            "status": "start",
            "message": "Start with the planned target and focus on controlled technique."
        }

    latest_date = rows[0]["created_at"][:10]
    latest_rows = [r for r in rows if r["created_at"][:10] == latest_date]

    target_reps = exercise["reps"]

    if not isinstance(target_reps, int):
        return {
            "status": "unclear",
            "message": "Repeat the current weight and log reps/RPE clearly next time."
        }

    reps = [parse_float(r["reps"]) for r in latest_rows]
    rpe_values = [parse_float(r["rpe"]) for r in latest_rows]

    if any(r is None for r in reps) or any(r is None for r in rpe_values):
        return {
            "status": "unclear",
            "message": "Repeat the current weight and log reps/RPE clearly next time."
        }

    if len(latest_rows) < exercise["sets"]:
        return {
            "status": "incomplete",
            "message": "Complete all prescribed sets before increasing weight."
        }

    reps_ok = all(r >= target_reps for r in reps)
    avg_rpe = sum(rpe_values) / len(rpe_values)

    if reps_ok and avg_rpe <= 8:
        return {
            "status": "increase",
            "message": "Consider a small increase next session, provided technique remains controlled."
        }

    if avg_rpe > 8:
        return {
            "status": "repeat",
            "message": "Repeat the current weight until it feels more controlled."
        }

    if not reps_ok:
        return {
            "status": "repeat",
            "message": "Repeat the current weight and aim to complete all prescribed reps."
        }

    return {
        "status": "repeat",
        "message": "Repeat the current weight and log reps/RPE clearly next time."
    }


@app.route("/")
def index():
    user = current_user()
    if not user:
        return render_template("login.html")

    return render_template("index.html", dashboard=get_dashboard_data(user), user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        selected_user = request.form.get("user", "")
        password = request.form.get("password", "")

        if selected_user in USERS and hmac.compare_digest(password, USERS[selected_user]):
            session.clear()
            session["user"] = selected_user
            return redirect(url_for("index"))

        return render_template(
            "login.html",
            selected_user=selected_user if selected_user in USERS else None,
            error="That password was not accepted. Please try again."
        )

    selected_user = request.args.get("user")
    return render_template(
        "login.html",
        selected_user=selected_user if selected_user in USERS else None
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/gym")
@login_required
def gym():
    user = current_user()
    session = request.args.get("session", "A")

    if session == "C":
        filtered = [e for e in EXERCISES if e["session"] == "Both"]
        title = "Session C – Core, Mobility & Finishers"
    else:
        filtered = [e for e in EXERCISES if e["session"] == session or e["session"] == "Both"]
        title = f"Session {session}"

    enriched = []
    for ex in filtered:
        ex_copy = ex.copy()
        ex_copy["history"] = get_recent_history(ex["name"], user)
        ex_copy["personal_best"] = get_personal_best(ex["name"], user)
        ex_copy["previous_summary"] = get_previous_session_summary(ex["name"], user)
        ex_copy["recommendation"] = get_recommendation(ex, user)
        enriched.append(ex_copy)

    return render_template(
        "gym.html",
        exercises=enriched,
        selected_session=session,
        title=title
    )


@app.route("/api/log", methods=["POST"])
@login_required
def save_log():
    user = current_user()
    data = request.json
    with sqlite3.connect(DB) as con:
        con.execute("""
        INSERT INTO exercise_logs
        (created_at, user, session, exercise, set_no, weight, reps, rpe, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(timespec="seconds"),
            user,
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
@login_required
def view_log():
    user = current_user()
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("""
        SELECT created_at, session, exercise, set_no, weight, reps, rpe, notes
        FROM exercise_logs
        WHERE user = ?
        ORDER BY id DESC
        """, (user,)).fetchall()
    return render_template("log.html", rows=rows, user=user)


@app.route("/admin")
@rynier_required
def admin():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        stats = con.execute("""
        SELECT
            COUNT(*) AS total_entries,
            COUNT(DISTINCT exercise) AS distinct_exercises,
            MAX(created_at) AS latest_entry
        FROM exercise_logs
        """).fetchone()

    db_size_kb = round(os.path.getsize(DB) / 1024, 1) if os.path.exists(DB) else 0

    return render_template(
        "admin.html",
        stats=stats,
        db_size_kb=db_size_kb,
        cleared=request.args.get("cleared") == "1"
    )


@app.route("/admin/export.csv")
@rynier_required
def export_workout_csv():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("""
        SELECT created_at, user, session, exercise, set_no, weight, reps, rpe, notes
        FROM exercise_logs
        ORDER BY id ASC
        """).fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["created_at", "user", "session", "exercise", "set_no", "weight", "reps", "rpe", "notes"])
    for row in rows:
        writer.writerow([
            row["created_at"],
            row["user"],
            row["session"],
            row["exercise"],
            row["set_no"],
            row["weight"],
            row["reps"],
            row["rpe"],
            row["notes"],
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=triad-workout-log.csv"}
    )


@app.route("/admin/download-db")
@rynier_required
def download_db():
    return send_file(DB, as_attachment=True, download_name="triad.db")


@app.route("/admin/clear", methods=["POST"])
@rynier_required
def clear_workout_history():
    if request.form.get("confirm_clear") == "yes":
        with sqlite3.connect(DB) as con:
            con.execute("DELETE FROM exercise_logs")
        return redirect(url_for("admin", cleared="1"))

    return redirect(url_for("admin"))
