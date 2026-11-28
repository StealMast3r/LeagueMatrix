# LeagueMatrix

LeagueMatrix is a Python project for collecting, storing, and exploring **League of Legends** data. It uses the Riot Games API, a MySQL database, and a Flask web application.

## Features

- Retrieve player and account information using Riot IDs.
- Collect ranked entries, champion mastery, match history, match details, and timelines.
- Store League of Legends data in a MySQL database.
- Browse data through a Flask web interface.
- Use Data Dragon and Riot static data for game-related information.

## Tech Stack

- Python
- Flask
- MySQL
- PyMySQL
- Requests
- Riot Games API

## Project Structure

```text
LeagueMatrix/
├── db/                 # Database connection, repository, mappings, and SQL queries
├── populate/           # Scripts for populating the database
├── riot/               # Riot Games API client
├── riot_static/        # Static game data
├── services/           # League of Legends data services
├── website/
│   ├── routes/         # Flask routes and blueprints
│   ├── services/       # Website-specific services
│   └── templates/      # HTML templates
├── flask_app.py        # Flask application entry point
└── README.md
```

## Notes

- LeagueMatrix is an independent project and is not affiliated with or endorsed by Riot Games.
