You are working in the Project-TRIAD repository on the develop branch.

Implement Release 2.7 – Workout Experience & Coaching Intelligence.

Important:

- Preserve all existing Release 2.6 functionality.

- Do not modify the main branch.

- Keep the current Flask structure unless small helper functions are needed.

- Do not introduce unnecessary dependencies.

- Maintain the Apple/Garmin Project TRIAD look and feel.

- Mobile-first design remains critical.

- Use PRODUCT_BACKLOG.md and COACHING_PHILOSOPHY.md as guiding documents.

- The source photos for Release 2.7 are in:

  reference/Release-2.7-photos/

- The final app images must live in:

  platform/app/static/images/machines/

Current app:

- Flask app: platform/app/app.py

- Templates: platform/app/templates/

- CSS: platform/app/static/css/triad.css

- JS: platform/app/static/js/gym.js

- SQLite database: /instance/triad.db

- Docker Compose already uses .env for secrets.

- Multi-user authentication exists for Rynier and Wietz.

- Rynier-only admin exists.

Release 2.7 goals:

1. Timed Exercise Support

Add exercise-type support.

Exercise types:

- standard: weight + reps + RPE

- timed: duration seconds + RPE

- loaded_carry: weight + distance/metres or duration + RPE

- bodyweight: reps + RPE

Apply:

- Front Plank = timed

- Side Plank = timed

- Dead Hang = timed

- Farmer's Carry = loaded_carry

- all normal gym exercises = standard

The UI should display the correct input labels per exercise type.

Examples:

- Timed: Duration (sec), RPE, Notes

- Loaded carry: Weight, Distance / Time, RPE, Notes

- Standard: Weight, Reps, RPE, Notes

Existing database can remain compatible, but add columns if useful:

- exercise_type

- duration

- distance

If database migration is needed, do it safely with ALTER TABLE checks.

Existing old data must remain usable.

2. Workout Draft Mode

Current problem:

Saving a set immediately writes to the permanent log and accidental duplicates can occur.

Implement a workout draft workflow:

- When a user opens a session, the set fields are blank unless a draft exists.

- Pressing Save stores or updates the set in a draft, not the final exercise_logs table.

- Saved values remain visible and editable.

- Pressing Save again updates the same draft row.

- Add a prominent “Post Workout” button at the bottom and top of the workout page.

- Pressing “Post Workout” writes all draft sets for the current user/session into the permanent workout log.

- After posting, clear the draft for that user/session.

- Support partially completed workouts.

- If user leaves and returns, the draft should still be visible.

- Drafts should be user-specific.

- Drafts should be session-specific.

Suggested database:

- workout_drafts table:

  id

  user

  session

  exercise

  exercise_order

  set_no

  exercise_type

  weight

  reps

  duration

  distance

  rpe

  notes

  updated_at

Posting should insert into exercise_logs and then delete the relevant draft rows.

3. Duplicate Entry Protection

- Prevent repeated accidental saves from creating duplicates.

- Disable Save button briefly after save.

- Draft table should enforce uniqueness:

  user + session + exercise + set_no

- Save should upsert rather than insert duplicates.

4. Machine Profiles

Add user-specific machine profile support.

Create table:

machine_profiles

- id

- user

- exercise

- seat_position

- cable_height

- backrest_position

- handle_attachment

- foot_position

- notes

- updated_at

On exercise cards:

- Show machine profile fields in a compact “Machine Setup” section.

- Allow user to save/edit profile fields.

- Machine setup should persist per user and per exercise.

- Display previous saved setup automatically.

5. Previous Machine Settings Display

- Display saved machine setup prominently on each exercise card.

- If no setup exists, show a friendly prompt:

  “No machine setup saved yet.”

6. Exercise Numbering

- Add exercise order to each exercise card.

- Display titles like:

  “1. Plate Loaded Pulldown”

  “2. Low Row Machine”

- Ensure numbering follows workout order.

7. Rename Seated Cable Row

- Rename “Seated Cable Row” to “Low Row Machine”.

- Keep movement context somewhere as:

  “Horizontal Pull / Seated Row Pattern”

- Update image reference to use low row naming if required.

- Existing historical entries under “Seated Cable Row” should still be handled gracefully where possible.

8. Exercise Card Redesign & High-Quality Photography

Use the new source photos in:

reference/Release-2.7-photos/

Tasks:

- Optimise/copy selected source images into:

  platform/app/static/images/machines/

- Use stable final names, for example:

  plate_loaded_pulldown.jpg

  low_row_machine.jpg

  lat_pulldown.jpg

  chest_press.jpg

  deadlift_machine.jpg

  farmers_carry.jpg

- Update app.py exercise image references accordingly.

- Remove obsolete unused image files only if they are definitely no longer referenced.

- Do not delete the source photos in reference/Release-2.7-photos/.

Redesign exercise cards:

Desktop/tablet:

- Photo on the left.

- Coaching panel on the right.

- Include:

  - Primary purpose

  - Coaching cue

  - Technique video

  - PB

  - Previous session summary

  - TRIAD recommendation

  - Machine setup

Mobile:

- Stack vertically:

  - Photo

  - Coaching information

  - Machine setup

  - Draft set inputs

Avoid wasted white space.

Avoid poorly cropped/centred images.

Use object-fit/object-position appropriately.

9. Update Recommendations Carefully

Existing conservative progression logic must remain aligned with COACHING_PHILOSOPHY.md.

For timed exercises:

- Do not recommend aggressive increases.

- Suggest repeat until RPE improves.

- Later we can progress duration, but keep Release 2.7 conservative.

For loaded carry:

- Treat distance/time and RPE carefully.

- Do not break if data is non-standard.

10. Update Admin

Admin export should still work.

If new exercise_logs columns are added, include them in CSV export.

Admin clear should clear permanent workout logs.

Draft data should either:

- be shown separately, or

- be cleared through a separate admin action if simple.

Do not accidentally delete machine profiles unless explicitly designed.

11. Update Log View

Workout log should display new fields gracefully:

- weight

- reps

- duration

- distance

- rpe

- notes

Hide empty fields where practical or display cleanly.

12. Update Documentation

Update:

- CHANGELOG.md

- RELEASE_NOTES.md

- PRODUCT_BACKLOG.md

In PRODUCT_BACKLOG.md:

- Mark implemented Release 2.7 items as completed or moved to release history.

- Keep future ideas intact.

In RELEASE_NOTES.md:

- Current release should become Release 2.7.

- Summarise major changes.

Testing:

Run:

python3 -m py_compile platform/app/app.py

Manually test:

- Unauthenticated users see login.

- Rynier login works.

- Wietz login works.

- Rynier sees Admin.

- Wietz does not see Admin.

- Session A opens.

- Session B opens.

- Session C opens.

- Timed exercises show Duration field.

- Farmer's Carry shows loaded carry fields.

- Saving a set saves draft but not permanent log.

- Saved draft values remain visible.

- Editing a draft and saving updates, not duplicates.

- Post Workout writes to permanent log.

- Draft clears after posting.

- Permanent log shows posted data.

- Machine setup saves and reloads.

- Exercise cards show improved photos and layout.

- Admin export still works.

- Mobile layout has no horizontal overflow.

After implementation, summarise:

- Files changed

- Database migrations added

- New tables added

- Routes added or changed

- How to test

- Any assumptions made