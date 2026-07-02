# Project TRIAD

## Release Notes

Current Release: **2.7**

Release Date: July 2026

Status: Stable

---

# Overview

Release 2.7 improves the in-gym workout experience by making logging safer, more flexible and more coaching-aware.

The workout screen now supports exercise-specific inputs, editable workout drafts, machine setup memory and improved exercise photography while preserving the Release 2.6 multi-user authentication and Rynier-only administration model.

---

# What's New

## Workout Draft Mode

- Saving a set now stores an editable draft instead of immediately posting to the permanent log.
- Drafts are user-specific and session-specific.
- Saving the same set again updates the draft row instead of creating duplicates.
- The new **Post Workout** action writes completed draft sets to permanent history and clears the draft.
- Partially completed workouts are supported.

## Exercise Type Support

- Standard exercises use weight, reps, RPE and notes.
- Timed exercises use duration, RPE and notes.
- Loaded carries use weight, distance/time, RPE and notes.
- The permanent log and CSV export now support duration and distance fields.

## Machine Profiles

- Each athlete can save machine setup notes per exercise.
- Setup fields include seat position, cable height, backrest, handle attachment, foot position and notes.
- Saved setup appears automatically on the relevant exercise card.

## Exercise Card Redesign

- Exercise cards now show numbered exercise titles in workout order.
- Desktop and tablet layouts use a photo-plus-coaching split.
- Mobile layouts stack photo, coaching, machine setup and draft inputs.
- Release 2.7 photography assets were added for key machine exercises.

## Coaching Intelligence

- Timed exercise recommendations remain conservative and focus on repeating duration until RPE improves.
- Loaded carry recommendations avoid aggressive progression and account for distance/time variability.
- Existing conservative progression logic remains in place for standard exercises.

## Administration

- CSV export includes the new exercise order, exercise type, duration and distance fields.
- Workout history clearing still only clears permanent logs.
- Draft clearing is available as a separate admin action.
- Machine profiles are not deleted by workout history or draft clear actions.

---

# Upgrade Notes

No manual migration command is required. On startup, the Flask app safely adds compatible columns to `exercise_logs` and creates the `workout_drafts` and `machine_profiles` tables if they do not already exist.

Deployment remains:

```
git pull
./platform/deploy.sh
```

---

# Known Limitations

- Timed exercise progression intentionally remains conservative in Release 2.7.
- Machine setup fields are free text to match real gym equipment variability.
- Historical Seated Cable Row entries are still used for history and recommendations, while new entries use Low Row Machine.

---

Project TRIAD

Train smarter.

Recover better.

Race stronger.

"You can do it!"
