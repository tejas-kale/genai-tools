## xG Grapher

This tool provides a Streamlit dashboard to visualize rolling averages of Expected Goals (xG) for various soccer teams across the top 5 European leagues.

### How to Run

This tool is a local script within the `genai-tools` project. You need to run it within the project's virtual environment managed by `uv`.

1.  **Sync Environment:** First, ensure your dependencies are synced and the tool is installed in editable mode. From the root of the `genai-tools` project, run:
    ```bash
    uv sync
    ```

2.  **Run the App:** Use the `uv run` command to execute the script within the project's environment. `uv tool run` is used for packages installed from a registry (like PyPI), not for local scripts.
    ```bash
    uv run xg_grapher
    ```
    This command executes the `xg_grapher` script defined in the project's `pyproject.toml` file.

    Alternatively, you can run the Streamlit app directly, also using `uv run`:
    ```bash
    uv run streamlit run tools/xg_grapher/app.py
    ```

The application will open in your web browser.

### Features

*   **Interactive Dashboard:** A Streamlit-based user interface for easy interaction.
*   **Data Caching:** Match data is cached in a local SQLite database to avoid repeated, slow data fetching from the source.
*   **Rolling Averages:** Calculates 10-game rolling averages for "xG For" and "xG Against".
*   **Team Selection:** A hierarchical dropdown menu to select teams by league.
*   **Visualization:** Uses Altair to plot the xG trends, with automatic theme adoption (light/dark mode).
*   **Seasonal Data:** Visualizes data from the 2020-21 season to the present.
