import pandas as pd

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
    df["xg_for"] = df.apply(lambda row: row["home_xg"] if row["home_team"] == team_name else row["away_xg"], axis=1)
    df["xg_against"] = df.apply(lambda row: row["away_xg"] if row["home_team"] == team_name else row["home_xg"], axis=1)
    
    # Calculate rolling averages, grouped by season
    df["xg_for_roll"] = df.groupby("season")["xg_for"].transform(lambda x: x.rolling(window_size, min_periods=1).mean())
    df["xg_against_roll"] = df.groupby("season")["xg_against"].transform(lambda x: x.rolling(window_size, min_periods=1).mean())

    df["match_num"] = df.groupby("season").cumcount() + 1

    return df