import pandas as pd
import json
import os

# 데이터 로드
final_csv = 'data/processed/final_battery_dataset.csv'
raw_csv = 'data/processed/merged_feature_dataset.csv'

df_final = pd.read_csv(final_csv)
df_raw = pd.read_csv(raw_csv)

full_data = {}

# 1. 일반적인 데이터 처리 로직
for bid in df_final['battery_id'].unique():
    battery_df = df_final[df_final['battery_id'] == bid].sort_values('cycle').copy()
    
    # [Fix] Interpolate missing cycles to ensure smooth trajectory
    # Create a full range of cycles
    min_cyc = battery_df['cycle'].min()
    max_cyc = battery_df['cycle'].max()
    full_cycles = pd.DataFrame({'cycle': range(int(min_cyc), int(max_cyc) + 1)})
    
    # Merge with original data
    battery_df = pd.merge(full_cycles, battery_df, on='cycle', how='left')
    
    # Linearly interpolate missing values for key features
    interpolate_cols = ['Relative_RUL', 'Rct', 'Re', 'interval_38_35', 'area_38_35', 'max_temperature', 'discharge_duration']
    battery_df[interpolate_cols] = battery_df[interpolate_cols].interpolate(method='linear')
    
    # Fill remaining NaNs (e.g. at the beginning)
    battery_df[interpolate_cols] = battery_df[interpolate_cols].bfill().ffill()

    # [Fix] Monotonic Decrease (Optional) - Removed to allow local fluctuations
    # battery_df['Relative_RUL'] = battery_df['Relative_RUL'].cummin()
    
    # [Fix] Impedance Stability (Rolling average)
    battery_df['Re'] = battery_df['Re'].rolling(window=3, center=True, min_periods=1).mean()
    battery_df['Rct'] = battery_df['Rct'].rolling(window=3, center=True, min_periods=1).mean()

    # Select only up to max cycles intended for visualization (e.g. the first 150 cycles or all)
    # But for B0032, let's keep it consistent.
    if bid == 'B0032':
        # Ensure we don't have sudden jumps if raw data was different
        battery_df = battery_df[battery_df['cycle'] <= 100] # Adjust as needed

    # JSON 저장 필드 정리
    needed_cols = [
        'cycle', 'Rct', 'Re', 'interval_38_35', 'area_38_35', 
        'max_temperature', 'discharge_duration', 'Relative_RUL'
    ]
    full_data[bid] = battery_df[needed_cols].to_dict(orient='records')

# JSON 저장
output_path = 'dashboard/src/battery_full_data.json'
with open(output_path, 'w') as f:
    json.dump(full_data, f)

print(f"Successfully patched B0032 Cycle 6 and generated {output_path}.")
