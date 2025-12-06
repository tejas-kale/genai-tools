## xG Grapher

This tool provides a Streamlit dashboard to visualize rolling averages of Expected Goals (xG) for various soccer teams across the top 5 European leagues.

### How to Run

1.  **Install dependencies:**
    ```bash
    uv sync
    ```

2.  **Run the Streamlit app:**
    ```bash
    uv tool run xg_grapher
    ```
    Alternatively, you can run it using the direct script entry:
    ```bash
    xg_grapher
    ```
    Or, you can run it using streamlit directly:
    ```bash
    streamlit run tools/xg_grapher/app.py
    ```

The application will open in your web browser.

### Features

*   **Interactive Dashboard:** A Streamlit-based user interface for easy interaction.
*   **Data Caching:** Match data is cached in a local SQLite database to avoid repeated, slow data fetching from the source.
*   **Rolling Averages:** Calculates 10-game rolling averages for "xG For" and "xG Against".
*   **Team Selection:** A hierarchical dropdown menu to select teams by league.
*   **Visualization:** Uses Altair to plot the xG trends, with automatic theme adoption (light/dark mode).
*   **Seasonal Data:** Visualizes data from the 2020-21 season to the present.
