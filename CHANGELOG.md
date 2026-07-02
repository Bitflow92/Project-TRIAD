# CHANGELOG.md

# Changelog

All notable changes to Project TRIAD will be documented in this file.

The project follows the principles of semantic release documentation.

---

# Release 2.7.1

## Added

- User-specific coaching plans for target, prescription and coach recommendation overrides
- Rynier-only Coaching Plans admin page
- Coaching plan JSON upload support
- `coaching_plans` database table with user/session/exercise upserts

## Changed

- Machine Setup sections now collapse by default and open automatically when saved setup data exists
- Workout cards show Coach Recommendation when a coaching plan recommendation is available
- Workout cards fall back to existing TRIAD recommendations and default programme values when no coaching plan exists

---

# Release 2.7

## Added

- Timed, loaded carry, bodyweight and standard exercise type support
- Editable workout draft mode with explicit Post Workout action
- Duplicate draft protection with user/session/exercise/set upserts
- User-specific machine setup profiles per exercise
- Duration and distance fields for workout logs and CSV export
- Exercise numbering and compact machine setup display
- Release 2.7 machine photography assets

## Changed

- Redesigned workout exercise cards with photo/coaching layout
- Renamed Seated Cable Row to Low Row Machine while preserving historical lookup
- Updated conservative recommendations for timed exercises and loaded carries
- Improved workout log display for weight, reps, duration and distance
- Added separate admin draft clearing without deleting posted logs or machine profiles

---

# Release 2.6

## Added

- Multi-user authentication for Rynier and Wietz
- Individual athlete data separation
- Rynier-only admin access

## Changed

- Docker Compose uses `.env` for deployment secrets

---

# Release 2.5

## Added

- Coaching dashboard homepage
- Dashboard statistics
- Suggested next workout
- Personal Best tracking
- Previous session summaries
- Progress badges on exercise cards

## Changed

- Improved conservative progression recommendations
- Improved mobile dashboard and exercise-card scanning

---

# Release 2.4

## Added

- Admin Dashboard
- Workout statistics
- CSV export
- SQLite database download
- Clear workout history
- Exercise history
- Conservative progression recommendations

## Changed

- Navigation updated with Admin page
- Improved workout cards
- Improved styling

## Fixed

- Machine image mapping
- Responsive layout improvements
- Exercise recommendation logic

---

# Release 2.3

## Added

- Exercise images
- Technique video links
- Primary purpose
- Coaching cues
- Common mistakes
- Session C
- Session A/B improvements

## Changed

- Session B updated with Lat Pulldown
- Improved mobile layout

---

# Release 2.2

## Added

- SQLite workout logging
- Workout history
- Docker deployment
- VPS hosting
- GitHub deployment workflow

---

# Release 2.1

## Added

- Flask application
- Home page
- Session A
- Session B
- Exercise logging
- Docker environment

---

# Release 2.0

## Initial Release

- Project structure
- Static HTML prototype
- Initial gym programme
- Exercise cards
- Mobile layout
