import pandas as pd
import numpy as np

def calculate_rolling_averages(df: pd.DataFrame, team_name: str, window_size: int = 10):
    """
    Calculates rolling averages for xG for and xG against.

    Args:
        df (pd.DataFrame): DataFrame containing match data for a team.
        team_name (str): The name of the team.
        window_size (int): The size of the rolling window.

    Returns:
        pd.DataFrame: A DataFrame with rolling averages.
    """
    if df.empty:
        return pd.DataFrame()

    # Create a single timeline for the team
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date")

    # Calculate xG For and xG Against
    df["xg_for"] = np.where(df["home_team"] == team_name, df["home_xg"], df["away_xg"])
    df["xg_against"] = np.where(df["home_team"] == team_name, df["away_xg"], df["home_xg"])
    
    # Calculate rolling averages, grouped by season
    df["xg_for_roll"] = df.groupby("season")["xg_for"].transform(lambda x: x.rolling(window_size, min_periods=1).mean())
    df["xg_against_roll"] = df.groupby("season")["xg_against"].transform(lambda x: x.rolling(window_size, min_periods=1).mean())

    df["match_num"] = df.groupby("season").cumcount() + 1

    return df