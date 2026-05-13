import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
import os
import json
from sklearn.preprocessing import StandardScaler

# 1. 데이터 로드
csv_path = r'c:\Users\View\cleaned_dataset\data_analysis\main_model\final_battery_dataset.csv'
df = pd.read_csv(csv_path)

feature_cols = [
    'early_voltage_mean', 'middle_voltage_mean', 'late_voltage_mean',
    'max_temperature', 'temperature_rise', 'mean_current',
    'discharge_duration', 'voltage_slope', 'mean_internal_resistance',
    'interval_40_38', 'interval_38_35', 'interval_35_32',
    'area_40_38', 'area_38_35', 'area_35_32',
    'dvdt_35', 'dv_dt_std', 'Re', 'Rct',
    'cutoff_voltage', 'ambient_temperature', 'inv_temperature',
    'delta_middle_voltage', 'delta_discharge_duration',
    'delta_Rct', 'delta_Re', 'delta_interval_38_35', 'delta_area_38_35'
]

# 2. 모델 학습 (전체 데이터 기반)
X = df[feature_cols]
y = df['Relative_RUL']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols)

model = xgb.XGBRegressor(
    n_estimators=700, learning_rate=0.02, max_depth=4,
    subsample=0.8, colsample_bytree=0.8, random_state=42
)
model.fit(X_scaled, y)

# 3. SHAP Explainer 생성
explainer = shap.TreeExplainer(model)
shap_values_all = explainer.shap_values(X_scaled_df)

# 4. 배터리별 분석 및 저장
local_importances = {}
output_dir = r'c:\Users\View\cleaned_dataset\data_analysis\dashboard\public\shap'
os.makedirs(output_dir, exist_ok=True)

plt.style.use('dark_background')

for bid in df['battery_id'].unique():
    # 해당 배터리 인덱스 추출
    indices = df[df['battery_id'] == bid].index
    battery_shap_values = shap_values_all[indices]
    battery_X = X_scaled_df.iloc[indices]
    
    # Feature Importance (Mean Absolute SHAP)
    mean_abs_shap = np.abs(battery_shap_values).mean(axis=0)
    importance_df = pd.DataFrame({
        'Feature': feature_cols,
        'Mean_SHAP_Importance': mean_abs_shap
    }).sort_values(by='Mean_SHAP_Importance', ascending=False)
    
    local_importances[bid] = importance_df.to_dict(orient='records')
    
    # SHAP Summary Plot 저장
    plt.figure(figsize=(10, 8))
    # 단일 배터리라도 여러 사이클이 있으므로 swarm plot 가능
    shap.summary_plot(battery_shap_values, battery_X, show=False, plot_type="dot")
    plt.title(f"SHAP Analysis for {bid}", fontsize=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{bid}_summary.png"), dpi=100, bbox_inches='tight')
    plt.close()
    
    print(f"Processed {bid}")

# 5. JSON 저장
with open(r'c:\Users\View\cleaned_dataset\data_analysis\dashboard\src\local_shap_importance.json', 'w') as f:
    json.dump(local_importances, f)

print("Battery-specific SHAP analysis completed.")
