async function saveSet(button) {
    const box = button.closest(".set-box");
    button.disabled = true;
    const originalText = button.textContent;

    const payload = {
        session: button.dataset.session,
        exercise: button.dataset.exercise,
        set_no: button.dataset.set,
        weight: fieldValue(box, "weight"),
        reps: fieldValue(box, "reps"),
        duration: fieldValue(box, "duration"),
        distance: fieldValue(box, "distance"),
        rpe: fieldValue(box, "rpe"),
        notes: fieldValue(box, "notes")
    };

    const response = await fetch("/api/log", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        button.textContent = "Draft Saved";
        button.style.background = "#6abf40";
    } else {
        button.textContent = "Error";
        button.style.background = "#cc0000";
    }

    window.setTimeout(() => {
        button.disabled = false;
        button.textContent = response.ok ? "Update Draft" : originalText;
        button.style.background = "";
    }, 1200);
}

function fieldValue(scope, field) {
    const input = scope.querySelector(`[data-field="${field}"]`);
    return input ? input.value : "";
}

function profileValue(scope, field) {
    const input = scope.querySelector(`[data-profile-field="${field}"]`);
    return input ? input.value : "";
}

async function saveMachineProfile(button) {
    const setup = button.closest(".machine-setup");
    button.disabled = true;
    const payload = {
        exercise: setup.dataset.exercise,
        seat_position: profileValue(setup, "seat_position"),
        cable_height: profileValue(setup, "cable_height"),
        backrest_position: profileValue(setup, "backrest_position"),
        handle_attachment: profileValue(setup, "handle_attachment"),
        foot_position: profileValue(setup, "foot_position"),
        notes: profileValue(setup, "notes")
    };

    const response = await fetch("/api/machine-profile", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    button.textContent = response.ok ? "Saved" : "Error";
    button.style.background = response.ok ? "#6abf40" : "#cc0000";

    window.setTimeout(() => {
        button.disabled = false;
        button.textContent = "Save Setup";
        button.style.background = "";
    }, 1200);
}

async function postWorkout(button) {
    const status = document.getElementById("post-status");
    const buttons = document.querySelectorAll(".post-workout-button");
    buttons.forEach((btn) => {
        btn.disabled = true;
        btn.textContent = "Posting...";
    });

    const response = await fetch("/api/post-workout", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({session: button.dataset.session})
    });

    const result = await response.json().catch(() => ({}));
    if (response.ok) {
        status.textContent = `Posted ${result.posted_sets} set${result.posted_sets === 1 ? "" : "s"} to your workout log.`;
        status.className = "post-status success";
        window.setTimeout(() => window.location.reload(), 900);
    } else {
        status.textContent = result.message || "Could not post workout.";
        status.className = "post-status error";
        buttons.forEach((btn) => {
            btn.disabled = false;
            btn.textContent = "Post Workout";
        });
    }
}
