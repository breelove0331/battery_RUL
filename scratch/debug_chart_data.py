import json
with open('dashboard/src/battery_full_data.json') as f:
    data = json.load(f)
b5 = data['B0005']
print(f"B0005 Last 3: {b5[-3:]}")
print(f"Max Relative_RUL: {max(r['Relative_RUL'] for r in b5)}")
print(f"Min Relative_RUL: {min(r['Relative_RUL'] for r in b5)}")
