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


# Export to JSON for frontend
team_metrics = {
    'rebound_percentage': float(rebound_pct),
    'total_good_attempts': int(total_good_execution),
    'total_attempts': int(total_attempts),
    'top_performer': str(top_performer)
}

with open('team_metrics.json', 'w') as f:
    json.dump(team_metrics, f, indent=2)

print("\n✅ Data exported to team_metrics.json")
