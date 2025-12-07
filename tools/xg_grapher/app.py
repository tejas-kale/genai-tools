import streamlit as st

from tools.xg_grapher.data_manager import DataManager
from tools.xg_grapher.plotting import plot_xg_trends
from tools.xg_grapher.processing import calculate_rolling_averages


def main():
    """
    Main function to run the Streamlit app.
    It handles the UI layout, user input, data fetching, and visualization display.
    """
    # Configure the Streamlit page layout to wide mode for better visualization space
    st.set_page_config(layout="wide")

    # Set the main title of the application
    st.title("xG Trend Visualizer")

    # Initialize the DataManager to handle database interactions and data fetching
    dm = DataManager()

    # -- Sidebar Configuration --
    # Header for the sidebar
    st.sidebar.header("Select League")

    # Retrieve available leagues from the DataManager
    leagues = dm.get_leagues()
    # Create a reverse mapping to find full league names from short codes if needed
    league_names = {v: k for k, v in leagues.items()}

    # Dropdown for league selection.
    # The user requested to remove "Choose a league" label, so we set the label to an empty string
    # or use label_visibility to hide it if we wanted to keep the semantic label.
    # Here we just make the label empty/generic as requested relative to the header.
    selected_league_short = st.sidebar.selectbox(
        label="",  # Empty label as per user request to remove "Choose a league" text
        options=list(leagues.values()),
    )

    # -- Main Content Logic --
    if selected_league_short:
        # Get the full league name key required for the fetch function
        selected_league_full = league_names[selected_league_short]

        # Fetch data for all available seasons for the selected league
        # We use a spinner to indicate background work
        with st.spinner(f"Fetching data for {selected_league_short}..."):
            for season in dm.get_seasons():
                # Fetch data from source (if not cached) and store in DB
                dm.fetch_and_store_data(selected_league_full, season)

            # Retrieve the consolidated data for the league from the local DB
            league_data = dm.get_league_data(selected_league_short)
            # Get the list of teams in this league for iteration
            teams = dm.get_teams_for_league(selected_league_short)

        # Check if we actually have data to display
        if not league_data.empty:
            # Iterate through each team to generate their specific chart
            for team_name in teams:
                st.header(team_name)

                # Filter data for the current team (matches where they are home OR away)
                # We create a copy to avoid SettingWithCopy warnings on subsequent modifications
                team_data = league_data[
                    (league_data["home_team"] == team_name)
                    | (league_data["away_team"] == team_name)
                ].copy()

                if not team_data.empty:
                    # Calculate the 10-game rolling averages for xG For and Against
                    rolling_data = calculate_rolling_averages(team_data, team_name)

                    # Prepare data for plotting:
                    # Melt the dataframe to have a 'long' format suitable for Seaborn/Altair
                    # This combines 'xg_for_roll' and 'xg_against_roll' into a single 'xG' column
                    # distinguished by a 'Metric' column.
                    plot_data = rolling_data.melt(
                        id_vars=["season", "match_num", "date"],
                        value_vars=["xg_for_roll", "xg_against_roll"],
                        var_name="Metric",
                        value_name="xG",
                    )

                    # Rename metric values for cleaner legend labels in the plot
                    plot_data["Metric"] = plot_data["Metric"].map(
                        {"xg_for_roll": "xG For", "xg_against_roll": "xG Against"}
                    )

                    # Generate the static plot using Seaborn via the helper module
                    fig = plot_xg_trends(plot_data, team_name)

                    # Display the matplotlib figure in Streamlit
                    st.pyplot(fig)

                # Add a line break between each club for visual separation
                st.markdown("---")
        else:
            # Fallback message if no data is returned
            st.warning("No data found for the selected league.")


if __name__ == "__main__":
    main()
