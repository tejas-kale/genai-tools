import os
import pandas as pd
import soccerdata as sd
from sqlalchemy import create_engine, inspect, text

class DataManager:
    """Manages data acquisition and persistence for the xG Grapher tool."""

    def __init__(self, db_path="xg_data.db"):
        """
        Initializes the DataManager.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        self._create_table()

    def _create_table(self):
        """Creates the match_stats table if it doesn't exist."""
        with self.engine.connect() as connection:
            if not inspect(self.engine).has_table("match_stats"):
                create_table_query = text("""
                CREATE TABLE match_stats (
                    season TEXT,
                    date TEXT,
                    league TEXT,
                    home_team TEXT,
                    away_team TEXT,
                    home_xg REAL,
                    away_xg REAL,
                    PRIMARY KEY (date, home_team, away_team)
                );
                """)
                connection.execute(create_table_query)

    def get_seasons(self):
        """Returns a list of seasons from 2020-21 to 2024-25."""
        return [f"{year}-{str(year+1)[-2:]}" for year in range(2020, 2025)]

    def get_leagues(self):
        """Returns a dictionary of top 5 leagues."""
        return {
            "ENG-Premier League": "EPL",
            "ESP-La Liga": "La Liga",
            "ITA-Serie A": "Serie A",
            "GER-Bundesliga": "Bundesliga",
            "FRA-Ligue 1": "Ligue 1",
        }

    def fetch_and_store_data(self, league: str, season: str):
        """
        Fetches data from soccerdata and stores it in the database.

        Args:
            league (str): The league identifier (e.g., 'ENG-Premier League').
            season (str): The season identifier (e.g., '20-21').
        """
        with self.engine.connect() as connection:
            # Check if data exists
            query = text("""
            SELECT COUNT(*) FROM match_stats WHERE league = :league AND season = :season
            """)
            result = connection.execute(query, {"league": self.get_leagues()[league], "season": season}).scalar()

            if result == 0:
                fbref = sd.FBref(leagues=league, seasons=season)
                matchlogs = fbref.read_schedule()
                
                # Filter for games with xG data and valid team names
                matchlogs = matchlogs[matchlogs["home_xg"].notna() & matchlogs["away_xg"].notna()]
                matchlogs = matchlogs[matchlogs["home_team"].notna() & matchlogs["away_team"].notna()]


                if not matchlogs.empty:
                    df = pd.DataFrame({
                        "season": season,
                        "date": matchlogs["datetime"].dt.strftime('%Y-%m-%d'),
                        "league": self.get_leagues()[league],
                        "home_team": matchlogs["home_team"],
                        "away_team": matchlogs["away_team"],
                        "home_xg": matchlogs["home_xg"],
                        "away_xg": matchlogs["away_xg"],
                    })
                    df.to_sql("match_stats", self.engine, if_exists="append", index=False)

    def get_all_teams(self):
        """Fetches all unique team names from the database."""
        with self.engine.connect() as connection:
            query = text("SELECT DISTINCT home_team FROM match_stats UNION SELECT DISTINCT away_team FROM match_stats ORDER BY 1")
            teams = connection.execute(query).fetchall()
            return [team[0] for team in teams]
    
    def get_teams_by_league(self):
        """Fetches all unique team names from the database, grouped by league."""
        with self.engine.connect() as connection:
            query = text("""
            SELECT league, team FROM (
                SELECT league, home_team as team FROM match_stats
                UNION
                SELECT league, away_team as team FROM match_stats
            )
            GROUP BY league, team
            ORDER BY league, team
            """)
            result = connection.execute(query).fetchall()
            
            teams_by_league = {}
            for league, team in result:
                if league not in teams_by_league:
                    teams_by_league[league] = []
                teams_by_league[league].append(team)
            
            return teams_by_league

    def get_team_data(self, team_name: str):
        """
        Retrieves all match data for a specific team.

        Args:
            team_name (str): The name of the team.

        Returns:
            pd.DataFrame: A DataFrame containing the team's match data.
        """
        with self.engine.connect() as connection:
            query = text("""
            SELECT * FROM match_stats WHERE home_team = :team_name OR away_team = :team_name
            """)
            df = pd.read_sql(query, connection, params={"team_name": team_name})
            return df