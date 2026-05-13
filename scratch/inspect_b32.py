import pandas as pd

df = pd.read_csv('main_model/merged_feature_dataset.csv')
b32 = df[df['battery_id'] == 'B0032'].sort_values('cycle')
print("B0032 Data (Cycle 4-8):")
print(b32[b32['cycle'].between(4, 8)][['cycle', 'Capacity', 'Rct', 'Re', 'interval_38_35']])
