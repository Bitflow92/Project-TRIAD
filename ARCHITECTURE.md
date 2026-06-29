# ARCHITECTURE.md

# Project TRIAD Architecture

## Overview

Project TRIAD is a self-hosted endurance coaching platform built around Flask, Docker and SQLite.

The architecture prioritises simplicity, maintainability and full ownership of athlete data.

---

# Source Control

GitHub

Repository:

Project-TRIAD

Branches:

main
Production

develop
Development

GitHub is the single source of truth.

---

# Development Workflow

ChatGPT

↓

Architecture
Planning
Release Design

↓

Codex

↓

Implementation

↓

GitHub Desktop

↓

GitHub

↓

VPS

↓

Docker Deployment

---

# Technology Stack

Frontend

- HTML5
- CSS3
- JavaScript

Backend

- Flask
- Gunicorn

Database

SQLite

Reverse Proxy

Caddy

Container

Docker

Operating System

Ubuntu VPS

Version Control

Git
GitHub

IDE

VS Code

Implementation

Codex

Architecture

ChatGPT

---

# Folder Structure

Project-TRIAD

docs/

platform/

app/

templates/

static/

instance/

Dockerfile

docker-compose.yml

deploy.sh

rollback.sh

---

# Deployment Flow

Developer

↓

Git Commit

↓

GitHub Push

↓

VPS

git pull

↓

deploy.sh

↓

Docker Build

↓

Container Restart

↓

Caddy

↓

Production

---

# Database

SQLite

Database file

instance/triad.db

Current Tables

exercise_logs

Future tables

athlete

equipment

sessions

swims

rides

runs

nutrition

recovery

pb_records

coach_notes

---

# Security Philosophy

- HTTPS only
- Docker isolation
- Reverse proxy via Caddy
- Local SQLite database
- GitHub version control
- VPS as deployment target only

---

# Design Philosophy

Visual identity

Apple meets Garmin

Development philosophy

Simple
Reliable
Maintainable
Mobile-first
Self-hosted
AI-enabled

---

# Future Architecture

Future releases will introduce:

- Modular Flask architecture
- Service layer
- REST API
- Authentication
- AI Coaching Engine
- Garmin integration
- Apple Health integration
- n8n automation
- Multi-athlete support