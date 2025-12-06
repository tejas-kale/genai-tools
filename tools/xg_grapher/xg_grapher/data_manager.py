import pandas as pd
import soccerdata as sd
from sqlalchemy import create_engine, inspect
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "xg_data.db")
DB_URI = f"sqlite:///{DB_PATH}"
ENGINE = create_engine(DB_URI)

LEAGUES = {
    "ENG-Premier League": "ENG-Premier League",
    "ESP-La Liga": "ESP-La Liga",
    "ITA-Serie A": "ITA-Serie A",
    "GER-Bundesliga": "GER-Bundesliga",
    "FRA-Ligue 1": "FRA-Ligue 1",
}

SEASONS = ["20-21", "21-22", "22-23", "23-24", "24-25"]


def setup_database():
    """Create the database and table if they don't exist."""
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with ENGINE.connect() as connection:
        if not inspect(ENGINE).has_table("match_stats"):
            pd.DataFrame(
                columns=[
                    "season",
                    "date",
                    "league",
                    "home_team",
                    "away_team",
                    "home_xg",
                    "away_xg",
                ]
            ).to_sql(
                "match_stats",
                connection,
                if_exists="fail",
                index=False,
                dtype={
                    "season": "TEXT",
                    "date": "DATETIME",
                    "league": "TEXT",
                    "home_team": "TEXT",
                    "away_team": "TEXT",
                    "home_xg": "FLOAT",
                    "away_xg": "FLOAT",
                },
            )
            # Add a unique constraint to prevent duplicate matches
            connection.execute(
                "CREATE UNIQUE INDEX ix_match_stats_unique "
                "ON match_stats (date, home_team, away_team)"
            )


def get_data(league: str, season: str) -> pd.DataFrame:
    """Fetch data from the database or soccerdata."""
    setup_database()
    try:
        with ENGINE.connect() as connection:
            # Check if data for the league and season exists
            query = f"SELECT * FROM match_stats WHERE league = '{league}' AND season = '{season}'"
            if pd.read_sql(query, connection).empty:
                fbref = sd.FBref(leagues=league, seasons=season)
                stats = fbref.read_schedule()
                stats = stats[["season", "date", "league", "home_team", "away_team", "home_xg", "away_xg"]]
                stats.to_sql(
                    "match_stats", connection, if_exists="append", index=False
                )
            return pd.read_sql(f"SELECT * FROM match_stats WHERE league = '{league}'", connection)
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()


def get_available_teams() -> dict:
    """Get a dictionary of leagues and their teams from the database."""
    setup_database()
    teams = {}
    with ENGINE.connect() as connection:
        for league_id, league_name in LEAGUES.items():
            query = f"SELECT DISTINCT home_team FROM match_stats WHERE league = '{league_id}'"
            df = pd.read_sql(query, connection)
            if not df.empty:
                teams[league_name] = sorted(df["home_team"].unique().tolist())
    return teams
