import pandas as pd
import numpy as np

# ==================================================
# 시각화
# ==================================================

import matplotlib.pyplot as plt

# ==================================================
# XGBoost
# ==================================================

from xgboost import XGBRegressor

# ==================================================
# 평가 함수
# ==================================================

from sklearn.metrics import (

    mean_absolute_error,

    mean_squared_error,

    r2_score
)

# ==================================================
# 데이터 스케일링
# ==================================================

from sklearn.preprocessing import StandardScaler

# ==================================================
# 최종 데이터셋 불러오기
# ==================================================

df = pd.read_csv(
    "../../data/processed/final_battery_dataset.csv"
)

# ==================================================
# 데이터 확인
# ==================================================

print("\n데이터 확인")

print(df.head())

print("\nShape")

print(df.shape)

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

    # delta feature
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

test_battery = 'B0031'

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

# ==================================================
# Relative RUL 사용
# ==================================================

y_train = train_df[
    'Relative_RUL'
]

y_test = test_df[
    'Relative_RUL'
]

# ==================================================
# EOL cycle 저장
# ==================================================

test_eol_cycle = test_df[
    'EOL_cycle'
].iloc[0]

# ==================================================
# Shape 확인
# ==================================================

print("\n====================")

print("Train/Test Shape")

print("\nX_train")

print(X_train.shape)

print("\ny_train")

print(y_train.shape)

print("\nX_test")

print(X_test.shape)

print("\ny_test")

print(y_test.shape)

# ==================================================
# Standard Scaling
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

    # regularization
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
# Relative RUL 예측
# ==================================================

y_pred_relative = model.predict(
    X_test_scaled
)

# ==================================================
# Relative RUL → 실제 RUL 역변환
# ==================================================

actual_rul = (

    y_test / 100

) * test_eol_cycle

predicted_rul = (

    y_pred_relative / 100

) * test_eol_cycle

# ==================================================
# 평가 지표 계산
# ==================================================

mae = mean_absolute_error(

    actual_rul,

    predicted_rul
)

rmse = np.sqrt(

    mean_squared_error(

        actual_rul,

        predicted_rul
    )
)

r2 = r2_score(

    actual_rul,

    predicted_rul
)

# ==================================================
# 성능 출력
# ==================================================

print("\n====================")

print("모델 성능")

print(f"\nMAE : {mae:.4f}")

print(f"\nRMSE : {rmse:.4f}")

print(f"\nR2 Score : {r2:.4f}")

# ==================================================
# 결과 dataframe 생성
# ==================================================

result_df = pd.DataFrame({

    'Actual_RUL':
        actual_rul.values,

    'Predicted_RUL':
        predicted_rul
})

print("\n예측 결과")

print(result_df.head())

# ==================================================
# Actual vs Predicted 그래프
# ==================================================

plt.figure(figsize=(12,6))

plt.plot(

    actual_rul.values,

    label='Actual RUL',

    linewidth=2
)

plt.plot(

    predicted_rul,

    label='Predicted RUL',

    linewidth=2
)

plt.title(
    f'Actual vs Predicted RUL ({test_battery})'
)

plt.xlabel('Sample')

plt.ylabel('RUL')

plt.legend()

plt.grid()

plt.savefig('../../results/figures/actual_vs_predicted.png', dpi=300, bbox_inches='tight')

# ==================================================
# Feature Importance 계산
# ==================================================

importance_df = pd.DataFrame({

    'Feature': feature_cols,

    'Importance':
        model.feature_importances_
})

# ==================================================
# 중요도 정렬
# ==================================================

importance_df = importance_df.sort_values(

    by='Importance',

    ascending=False
)

# ==================================================
# 중요도 출력
# ==================================================

print("\nFeature Importance")

print(importance_df)

# ==================================================
# 중요도 시각화
# ==================================================

plt.figure(figsize=(10,8))

plt.barh(

    importance_df['Feature'],

    importance_df['Importance']
)

plt.title(
    'Feature Importance'
)

plt.xlabel('Importance')

plt.ylabel('Feature')

plt.grid()

plt.savefig('../../results/figures/feature_importance.png', dpi=300, bbox_inches='tight')


# ==================================================
# 결과 저장
# ==================================================

result_df.to_csv(

    "xgboost_prediction_result.csv",

    index=False
)

print("\nxgboost_prediction_result.csv 저장 완료")