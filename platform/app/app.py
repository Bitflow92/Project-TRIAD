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


def get_recent_history(exercise_name, limit=3):
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("""
        SELECT created_at, session, exercise, set_no, weight, reps, rpe, notes
        FROM exercise_logs
        WHERE exercise = ?
        ORDER BY id DESC
        LIMIT ?
        """, (exercise_name, limit * 4)).fetchall()

    return [dict(r) for r in rows]


def get_recommendation(exercise):
    rows = get_recent_history(exercise["name"], limit=1)

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
            "status": "repeat",
            "message": "Repeat the current target and focus on clean form."
        }

    try:
        reps_ok = all(int(r["reps"]) >= target_reps for r in latest_rows if r["reps"])
        rpe_values = [float(r["rpe"]) for r in latest_rows if r["rpe"]]
        avg_rpe = sum(rpe_values) / len(rpe_values) if rpe_values else 10
        sets_ok = len(latest_rows) >= exercise["sets"]
    except ValueError:
        return {
            "status": "repeat",
            "message": "Repeat the current weight until reps and RPE are logged clearly."
        }

    if sets_ok and reps_ok and avg_rpe <= 8:
        return {
            "status": "increase",
            "message": "Consider a small increase next session, provided technique remains controlled."
        }

    return {
        "status": "repeat",
        "message": "Repeat the current weight and focus on clean form."
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gym")
def gym():
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
        ex_copy["history"] = get_recent_history(ex["name"])
        ex_copy["recommendation"] = get_recommendation(ex)
        enriched.append(ex_copy)

    return render_template(
        "gym.html",
        exercises=enriched,
        selected_session=session,
        title=title
    )


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