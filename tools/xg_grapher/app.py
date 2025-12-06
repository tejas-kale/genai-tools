import streamlit as st
import pandas as pd
import altair as alt
from .data_manager import DataManager
from .processing import calculate_rolling_averages
import os

def get_team_selections(dm):
    """Creates a formatted list for the team selection dropdown."""
    # Pre-fetch data for all leagues and seasons to populate the dropdown
    for league in dm.get_leagues():
        for season in dm.get_seasons():
            dm.fetch_and_store_data(league, season)
    
    teams_by_league = dm.get_teams_by_league()
    
    options = []
    league_map = {v: k for k, v in dm.get_leagues().items()}
    
    for league_short, teams in sorted(teams_by_league.items()):
        league_full = league_map.get(league_short, league_short).split('-')[1]
        options.append(f"--- {league_full} ---")
        for team in teams:
            options.append(f"  {team}")
    return options

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(layout="wide")
    st.title("xG Trend Visualizer")

    dm = DataManager()
    
    st.sidebar.header("Select Team")

    # Populate dropdown
    with st.spinner("Fetching available teams..."):
        team_options = get_team_selections(dm)

    selected_option = st.sidebar.selectbox(
        "Choose a team",
        team_options
    )

    if selected_option and not selected_option.startswith("---"):
        team_name = selected_option.strip()
        st.header(f"xG Trends for {team_name}")

        with st.spinner(f"Fetching and processing data for {team_name}..."):
            team_data = dm.get_team_data(team_name)
            if not team_data.empty:
                rolling_data = calculate_rolling_averages(team_data, team_name)

                # Melt data for Altair
                plot_data = rolling_data.melt(
                    id_vars=["season", "match_num", "date"],
                    value_vars=["xg_for_roll", "xg_against_roll"],
                    var_name="Metric",
                    value_name="xG"
                )
                plot_data["Metric"] = plot_data["Metric"].map({
                    "xg_for_roll": "Expected Goals For",
                    "xg_against_roll": "Expected Goals Against"
                })

                # Chart
                color_scale = alt.Scale(
                    domain=["Expected Goals For", "Expected Goals Against"],
                    range=["#3498db", "#e74c3c"]
                )

                line = alt.Chart(plot_data).mark_line().encode(
                    x=alt.X("match_num:Q", title="Match Number"),
                    y=alt.Y("xG:Q", title="Expected Goals (10-game Rolling Avg)"),
                    color=alt.Color("Metric:N", scale=color_scale, title=None, legend=alt.Legend(orient="top")),
                    tooltip=["date", "xG"]
                )
                
                points = alt.Chart(plot_data).mark_point().encode(
                    x=alt.X("match_num:Q", title="Match Number"),
                    y=alt.Y("xG:Q", title="Expected Goals (10-game Rolling Avg)"),
                    color=alt.Color("Metric:N", scale=color_scale),
                     tooltip=["date", "xG"]
                )

                chart = (line + points).properties(
                    height=400
                ).facet(
                    column=alt.Column("season:N", title=None, header=alt.Header(labelOrient="bottom"))
                ).configure_view(
                    stroke=None # Removes the border around each facet
                )
                
                st.altair_chart(chart, use_container_width=True, theme="streamlit")

            else:
                st.warning(f"No data found for {team_name}.")
    elif selected_option:
        st.info("Please select a club from the dropdown to see the visualization.")

if __name__ == "__main__":
    main()
