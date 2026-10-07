# Fitness Log Application

A full-stack Flask web app for logging strength workouts and reviewing training history.

![Dashboard screenshot](screenshots/dashboard.png)

## Features

- Log workouts with multiple exercises, each with sets, reps, and weight
- JavaScript-driven form for adding exercises and sets dynamically
- Dashboard of past workout sessions
- Relational schema covering users, exercises, workouts, and set entries

## Tech Stack

Python, Flask, SQLAlchemy, SQLite, JavaScript, HTML/CSS

## Getting Started

1. Clone the repo and enter the folder:
```bash
   git clone https://github.com/cschleyer-2004/fitness-log-application
   cd fitness-log-application
```
2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Run the app:
```bash
   [flask run / python3 main.py]
```
5. Open http://localhost:5000 in your browser.

## Status

In active development. [Planned next: e.g., progress charts, edit/delete workouts.]