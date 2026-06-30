# Project TRIAD

## Release Notes

Current Release: **2.5**

Release Date: June 2026

Status: Stable

---

# Overview

Release 2.5 marks the completion of the Project TRIAD platform foundation.

The application has evolved from a simple static gym programme into a self-hosted coaching platform featuring workout logging, progress tracking, intelligent progression recommendations, administration tools and a modern Docker-based deployment workflow.

This release establishes the technical foundation upon which future endurance coaching, analytics and AI features will be built.

---

# What's New

## Coaching Dashboard

- Modern landing dashboard
- Session A / B / C navigation
- Mobile-friendly interface
- Improved visual design

## Workout Logging

- Record every exercise session
- Store weights, repetitions and notes
- Persistent SQLite database

## Progress Intelligence

- Previous performance displayed
- Personal Best tracking
- Conservative progression recommendations
- Historical workout review

## Exercise Library

Each exercise now includes:

- Machine photographs
- Primary purpose
- Coaching cue
- Common mistakes
- Video reference links

## Administration

Administrator tools include:

- CSV export
- SQLite database download
- Workout history
- Database maintenance
- Clear workout log

## Infrastructure

Major improvements include:

- Dockerized deployment
- Caddy reverse proxy
- SQLite persistence
- Automated deployment script
- Automated rollback script
- GitHub-managed source control
- VPS deployment workflow

---

# Current Platform

Live Platform

https://triad.bitflow92.co.za

Project Website

https://bitflow92.github.io/Project-TRIAD/

---

# Technology

- Python
- Flask
- SQLite
- Docker
- Caddy
- GitHub
- GitHub Pages
- Codex
- ChatGPT

---

# Known Limitations

The following functionality is planned but not yet implemented.

- Athlete profile
- Swim training
- Cycling training
- Running training
- Nutrition tracking
- Recovery dashboard
- Performance analytics
- Garmin integration
- AI coaching
- n8n automation

---

# Upgrade Notes

No manual upgrade steps are required.

Deployment consists of:

```
git pull
./platform/deploy.sh
```

The deployment script automatically:

- updates the application
- rebuilds the Docker image
- restarts the container
- performs a health check

---

# Next Release

Release 2.6

Project Website

Focus areas include:

- Professional GitHub Pages landing page
- Public project presentation
- Better onboarding experience
- Improved branding
- Documentation improvements

---

Project TRIAD

Train smarter.

Recover better.

Race stronger.

"You can do it!"