import pandas as pd
import json

csv_path = 'main_model/final_battery_dataset.csv'
df = pd.read_csv(csv_path)

trajectories = {}
for bid in df['battery_id'].unique():
    sub = df[df['battery_id'] == bid][['cycle', 'Relative_RUL']]
    trajectories[bid] = sub.to_dict(orient='records')

with open('dashboard/src/battery_trajectories.json', 'w') as f:
    json.dump(trajectories, f)

print("Successfully generated battery_trajectories.json")
