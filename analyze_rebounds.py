import json
import pandas as pd
from template import read_sheet, write_sheet

# ============================================
# READ DATA
# ============================================
df, spreadsheet = read_sheet('WBB', 'Sheet1')

print("📊 Starting analysis...\n")

# Convert numeric columns from text to numbers (empty becomes 0)
df["Attempts"] = pd.to_numeric(
    df["Attempts"], errors='coerce').fillna(0).astype(int)
df["Good Execution"] = pd.to_numeric(
    df["Good Execution"], errors='coerce').fillna(0).astype(int)

# Filter out rows with 0 attempts (players who didn't play)
df = df[df["Attempts"] > 0]

# Filter to offensive
df["Type"] = df["Type"].astype(str).str.strip()

base_df = df.copy()
df = base_df[base_df["Type"] == "Offensive"].copy()

# ============================================
# PANDAS CALCULATIONS GO HERE!
# ============================================

# Team Rebound
total_attempts = df["Attempts"].sum()
total_good_execution = df["Good Execution"].sum()
rebound_pct = (total_good_execution/total_attempts*100).round(1)
print(f"Rebound Percentage: {rebound_pct}%")
print(f"Total Good Attempts: {total_good_execution}/{total_attempts}")

# Top Performer
df['player_pct'] = (df['Good Execution'] / df['Attempts'] * 100).round(1)
top_performer = df.loc[df['player_pct'].idxmax(), "Player"]
print(f"Top Performer: {top_performer}")

# Husky leaders
top_3 = (
    df[df["Attempts"] >= 15]
    .sort_values(["player_pct", "Attempts"], ascending=[False, False])
    .head(3)[["Player", "player_pct", "Attempts"]]
)
print("\nHusky Leaders")
print(top_3)

# Deevelopment needed
bottom_3 = (
    df[df["Attempts"] >= 15]
    .sort_values(["player_pct", "Attempts"], ascending=[True, False])
    .head(3)[["Player", "player_pct", "Attempts"]]
)

print("\nDevelopment Needed")
print(bottom_3)

# ============================================
# FULL OFFENSIVE ROSTER EXPORT
# ============================================

roster_df = df[[
    "Player",
    "Attempts",
    "Good Execution",
    "Stand Around",
    "On the Back",
    "Get Back",
    "player_pct"
]].copy()

# Replace NaN with 0 for cleaner JSON
roster_df = roster_df.fillna(0)

full_roster = roster_df.rename(
    columns={
        "Attempts": "attempts",
        "Good Execution": "good_execution",
        "Stand Around": "stand_around",
        "On the Back": "on_the_back",
        "Get Back": "get_back",
        "player_pct": "final_pct"
    }
).to_dict(orient="records")


# Export to JSON for frontend
team_metrics = {
    'rebound_percentage': float(rebound_pct),
    'total_good_attempts': int(total_good_execution),
    'total_attempts': int(total_attempts),
    'top_performer': str(top_performer),

    # Top 3
    'husky_leaders': (
        top_3.rename(columns={"player_pct": "success_pct"})
        .to_dict(orient="records")
    ),

    # Bottom 3
    'development_needed': (
        bottom_3.rename(columns={"player_pct": "success_pct"})
        .to_dict(orient="records")
    ),

    # Full roster
    'full_roster': full_roster
}


with open('team_metrics.json', 'w') as f:
    json.dump(team_metrics, f, indent=2)

print("\n✅ Data exported to team_metrics.json")
