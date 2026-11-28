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

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/StealMast3r/LeagueMatrix.git
cd LeagueMatrix
```

### 2. Install dependencies

Create and activate a virtual environment, then install the required packages:

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install Flask PyMySQL python-dotenv requests
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
RIOT_API_KEY=your_riot_api_key

DB_HOST=localhost
DB_PORT=3306
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=leaguematrix
```

Use your own Riot API key and MySQL credentials. Do not commit your `.env` file.

### 4. Set up the database

Create the MySQL database, then execute the schema in:

```text
db/schema.sql
```

### 5. Run the application

Start the Flask application from the project root:

```bash
python flask_app.py
```

The development server will be available at:

```text
http://127.0.0.1:5000
```

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

- A valid Riot Games API key is required for Riot API requests.
- Riot API rate limits apply.
- Keep API keys and database credentials out of source control.
- LeagueMatrix is an independent project and is not affiliated with or endorsed by Riot Games.
