import pandas as pd
import matplotlib.pyplot as plt
import os

csv_path = r'c:\Users\View\cleaned_dataset\data_analysis\main_model\final_battery_dataset.csv'
target_dir = r'c:\Users\View\cleaned_dataset\data_analysis\dashboard\public\trajectories'

df = pd.read_csv(csv_path)
os.makedirs(target_dir, exist_ok=True)

plt.style.use('dark_background')

for bid in df['battery_id'].unique():
    sub = df[df['battery_id'] == bid]
    plt.figure(figsize=(10, 6))
    plt.plot(sub['cycle'], sub['Relative_RUL'], color='#38bdf8', linewidth=2)
    plt.title(f'[{bid}] Relative RUL Trajectory', fontsize=14, pad=20)
    plt.xlabel('Cycle', fontsize=12)
    plt.ylabel('Relative RUL (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(target_dir, f'{bid}.png'), dpi=100)
    plt.close()
    print(f"Generated {bid}.png")
