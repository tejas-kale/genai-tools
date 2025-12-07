import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_xg_trends(plot_data: pd.DataFrame, team_name: str):
    """
    Plots rolling xG trends using Seaborn with an Economist-like style.

    Args:
        plot_data (pd.DataFrame): DataFrame containing 'match_num', 'xG', 'Metric', and 'season'.
        team_name (str): Name of the team being analyzed.

    Returns:
        matplotlib.figure.Figure: The generated figure object.
    """
    # Set the style to mimic The Economist
    # Use a white grid style as a base
    sns.set_theme(style="whitegrid")

    # Customizing rcParams for Economist-like look
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
    plt.rcParams["axes.edgecolor"] = "#d9d9d9"  # Light gray spines
    plt.rcParams["axes.linewidth"] = 0
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.color"] = "#d9d9d9"
    plt.rcParams["grid.linestyle"] = "-"
    plt.rcParams["grid.linewidth"] = 1.0
    plt.rcParams["axes.axisbelow"] = True  # Grid behind plot elements
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"
    plt.rcParams["text.color"] = "#333333"
    plt.rcParams["axes.labelcolor"] = "#333333"
    plt.rcParams["xtick.color"] = "#333333"
    plt.rcParams["ytick.color"] = "#333333"
    plt.rcParams["font.weight"] = "bold"

    # Economist colors (approximate)
    # Blue-ish for For, Red-ish for Against
    palette = {"Expected Goals For": "#0072B2", "Expected Goals Against": "#D55E00"}

    # Create the plot
    # Using FacetGrid to handle seasons as columns, similar to the Altair chart
    g = sns.FacetGrid(
        plot_data,
        col="season",
        col_wrap=3,  # Wrap columns if too many, though seasons usually fit in one row or wrap nicely
        sharex=False,  # Match numbers reset per season, so don't strictly share x-axis range if lengths differ
        sharey=True,  # Share Y for comparison
        height=4,
        aspect=1.5,
    )

    # Map the line plot
    g.map_dataframe(
        sns.lineplot,
        x="match_num",
        y="xG",
        hue="Metric",
        palette=palette,
        linewidth=2.5,
    )

    # Map the scatter plot (points) for detail
    g.map_dataframe(
        sns.scatterplot,
        x="match_num",
        y="xG",
        hue="Metric",
        palette=palette,
        s=30,
        alpha=0.8,
    )

    # Add a red horizontal line at y=0 (though xG is always >= 0) if needed, or reference lines.
    # Economist graphs often have a strong horizontal baseline.

    # Customize titles and labels
    g.set_titles("{col_name}", fontweight="bold", fontsize=14)
    g.set_axis_labels(
        "Match Number", "Expected Goals (10-game Rolling Avg)", fontsize=12
    )

    # Adjust legend
    g.add_legend(title="", fontsize=12, adjust_subtitles=True)

    # Set overall title
    g.figure.suptitle(
        f"{team_name}: Expected Goals Trends (10-Game Rolling Average)",
        fontsize=16,
        fontweight="bold",
        y=1.05,
    )

    # Tight layout to prevent clipping
    plt.tight_layout()

    return g.figure
