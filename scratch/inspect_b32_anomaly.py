import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/final_battery_dataset.csv")
b32 = df[df['battery_id'] == 'B0032']

print("Battery B0032 Data (Top 15 cycles):")
cols = ['battery_id', 'cycle', 'Capacity', 'RUL', 'Relative_RUL', 'Re', 'Rct']
print(b32[cols].head(15))

# Check for specific anomaly at cycle 6
c6 = b32[b32['cycle'] == 6]
print("\nCycle 6 details:")
print(c6)

# Check if eol_cycle was consistent
# eol_cycle is RUL + cycle if RUL > 0
b32_copy = b32.copy()
b32_copy['derived_eol'] = b32_copy['RUL'] + b32_copy['cycle']
print("\nDerived EOL Cycles:")
print(b32_copy[['cycle', 'derived_eol']].head(15))
