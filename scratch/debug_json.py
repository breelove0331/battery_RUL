import json
with open('dashboard/src/battery_full_data.json') as f:
    data = json.load(f)
for bid, records in list(data.items())[:2]:
    print(f"Battery: {bid}")
    print(f"First 3 cycles: {[r['cycle'] for r in records[:3]]}")
    print(f"First record: {records[0]}")
