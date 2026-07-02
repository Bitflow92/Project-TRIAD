# Project TRIAD Product Backlog

## Purpose

This backlog captures observations from real training sessions and
converts them into prioritised product improvements. Every enhancement
should be traceable to the workout, discussion or coaching insight that
inspired it.

------------------------------------------------------------------------

# Current Stable Release

**Release:** 2.6\
**Status:** Stable

Highlights:

-   Multi-user authentication (Rynier / Wietz)
-   User-specific workout history
-   Personal Best tracking
-   Rynier-only administration
-   Docker deployment
-   Environment-based configuration

------------------------------------------------------------------------

# Release 2.7 Candidate Backlog

## HIGH PRIORITY

------------------------------------------------------------------------

### Feature: Timed Exercise Support

**Priority:** High\
**Status:** Planned\
**Target Release:** 2.7\
**Category:** Workout UX

**Problem**

Timed exercises currently use the repetitions field to store seconds.

**Proposed Solution**

Introduce exercise types:

-   Standard (Weight + Reps)
-   Timed (Duration)
-   Bodyweight
-   Loaded Carry

Affected exercises:

-   Front Plank
-   Side Plank
-   Dead Hang

**Benefits**

-   Cleaner data
-   Better progress tracking
-   Future analytics

**Origin**

Session A & Session B

------------------------------------------------------------------------

### Feature: Workout Draft Mode

**Priority:** High\
**Status:** Planned\
**Target Release:** 2.7\
**Category:** Data Entry

**Problem**

Every press of Save immediately writes to the permanent workout log,
making corrections difficult and allowing duplicate entries.

**Proposed Solution**

Create a temporary workout draft.

Workflow:

1.  Exercise form starts blank.
2.  Save stores values in the current workout draft.
3.  Saved values remain editable.
4.  Saving again updates the draft.
5.  A new **Post Workout** button commits all draft data to the
    permanent workout log.
6.  Draft data is then cleared.

**Benefits**

-   Prevents accidental duplicates
-   Allows corrections
-   Supports partially completed workouts
-   Foundation for Resume Workout

**Origin**

Session B + user suggestion

------------------------------------------------------------------------

### Feature: Machine Profiles

**Priority:** High\
**Status:** Planned\
**Target Release:** 2.7\
**Category:** Coaching

**Problem**

Machine setup information is hidden inside notes.

**Proposed Solution**

Store:

-   Seat position
-   Cable height
-   Backrest
-   Handle attachment
-   Personal notes

Display these automatically before each workout.

**Benefits**

-   Faster setup
-   Consistent execution
-   Less cognitive load

**Origin**

Session A & B

------------------------------------------------------------------------

### Feature: Exercise Numbering

**Priority:** High\
**Status:** Planned\
**Target Release:** 2.7\
**Category:** UI

Number exercises in workout order.

**Origin**

Session A

------------------------------------------------------------------------

### Feature: Rename Seated Cable Row

**Priority:** High\
**Status:** Planned\
**Target Release:** 2.7\
**Category:** Exercise Library

Rename to:

**Low Row Machine**

**Origin**

Session A

------------------------------------------------------------------------

### Feature: Duplicate Entry Protection

**Priority:** High\
**Status:** Planned\
**Target Release:** 2.7\
**Category:** Reliability

Disable repeated Save taps or intelligently detect duplicate
submissions.

**Origin**

Session B

------------------------------------------------------------------------

# Coaching Baselines

## Session A (2026-06-30)

  Exercise                Next Recommendation
  ----------------------- ---------------------
  Plate Loaded Pulldown   50 / 55 / 60 kg
  Low Row Machine         40 / 40 / 40 kg
  Pullover                25 / 30 / 30 kg
  Chest Press             Repeat 30 kg
  Shoulder Press          15--17.5 kg
  Triceps Pushdown        20 kg
  Face Pull               Repeat 15 kg
  External Rotation       Repeat 5 kg
  Pallof Press            15 kg all sets
  Front Plank             60 sec
  Side Plank              30 sec
  Dead Hang               30 sec

## Session B (2026-07-01)

  Exercise              Next Recommendation
  --------------------- ----------------------
  Lat Pulldown          42.5--45 kg
  Deadlift Machine      Repeat 40 kg
  Leg Press             80 / 80 / 80 kg
  Hack Squat            Repeat 10 kg
  Leg Curl              Repeat 40 kg
  Standing Calf Raise   \~70 kg
  Hip Thrust            Repeat current load
  Farmer's Carry        Increase to RPE 8--9
  Core                  Repeat durations

------------------------------------------------------------------------

# Medium Priority

-   Workout completion summary
-   Session duration
-   Rest timer
-   Next Exercise button
-   Energy rating
-   Pain/discomfort notes
-   Training readiness

------------------------------------------------------------------------

# Future Vision

-   Swim module
-   Bike module
-   Run module
-   Recovery module
-   Nutrition module
-   AI coaching
-   Garmin integration
-   Weekly coaching email via n8n

------------------------------------------------------------------------

# Working Process

At the start of each release planning session:

1.  Open this document.
2.  Add new observations.
3.  Prioritise enhancements.
4.  Mark completed items.
5.  Generate the Codex implementation prompt from this backlog.

This document becomes the single source of truth for Project TRIAD
feature planning.
