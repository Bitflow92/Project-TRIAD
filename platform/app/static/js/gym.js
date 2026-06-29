async function saveSet(button) {
    const box = button.closest(".set-box");

    const payload = {
        session: button.dataset.session,
        exercise: button.dataset.exercise,
        set_no: button.dataset.set,
        weight: box.querySelector('[data-field="weight"]').value,
        reps: box.querySelector('[data-field="reps"]').value,
        rpe: box.querySelector('[data-field="rpe"]').value,
        notes: box.querySelector('[data-field="notes"]').value
    };

    const response = await fetch("/api/log", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        button.textContent = "Saved ✓";
        button.style.background = "#6abf40";
    } else {
        button.textContent = "Error";
        button.style.background = "#cc0000";
    }
}