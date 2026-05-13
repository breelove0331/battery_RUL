import pandas as pd
import numpy as np

# -----------------------------
# discharge feature dataset 읽기
# -----------------------------
feature_df = pd.read_csv(
    "../../data/processed/feature_dataset.csv"
)

# -----------------------------
# metadata.csv 읽기
# -----------------------------
metadata_df = pd.read_csv(
    "../../../metadata.csv"
)

# -----------------------------
# impedance 데이터만 선택
# -----------------------------
impedance_df = metadata_df[
    metadata_df['type'] == 'impedance'
].copy()

# -----------------------------
# battery별 impedance cycle 생성
# -----------------------------
impedance_df['cycle'] = (
    impedance_df.groupby(
        'battery_id'
    ).cumcount() + 1
)

# -----------------------------
# 사용할 impedance feature 선택
# -----------------------------
impedance_df = impedance_df[[
    'battery_id',
    'cycle',
    'Re',
    'Rct'
]]

# -----------------------------
# 숫자형 변환
# -----------------------------
impedance_df['Re'] = pd.to_numeric(
    impedance_df['Re'],
    errors='coerce'
)

impedance_df['Rct'] = pd.to_numeric(
    impedance_df['Rct'],
    errors='coerce'
)

# -----------------------------
# impedance 데이터 확인
# -----------------------------
print("\nImpedance Data")

print(impedance_df.head())

print("\nShape")

print(impedance_df.shape)

# -----------------------------
# discharge feature와 merge
# -----------------------------
merged_df = pd.merge_asof(

    feature_df.sort_values('cycle'),

    impedance_df.sort_values('cycle'),

    on='cycle',

    by='battery_id',

    direction='nearest'
)

# -----------------------------
# merge 결과 확인
# -----------------------------
print("\nMerged Data")

print(merged_df.head())

print("\nShape")

print(merged_df.shape)

# -----------------------------
# 저장
# -----------------------------
    "../../data/processed/merged_feature_dataset.csv",

    index=False
)

print("\nmerged_feature_dataset.csv 저장 완료")