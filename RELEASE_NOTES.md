# Project TRIAD

## Release Notes

Current Release: **2.7.1**

Release Date: July 2026

Status: Stable

---

# Overview

Release 2.7.1 builds on the Release 2.7 workout experience with editable coaching plans and cleaner machine setup handling.

The workout screen can now show user-specific coach targets, prescriptions and recommendations without code changes, while Machine Setup stays compact until the athlete needs it.

---

# What's New

## Coaching Plans

- Rynier can manage per-athlete coaching plans from `/admin/coaching`.
- Coaching plans can override Target, Sets/Prescription and Recommendation per user, session and exercise.
- Rynier and Wietz can have different coaching plans.
- Blank coaching plan fields fall back to the default programme and existing TRIAD recommendation logic.
- JSON upload is supported for bulk coaching plan updates.

## Collapsible Machine Setup

- Machine Setup now behaves like Recent History.
- Exercises without saved setup show a compact “No setup saved yet” summary.
- Exercises with saved setup open automatically and show a compact summary such as “Seat 7 • Cable 20”.

---

# Release 2.7 Highlights

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

No manual migration command is required. On startup, the Flask app safely adds compatible columns to `exercise_logs` and creates the `workout_drafts`, `machine_profiles` and `coaching_plans` tables if they do not already exist.

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
- Coaching plan management is currently admin-only.

---

Project TRIAD

Train smarter.

Recover better.

Race stronger.

"You can do it!"
