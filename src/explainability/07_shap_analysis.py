import pandas as pd
import numpy as np

# ==================================================
# 시각화
# ==================================================

import matplotlib.pyplot as plt

# ==================================================
# SHAP
# ==================================================

import shap

# ==================================================
# XGBoost
# ==================================================

from xgboost import XGBRegressor

# ==================================================
# Scaling
# ==================================================

from sklearn.preprocessing import StandardScaler

# ==================================================
# 데이터 불러오기
# ==================================================

df = pd.read_csv(
    "../../data/processed/final_battery_dataset.csv"
)

# ==================================================
# Battery 종류 확인
# ==================================================

print("\nBattery 종류")

print(df['battery_id'].unique())

# ==================================================
# 사용할 feature
# ==================================================

feature_cols = [

    # voltage mean
    'early_voltage_mean',
    'middle_voltage_mean',
    'late_voltage_mean',

    # temperature
    'max_temperature',
    'temperature_rise',

    # current
    'mean_current',

    # discharge
    'discharge_duration',

    # slope
    'voltage_slope',

    # resistance
    'mean_internal_resistance',

    # voltage transition
    'interval_40_38',
    'interval_38_35',
    'interval_35_32',

    # voltage area
    'area_40_38',
    'area_38_35',
    'area_35_32',

    # collapse acceleration
    'dvdt_35',

    # instability
    'dv_dt_std',

    # impedance
    'Re',
    'Rct',

    # context
    'cutoff_voltage',
    'ambient_temperature',
    'inv_temperature',

    # delta
    'delta_middle_voltage',
    'delta_discharge_duration',

    'delta_Rct',
    'delta_Re',

    'delta_interval_38_35',
    'delta_area_38_35'
]

# ==================================================
# Leave-One-Battery-Out
# ==================================================

test_battery = 'B0006'

# ==================================================
# train / test 분리
# ==================================================

train_df = df[

    df['battery_id']
    != test_battery
]

test_df = df[

    df['battery_id']
    == test_battery
]

# ==================================================
# X / y 생성
# ==================================================

X_train = train_df[
    feature_cols
]

X_test = test_df[
    feature_cols
]

y_train = train_df[
    'Relative_RUL'
]

y_test = test_df[
    'Relative_RUL'
]

# ==================================================
# Scaling
# ==================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)

print("\nScaling 완료")

# ==================================================
# XGBoost 모델 생성
# ==================================================

model = XGBRegressor(

    n_estimators=700,

    learning_rate=0.02,

    max_depth=4,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42,

    reg_alpha=0.5,

    reg_lambda=1.0
)

# ==================================================
# 모델 학습
# ==================================================

model.fit(

    X_train_scaled,

    y_train
)

print("\nXGBoost 학습 완료")

# ==================================================
# SHAP Explainer 생성
# ==================================================

explainer = shap.Explainer(
    model
)

# ==================================================
# SHAP Value 계산
# ==================================================

shap_values = explainer(
    X_test_scaled
)

print("\nSHAP Value 계산 완료")

# ==================================================
# SHAP Summary Plot
# ==================================================

print("\nSHAP Summary Plot 생성")

shap.summary_plot(

    shap_values,

    X_test,

    feature_names=feature_cols,

    show=False
)

plt.tight_layout()

plt.savefig(

    "../../results/figures/shap_summary.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()

print("\nshap_summary.png 저장 완료")

# ==================================================
# SHAP Bar Plot
# ==================================================

print("\nSHAP Bar Plot 생성")

shap.summary_plot(

    shap_values,

    X_test,

    feature_names=feature_cols,

    plot_type='bar',

    show=False
)

plt.tight_layout()

plt.savefig(

    "../../results/figures/shap_bar_importance.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()

print("\nshap_bar_importance.png 저장 완료")

# ==================================================
# Dependence Plot
# interval_38_35
# ==================================================

print("\nDependence Plot 생성")

shap.dependence_plot(

    'interval_38_35',

    shap_values.values,

    X_test,

    feature_names=feature_cols,

    show=False
)

plt.tight_layout()

plt.savefig(

    "../../results/figures/shap_dependence_plot.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()

print("\ninterval_38_35_dependence.png 저장 완료")

# ==================================================
# SHAP Importance DataFrame
# ==================================================

shap_importance = pd.DataFrame({

    'Feature': feature_cols,

    'Mean_SHAP_Importance':

        np.abs(
            shap_values.values
        ).mean(axis=0)
})

# ==================================================
# 중요도 정렬
# ==================================================

shap_importance = shap_importance.sort_values(

    by='Mean_SHAP_Importance',

    ascending=False
)

# ==================================================
# 출력
# ==================================================

print("\n====================")

print("SHAP Importance")

print(shap_importance)

# ==================================================
# 저장
# ==================================================

shap_importance.to_csv(

    "shap_feature_importance.csv",

    index=False
)

print("\nshap_feature_importance.csv 저장 완료")

# ==================================================
# Top 10 SHAP Importance 출력
# ==================================================

print("\nTop 10 Feature")

print(
    shap_importance.head(10)
)

# ==================================================
# 프로젝트 핵심 해석 출력
# ==================================================

top_feature = shap_importance.iloc[0]['Feature']

print("\n====================")

print("핵심 해석")

print(

    f"\n가장 중요한 Feature는 "
    f"{top_feature} 입니다."
)

print(

    "\n모델은 단순 용량 감소보다 "
    "전압 Plateau Stability 변화를 "
    "중요하게 학습하고 있을 가능성이 높습니다."
)

print(

    "\n특히 interval_38_35 구간은 "
    "배터리 degradation acceleration과 "
    "강하게 연결될 수 있습니다."
)