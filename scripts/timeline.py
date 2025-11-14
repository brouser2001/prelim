import matplotlib.pyplot as plt, json
import pandas as pd
import textwrap

color_dict = {
    'Aircraft': 'red',
    'Human Factors': 'blue'
}

def timelineplot(df):
    df["year_dt"] = pd.to_datetime(df["year"].astype(str))

    fig, ax = plt.subplots(figsize=[8, 10], constrained_layout=True)  # Wider and taller

    min_year = df["year_dt"].min().year - 3
    max_year = df["year_dt"].max().year + 2
    min_dt = pd.to_datetime(f"{min_year}-01-01")
    max_dt = pd.to_datetime(f"{max_year}-01-01")

    ax.plot([0, 0], [min_dt, max_dt], "-", color="black", linewidth=1.2)
    ax.plot([0]*len(df), df["year_dt"], "o", color="black", markerfacecolor="white", markersize=6)

    years = pd.date_range(min_dt, max_dt, freq="10YS")
    ax.set_yticks(years)
    ax.set_yticklabels([y.year for y in years])

    ax.set_xlim(-10, 10)  # More space for annotations

    for idx, row in df.iterrows():
        x_offset = row["Level"]
        align = "left" if x_offset > 0 else "right"
        arrow_start_x = 0.5 if x_offset > 0 else -0.5

        wrapped_text = textwrap.fill(row["name"], width=30)  # Adjust width as needed

        ax.annotate(
            wrapped_text,
            xy=(arrow_start_x, row["year_dt"]),
            xytext=(x_offset, row["year_dt"]),
            arrowprops=dict(arrowstyle="-", color=color_dict[row['type']], linewidth=0.8),
            va="center",
            ha=align,
            fontsize=15,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.8)
        )


    for spine in ["left", "top", "right", "bottom"]:
        ax.spines[spine].set_visible(False)

    ax.spines["left"].set_position(("axes", 0.5))
    ax.xaxis.set_visible(False)
    ax.invert_yaxis()

    plt.savefig('media/timeline.png', dpi=300)

# Load data and plot
with open('data/timeline.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data['data'])
timelineplot(df)