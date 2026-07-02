# Project TRIAD Release Backlog

## Purpose

This document captures observations, training feedback, improvement ideas and planned enhancements for future Project TRIAD releases.

It is updated from real training use, especially feedback after gym, swim, bike and run sessions.

---

# Current Stable Release

## Release 2.6

Status: Stable

Includes:

- Multi-user login
- Users: Rynier and Wietz
- User-specific workout logs
- User-specific history
- User-specific personal bests
- Rynier-only admin access
- Environment-based passwords
- Docker deployment

---

# Release 2.7 Candidate Backlog

## High Priority

### Timed Exercise Support
- Replace the current reps field for timed exercises with a dedicated duration field.
- Introduce exercise types:
  - Standard
  - Timed
  - Bodyweight
  - Loaded Carry

Affected exercises:
- Front Plank
- Side Plank
- Dead Hang

### Exercise Numbering
Display the exercise order clearly:
1. Plate Loaded Pulldown
2. Low Row Machine
3. Pullover
...

### Rename Seated Cable Row
Rename to:
Low Row Machine

Optional subtitle:
Horizontal Pull / Seated Row Pattern

### Machine Profiles
Store machine setup information such as:
- Seat position
- Cable height
- Backrest position
- Handle attachment
- Foot position
- Personal notes

### Previous Machine Settings
Display previous machine settings automatically before starting an exercise.

---

# Session A Feedback

Date:
2026-06-30

Purpose:
- Learn machines
- Benchmark starting weights
- Test TRIAD workflow
- Capture first real training data

Training observations:

Plate Loaded Pulldown
- Suggested next session:
  - 50 kg
  - 55 kg
  - 60 kg

Low Row Machine
- Rename exercise.
- Suggested next session:
  - 40 kg
  - 40 kg
  - 40 kg

Pullover
- Suggested next session:
  - 25 kg
  - 30 kg
  - 30 kg

Chest Press
- Repeat 30 kg.

Shoulder Press
- Reduce to 15–17.5 kg.

Triceps Pushdown
- Reduce to 20 kg.

Face Pull
- Repeat 15 kg.

External Rotation
- Repeat 5 kg.

Pallof Press
- 15 kg all sets.

Core
- Improve timed exercise logging.

---

# Medium Priority Ideas

- Workout completion summary
- Session duration
- Rest timer
- Better mobile navigation
- Next Exercise button
- Quick post-workout notes
- Workout difficulty
- Energy level
- Pain/discomfort notes
- Training readiness

---

# Future Ideas

- Exercise progress charts
- Weekly training summary
- AI coaching notes
- Automatic progression
- Garmin integration
- n8n coaching emails
- Swim module
- Bike module
- Run module
- Recovery
- Nutrition

---

# Working Process

At the beginning of every release planning discussion, provide the latest version of this file. It will be updated with new observations, prioritised enhancements and coaching decisions before the next release is implemented.

---

# Notes

Release 2.7 should be driven by real training feedback before implementation.


---

# Session B Feedback

## Date
2026-07-01

## Summary
Second real training session and first execution of Session B.

Purpose:
- Establish lower-body working weights
- Evaluate the new Lat Pulldown exercise
- Validate progression philosophy
- Continue refining TRIAD using real training feedback

## Coaching Observations

### Lat Pulldown
- Excellent baseline.
- Increase slightly next session (42.5–45 kg depending on machine increments).

### Deadlift Machine
- Repeat 40 kg.

### Leg Press
- Standardise at 80 kg for all working sets.

### Hack Squat
- Maintain 10 kg while prioritising depth and technique.

### Leg Curl
- Repeat 40 kg.
- Remember:
  - Seat position 6
  - Arm position 2

### Standing Calf Raise
- Consider a small increase to approximately 70 kg.

### Hip Thrust
- Repeat current load.

### Farmer's Carry
- Increase load until final effort reaches approximately RPE 8–9.

### Core
- Confirms the need for dedicated timed exercise support.

## New High Priority Enhancements

### Workout Draft Mode

Current issue:
Workout sets are immediately written to the permanent workout log, making accidental entries difficult to correct.

Proposed workflow:
- Exercise form starts blank.
- User enters sets and presses Save.
- Saved values remain visible and editable.
- Pressing Save again updates the draft instead of creating duplicate records.
- A new Post Workout button commits all exercises to the permanent workout log.
- Draft data is then cleared.

Benefits:
- Prevents accidental duplicate entries.
- Supports corrections during training.
- Allows partially completed workouts.
- Separates active workouts from completed history.

### Duplicate Entry Protection

Prevent multiple saves caused by accidental repeated taps.

## Additional Observations

- Pulling strength continues to exceed pressing strength.
- Conservative progression remains appropriate.
- Machine setup information should become a dedicated feature rather than relying on notes.
