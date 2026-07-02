# Project TRIAD Product Backlog

## Purpose

This document is the single source of truth for Project TRIAD product planning. It captures observations from real training, prioritises enhancements, records coaching decisions and defines the scope of upcoming releases.

---

# Product Vision

Project TRIAD aims to become an AI-assisted endurance coaching platform that reduces cognitive load during training while helping athletes train consistently, safely and intelligently.

Primary objectives:

- Deliver an exceptional mobile workout experience.
- Remember everything the athlete should not have to remember.
- Provide transparent coaching recommendations based on evidence and training history.
- Grow from strength training into a complete swim, bike, run and recovery platform.

---

# Current Release

**Release:** 2.6  
**Status:** Stable

Major capabilities:

- Multi-user authentication
- Individual athlete data
- Personal Best tracking
- Workout history
- Dashboard
- Administration
- Docker deployment
- GitHub-managed development

---

# Next Planned Release

## Release 2.7

**Theme:** Workout Experience & Coaching Intelligence

**Status:** Planning

---

# Ready for Codex

- [ ] Timed Exercise Support
- [ ] Workout Draft Mode
- [ ] Machine Profiles
- [ ] Previous Machine Settings
- [ ] Exercise Numbering
- [ ] Rename Seated Cable Row → Low Row Machine
- [ ] Duplicate Entry Protection

Only these items should be implemented unless the scope is deliberately expanded.

---

# Product Backlog

## High Priority

### Timed Exercise Support
- **Status:** Planned
- **Category:** Workout UX
- **Target:** Release 2.7

**Problem:** Timed exercises currently use the repetitions field.

**Solution:** Support Standard, Timed, Bodyweight and Loaded Carry exercise types.

**Origin:** Sessions A & B

---

### Workout Draft Mode
- **Status:** Planned
- **Category:** Data Entry
- **Target:** Release 2.7

**Problem:** Sets are immediately written to the permanent log.

**Solution:** Maintain an editable workout draft and commit only when the athlete presses **Post Workout**.

**Benefits:**
- Prevent accidental entries
- Allow corrections
- Support incomplete workouts
- Foundation for Resume Workout

**Origin:** Session B

---

### Machine Profiles
- **Status:** Planned
- **Category:** Coaching
- **Target:** Release 2.7

Store:
- Seat position
- Cable height
- Backrest
- Handle attachment
- Personal notes

Automatically display these during future workouts.

**Origin:** Sessions A & B

---

### Previous Machine Settings
- **Status:** Planned
- **Category:** Coaching
- **Target:** Release 2.7

Automatically display previous setup and previous working weight before each exercise.

**Origin:** Sessions A & B

---

### Exercise Numbering
Target: Release 2.7

Display exercises as 1, 2, 3...

Origin: Session A

---

### Rename Seated Cable Row
Target: Release 2.7

Rename to **Low Row Machine**.

Origin: Session A

---

### Duplicate Entry Protection
Target: Release 2.7

Prevent accidental multiple submissions.

Origin: Session B

---

# Coaching Decisions

## Strength Progression

Maintain weight until:

- All prescribed repetitions are achieved.
- Technique remains consistent.
- Final set RPE is approximately 8.

Only then increase using the smallest practical increment.

## Coaching Priority

1. Technique
2. Consistency
3. Progression
4. Load

---

# Training Observations

## Session A (2026-06-30)

- Established upper-body baselines.
- Pulling strength exceeded pressing strength.
- Machine setup notes proved valuable.
- Timed exercises require dedicated support.

## Session B (2026-07-01)

- Lower-body baselines established.
- Farmer's Carry load too conservative.
- Hack Squat depth prioritised over load.
- Duplicate save behaviour observed.
- Machine profiles confirmed as valuable.

---

# Medium Priority

- Workout completion summary
- Session duration
- Rest timer
- Next Exercise button
- Workout difficulty
- Energy level
- Pain/discomfort
- Training readiness

---

# Future Vision

- Swim module
- Bike module
- Run module
- Recovery
- Nutrition
- AI coaching
- Garmin integration
- n8n coaching automation

---

# Release History

- 2.3 Exercise Library
- 2.4 Administration
- 2.5 Dashboard & Coaching Experience
- 2.6 Multi-user Authentication

---

# Working Process

1. Train.
2. Capture observations.
3. Update this document.
4. Prioritise.
5. Generate the Codex prompt.
6. Implement.
7. Test.
8. Release.
