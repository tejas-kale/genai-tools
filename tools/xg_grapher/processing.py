import numpy as np
import pandas as pd


def calculate_rolling_averages(df: pd.DataFrame, team_name: str, window_size: int = 10):
    """
    Calculates rolling averages for Expected Goals (xG) For and Against for a specific team.

    This function processes raw match data to create a rolling average trend line,
    which helps in visualizing team performance over time by smoothing out single-match variance.

    Args:
        df (pd.DataFrame): DataFrame containing raw match data. Must include columns:
                           'date', 'home_team', 'away_team', 'home_xg', 'away_xg', 'season'.
        team_name (str): The name of the team to calculate averages for.
                         Used to distinguish between home and away stats.
        window_size (int, optional): The size of the rolling window (number of matches).
                                     Defaults to 10.

    Returns:
        pd.DataFrame: A DataFrame enhanced with rolling average columns ('xg_for_roll', 'xg_against_roll')
                      and a match counter ('match_num') reset per season.
    """
    # Return immediately if the input DataFrame is empty to avoid errors
    if df.empty:
        return pd.DataFrame()

    # Ensure the 'date' column is in datetime format for correct sorting
    df["date"] = pd.to_datetime(df["date"])

    # Sort values by date to ensure the rolling calculation follows chronological order
    df = df.sort_values(by="date")

    # Calculate 'xG For' and 'xG Against' based on whether the target team is playing Home or Away
    # If the team is Home, xG For is home_xg, xG Against is away_xg
    # If the team is Away, xG For is away_xg, xG Against is home_xg
    df["xg_for"] = np.where(df["home_team"] == team_name, df["home_xg"], df["away_xg"])
    df["xg_against"] = np.where(
        df["home_team"] == team_name, df["away_xg"], df["home_xg"]
    )

    # Calculate rolling averages grouped by 'season'
    # We group by season so that the rolling average does not bleed from one season into the next.
    # 'min_periods=1' ensures we get values even for the first few games of the season (expanding window initially).
    df["xg_for_roll"] = df.groupby("season")["xg_for"].transform(
        lambda x: x.rolling(window_size, min_periods=1).mean()
    )
    df["xg_against_roll"] = df.groupby("season")["xg_against"].transform(
        lambda x: x.rolling(window_size, min_periods=1).mean()
    )

    # Create a 'match_num' column that counts games sequentially within each season
    # This provides a clean x-axis 1, 2, 3... N for plotting, independent of dates
    df["match_num"] = df.groupby("season").cumcount() + 1

    return df
