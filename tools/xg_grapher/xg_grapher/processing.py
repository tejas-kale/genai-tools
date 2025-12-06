import pandas as pd

def calculate_rolling_averages(df: pd.DataFrame, team: str, window: int = 10) -> pd.DataFrame:
    """Calculate rolling averages for xG for and against."""
    team_df = df[(df["home_team"] == team) | (df["away_team"] == team)].copy()
    team_df["date"] = pd.to_datetime(team_df["date"])
    team_df = team_df.sort_values(by="date")

    team_df["xg_for"] = team_df.apply(
        lambda row: row["home_xg"] if row["home_team"] == team else row["away_xg"],
        axis=1,
    )
    team_df["xg_against"] = team_df.apply(
        lambda row: row["away_xg"] if row["home_team"] == team else row["home_xg"],
        axis=1,
    )

    team_df["rolling_xg_for"] = (
        team_df.groupby("season")["xg_for"]
        .rolling(window, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )
    team_df["rolling_xg_against"] = (
        team_df.groupby("season")["xg_against"]
        .rolling(window, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )
    
    team_df["match_num"] = team_df.groupby("season").cumcount() + 1

    return team_df
