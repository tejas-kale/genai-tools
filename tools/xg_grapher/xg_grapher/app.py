import streamlit as st
import pandas as pd
import altair as alt
from .data_manager import get_data, get_available_teams, LEAGUES, SEASONS
from .processing import calculate_rolling_averages
import os

st.set_page_config(layout="wide")


def format_team_selection(teams_by_league):
    """Format the team selection dropdown."""
    options = []
    for league, teams in teams_by_league.items():
        options.append(f"--- {league} ---")
        for team in teams:
            options.append(f"  {team}")
    return options


def main():
    """Main function to run the Streamlit app."""
    st.title("xG Rolling Averages")

    # Initial data load for the first league and season to get teams
    with st.spinner("Loading initial data..."):
        get_data(list(LEAGUES.keys())[0], SEASONS[0])

    teams_by_league = get_available_teams()

    if not teams_by_league:
        st.warning("No data available. Please run the data fetching process.")
        return

    formatted_teams = format_team_selection(teams_by_league)
    selected_team_formatted = st.selectbox("Select a Team", formatted_teams)

    if selected_team_formatted:
        if selected_team_formatted.startswith("---"):
            st.info("Please select a club.")
            return

        selected_team = selected_team_formatted.strip()
        st.header(f"10-Game Rolling xG Averages for {selected_team}")

        league_id = None
        for l_id, l_name in LEAGUES.items():
            if l_name in teams_by_league and selected_team in teams_by_league[l_name]:
                league_id = l_id
                break

        if league_id:
            with st.spinner(f"Loading data for {selected_team}..."):
                full_data = pd.DataFrame()
                for season in SEASONS:
                    data = get_data(league_id, season)
                    if not data.empty:
                        full_data = pd.concat([full_data, data])

            if not full_data.empty:
                rolling_df = calculate_rolling_averages(full_data, selected_team)

                base_chart = (
                    alt.Chart(rolling_df)
                    .encode(x=alt.X("match_num:Q", title="Match Number"))
                    .properties(width=200, height=300)
                )

                line_for = base_chart.mark_line(color="blue").encode(
                    y=alt.Y("rolling_xg_for:Q", title="xG (10-game Rolling)")
                )
                points_for = base_chart.mark_point(color="blue").encode(
                    y=alt.Y("rolling_xg_for:Q")
                )

                line_against = base_chart.mark_line(color="red").encode(
                    y=alt.Y("rolling_xg_against:Q")
                )
                points_against = base_chart.mark_point(color="red").encode(
                    y=alt.Y("rolling_xg_against:Q")
                )

                chart = (
                    (line_for + points_for + line_against + points_against)
                    .facet(column=alt.Column("season:N", title="Season"))
                    .resolve_scale(x="independent")
                )

                st.altair_chart(chart, use_container_width=True)
            else:
                st.warning(f"No data available for {selected_team}")
        else:
            st.error("Could not determine the league for the selected team.")


if __name__ == "__main__":
    main()