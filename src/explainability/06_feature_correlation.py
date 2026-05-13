import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

# ==================================================
# 최종 dataset 불러오기
# ==================================================

df = pd.read_csv(
    "../../data/processed/final_battery_dataset.csv"
)

# ==================================================
# 분석할 feature 선택
# ==================================================

feature_cols = [

    # voltage mean
    'early_voltage_mean',
    'middle_voltage_mean',
    'late_voltage_mean',

    # discharge
    'discharge_duration',

    # voltage transition
    'interval_40_38',
    'interval_38_35',
    'interval_35_32',

    # voltage area
    'area_40_38',
    'area_38_35',
    'area_35_32',

    # instability
    'dvdt_35',
    'dv_dt_std',

    # resistance
    'mean_internal_resistance',

    'Re',
    'Rct',

    # delta
    'delta_Rct',
    'delta_Re',

    'delta_interval_38_35',
    'delta_area_38_35'
]

# ==================================================
# correlation 계산
# ==================================================

corr_matrix = df[
    feature_cols
].corr()

# ==================================================
# correlation 출력
# ==================================================

print("\n====================")

print("Correlation Matrix")

print(corr_matrix)

# ==================================================
# Heatmap 시각화
# ==================================================

plt.figure(figsize=(14,12))

plt.imshow(

    corr_matrix,

    cmap='coolwarm',

    interpolation='nearest'
)

plt.colorbar()

plt.xticks(

    range(len(feature_cols)),

    feature_cols,

    rotation=90
)

plt.yticks(

    range(len(feature_cols)),

    feature_cols
)

plt.title(
    'Feature Correlation Heatmap'
)

plt.tight_layout()

plt.savefig('../../results/figures/feature_correlation.png', dpi=300, bbox_inches='tight')


# ==================================================
# 높은 상관관계 출력
# ==================================================

print("\n====================")

print("High Correlation Pairs")

threshold = 0.85

for i in range(len(feature_cols)):

    for j in range(i+1, len(feature_cols)):

        corr_value = corr_matrix.iloc[i,j]

        if abs(corr_value) >= threshold:

            print(

                f"{feature_cols[i]}"
                f" <-> "
                f"{feature_cols[j]}"
                f" : "
                f"{corr_value:.4f}"
            )

# ==================================================
# Correlation 저장
# ==================================================

corr_matrix.to_csv(
    "feature_correlation_matrix.csv"
)

print("\nfeature_correlation_matrix.csv 저장 완료")