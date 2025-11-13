import matplotlib.pyplot as plt, json
import pandas as pd

color_dict={'Aircraft':'red',
            'Human Factors':'blue'}

def timelineplot(df):

    # Convert year to datetime for consistent y-axis handling
    df["year_dt"] = pd.to_datetime(df["year"].astype(str))

    fig, ax = plt.subplots(figsize=[6,9])

    # ---- EXTEND RANGE ----
    min_year = df["year_dt"].min().year - 3
    max_year = df["year_dt"].max().year + 2
    min_dt = pd.to_datetime(f"{min_year}-01-01")
    max_dt = pd.to_datetime(f"{max_year}-01-01")

    # ---- DRAW FULL BASELINE ----
    # Draw continuous vertical line from min_dt to max_dt
    ax.plot([0, 0], [min_dt, max_dt], "-", color="black", linewidth=1.2)

    # Markers for events
    ax.plot([0]*len(df), df["year_dt"], "o", color="black", markerfacecolor="white", markersize=6)
    # ------------------------------

    # Decrease spacing between year ticks (use 2-year steps)
    years = pd.date_range(min_dt, max_dt, freq="10YS")
    ax.set_yticks(years)
    ax.set_yticklabels([y.year for y in years])

    # Set limits for x-axis
    ax.set_xlim(-7, 7)

    # Annotate each event
    for idx, row in df.iterrows():
        x_offset = row["Level"]
        align = "left" if x_offset > 0 else "right"
        arrow_start_x = 0.5 if x_offset > 0 else -0.5

        ax.annotate(
            row["name"],
            xy=(arrow_start_x, row["year_dt"]),
            xytext=(x_offset, row["year_dt"]),
            arrowprops=dict(arrowstyle="-", color=color_dict[row['type']], linewidth=0.8),
            va="center",
            ha=align,
            fontsize=10,
        )

    # Style cleanup
    for spine in ["left", "top", "right", "bottom"]:
        ax.spines[spine].set_visible(False)

    ax.spines["left"].set_position(("axes", 0.5))
    ax.xaxis.set_visible(False)

    # Oldest date at the top
    ax.invert_yaxis()

    ax.set_title("Aviation History", pad=10, loc="center", fontsize=20)

    plt.tight_layout()
    #plt.show()
    plt.savefig('media/timeline.png',dpi=300)

with open('data/timeline.json', 'r') as f:
    data = json.load(f)

# Load into a DataFrame
df = pd.DataFrame(data['data'])

timelineplot(df)
