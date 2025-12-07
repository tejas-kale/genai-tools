import os

import pandas as pd
import soccerdata as sd
from soccerdata import _config
from sqlalchemy import create_engine, inspect, text


class DataManager:
    """
    Manages data acquisition, caching, and persistence for the xG Grapher tool.
    It handles connections to the SQLite database and interfaces with the soccerdata library.
    """

    def __init__(self):
        """
        Initializes the DataManager.
        Sets up the cache directory, initializes the SQLite database connection,
        ensures the necessary table exists, and configures the user agent for scraping.
        """
        # Define the directory where soccerdata will cache its downloads
        cache_dir = os.path.expanduser("~/.cache/soccerdata")
        os.environ["SOCCERDATA_DIR"] = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

        # Initialize SQLite database connection
        self.db_path = os.path.join(cache_dir, "xg_data.db")
        self.engine = create_engine(f"sqlite:///{self.db_path}")

        # Ensure the data table exists on startup
        self._create_table()

        # Set a custom User-Agent to avoid being blocked by data providers
        _config.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

    def _create_table(self):
        """
        Creates the 'match_stats' table in the SQLite database if it doesn't already exist.
        This table stores season, date, league, team names, and expected goals (xG) data.
        """
        with self.engine.connect() as connection:
            # Check for table existence using SQLAlchemy's inspector
            if not inspect(self.engine).has_table("match_stats"):
                # Define schema: date+teams form the composite primary key to avoid duplicates
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
        """
        Returns a list of season strings relevant to the tool.
        Currently covers seasons from 2020-21 to 2025-26.
        Format example: '20-21', '21-22'.
        """
        return [f"{year}-{str(year + 1)[-2:]}" for year in range(2020, 2026)]

    def get_leagues(self):
        """
        Returns a dictionary mapping full league names (used by soccerdata)
        to short codes (used for display and internal logic).
        """
        return {
            "ENG-Premier League": "EPL",
            "ESP-La Liga": "La Liga",
            "ITA-Serie A": "Serie A",
            "GER-Bundesliga": "Bundesliga",
            "FRA-Ligue 1": "Ligue 1",
        }

    def fetch_and_store_data(self, league: str, season: str):
        """
        Fetches match data from the 'Understat' provider via soccerdata for a specific league and season.
        The data is cleaned and stored in the local SQLite database.

        Args:
            league (str): The full league identifier (e.g., 'ENG-Premier League').
            season (str): The season identifier (e.g., '20-21').
        """
        with self.engine.connect() as connection:
            # Check if data for this specific league and season is already present in the DB
            # This prevents redundant API calls/scraping.
            query = text("""
            SELECT COUNT(*) FROM match_stats WHERE league = :league AND season = :season
            """)
            result = connection.execute(
                query, {"league": self.get_leagues()[league], "season": season}
            ).scalar()

            if result == 0:
                # Initialize the scraper for the specific league and season
                understat = sd.Understat(leagues=league, seasons=season)

                # Fetch the schedule which includes match results and xG data
                matchlogs = understat.read_schedule()

                # Filter for completed games that have valid xG data and team names
                matchlogs = matchlogs[
                    matchlogs["home_xg"].notna() & matchlogs["away_xg"].notna()
                ]
                matchlogs = matchlogs[
                    matchlogs["home_team"].notna() & matchlogs["away_team"].notna()
                ]

                if not matchlogs.empty:
                    # Prepare the DataFrame for insertion into SQLite
                    # Map the full league name to our short code
                    df = pd.DataFrame(
                        {
                            "season": season,
                            "date": matchlogs["date"].dt.strftime("%Y-%m-%d"),
                            "league": self.get_leagues()[league],
                            "home_team": matchlogs["home_team"],
                            "away_team": matchlogs["away_team"],
                            "home_xg": matchlogs["home_xg"],
                            "away_xg": matchlogs["away_xg"],
                        }
                    )

                    # Append data to the table; 'if_exists="append"' adds new rows
                    df.to_sql(
                        "match_stats", self.engine, if_exists="append", index=False
                    )

    def get_all_teams(self):
        """
        Fetches a list of all unique team names currently stored in the database across all leagues.

        Returns:
            list: A sorted list of unique team names.
        """
        with self.engine.connect() as connection:
            query = text(
                "SELECT DISTINCT home_team FROM match_stats UNION SELECT DISTINCT away_team FROM match_stats ORDER BY 1"
            )
            teams = connection.execute(query).fetchall()
            return [team[0] for team in teams]

    def get_teams_by_league(self):
        """
        Fetches all unique team names grouped by their league.

        Returns:
            dict: Keys are league codes, values are lists of team names.
        """
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
        Retrieves all historical match data for a specific team from the database.
        Includes matches where the team played either at home or away.

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

    def get_league_data(self, league: str):
        """
        Retrieves all match data for a specific league from the database.

        Args:
            league (str): The short league identifier (e.g., 'EPL').

        Returns:
            pd.DataFrame: A DataFrame containing the league's match data.
        """
        with self.engine.connect() as connection:
            query = text("""
            SELECT * FROM match_stats WHERE league = :league
            """)
            df = pd.read_sql(query, connection, params={"league": league})
            return df

    def get_teams_for_league(self, league: str):
        """
        Retrieves a list of all unique team names that have played in a specific league.

        Args:
            league (str): The short league identifier (e.g., 'EPL').

        Returns:
            list: A sorted list of unique team names.
        """
        with self.engine.connect() as connection:
            query = text("""
            SELECT DISTINCT home_team FROM match_stats WHERE league = :league
            UNION
            SELECT DISTINCT away_team FROM match_stats WHERE league = :league
            ORDER BY 1
            """)
            teams = connection.execute(query, {"league": league}).fetchall()
            return [team[0] for team in teams]
