import streamlit as st
import pandas as pd
import altair as alt
from tools.xg_grapher.data_manager import DataManager
from tools.xg_grapher.processing import calculate_rolling_averages
import os

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(layout="wide")
    st.title("xG Trend Visualizer")

    dm = DataManager()
    
    st.sidebar.header("Select League")

    leagues = dm.get_leagues()
    league_names = {v: k for k, v in leagues.items()}
    
    selected_league_short = st.sidebar.selectbox(
        "Choose a league",
        list(leagues.values())
    )

    if selected_league_short:
        selected_league_full = league_names[selected_league_short]

        with st.spinner(f"Fetching data for {selected_league_short}..."):
            for season in dm.get_seasons():
                dm.fetch_and_store_data(selected_league_full, season)
            
            league_data = dm.get_league_data(selected_league_short)
            teams = dm.get_teams_for_league(selected_league_short)

        if not league_data.empty:
            for team_name in teams:
                st.header(team_name)
                team_data = league_data[(league_data["home_team"] == team_name) | (league_data["away_team"] == team_name)]
                
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

                    # Create a single continuous match number
                    plot_data['global_match_num'] = plot_data.groupby('season').cumcount()
                    season_starts = plot_data.groupby('season')['global_match_num'].min().reset_index()
                    
                    # Chart
                    color_scale = alt.Scale(
                        domain=["Expected Goals For", "Expected Goals Against"],
                        range=["#3498db", "#e74c3c"]
                    )

                    line = alt.Chart(plot_data).mark_line().encode(
                        x=alt.X("global_match_num:Q", title="Match Number"),
                        y=alt.Y("xG:Q", title="Expected Goals (10-game Rolling Avg)"),
                        color=alt.Color("Metric:N", scale=color_scale, title=None, legend=alt.Legend(orient="top")),
                        tooltip=["date", "xG", "season"]
                    )
                    
                    points = alt.Chart(plot_data).mark_point().encode(
                        x=alt.X("global_match_num:Q"),
                        y=alt.Y("xG:Q"),
                        color=alt.Color("Metric:N", scale=color_scale),
                        tooltip=["date", "xG", "season"]
                    )

                    # Vertical lines for season demarcation
                    rule_data = plot_data.groupby('season')['global_match_num'].max().reset_index()
                    rule_data = rule_data[rule_data['season'] != rule_data['season'].max()] # Don't draw line at the very end
                    
                    rules = alt.Chart(rule_data).mark_rule(strokeDash=[4, 4], color='gray').encode(
                        x='global_match_num:Q'
                    )

                    chart = (line + points + rules).properties(
                        width=800,
                        height=400
                    )
                    
                    st.altair_chart(chart, use_container_width=False)
        else:
            st.warning("No data found for the selected league.")

if __name__ == "__main__":
    main()