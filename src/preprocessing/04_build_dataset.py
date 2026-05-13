import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# merged dataset ?�기
# ==================================================

df = pd.read_csv(
    "data/processed/merged_feature_dataset.csv"
)

# ==================================================
# ?�이저장?�인
# ==================================================

print("\n원본 데이터")

print(df.head())

print("\nShape")

print(df.shape)

# ==================================================
# Battery Context ?�보
# ==================================================

# cutoff voltage ?�보
cutoff_dict = {

    'B0005': 2.7,
    'B0006': 2.5,
    'B0007': 2.2,
    'B0018': 2.5,

    'B0025': 2.0,
    'B0026': 2.2,
    'B0027': 2.5,
    'B0028': 2.7,

    # high temperature
    'B0029': 2.0,
    'B0030': 2.2,
    'B0031': 2.5,
    'B0032': 2.7,

}

# ambient temperature ?�보
temp_dict = {

    'B0005': 24,
    'B0006': 24,
    'B0007': 24,
    'B0018': 24,

    'B0025': 24,
    'B0026': 24,
    'B0027': 24,
    'B0028': 24,

     # high temperature
    'B0029': 44,
    'B0030': 44,
    'B0031': 44,
    'B0032': 44
}

# ==================================================
# battery�?처리 리스저장
# ==================================================

processed_list = []

# ==================================================
# battery 목록
# ==================================================

battery_ids = df[
    'battery_id'
].unique()

# ==================================================
# EOL 기�?
# ==================================================

EOL_PERCENT = 0.8

# ==================================================
# battery 반복
# ==================================================

for battery_id in battery_ids:

    # ------------------------------------------------
    # battery ?�이저장?�택
    # ------------------------------------------------

    battery_df = df[
        df['battery_id']
        == battery_id
    ].copy().sort_values('cycle')

    # ==================================================
    # [Fix] Anomaly Handling: Capacity & Impedance Outliers
    # ==================================================
    # 1. Capacity Smoothing (Rolling average to remove sudden dips)
    battery_df['Capacity'] = battery_df['Capacity'].rolling(window=3, center=True, min_periods=1).mean()
    
    # 2. Monotonic Constraint for EOL detection (Capacity should generally decrease)
    # Note: We use cumulative minimum to ensure we don't recover from a "fake" dip for EOL calculation
    battery_df['Capacity_monotone'] = battery_df['Capacity'].cummin()

    # 3. Impedance Stability (Prevent abnormal decrease in late stages)
    # Impedance typically increases with aging.
    # We use a combined approach: Smoothing + Cumulative Max to maintain physics consistency.
    battery_df['Re'] = battery_df['Re'].rolling(window=5, center=True, min_periods=1).mean()
    battery_df['Rct'] = battery_df['Rct'].rolling(window=5, center=True, min_periods=1).mean()
    
    # Soft constraint: Impedance should not decrease significantly below the initial value
    initial_re = battery_df['Re'].iloc[0]
    initial_rct = battery_df['Rct'].iloc[0]
    battery_df['Re'] = battery_df['Re'].cummax().clip(lower=initial_re)
    battery_df['Rct'] = battery_df['Rct'].cummax().clip(lower=initial_rct)

    # ==================================================
    # Context Feature 추�?
    # ==================================================

    battery_df['cutoff_voltage'] = (

        cutoff_dict[battery_id]
    )

    battery_df['ambient_temperature'] = (

        temp_dict[battery_id]
    )

    # ==================================================
    # Arrhenius-like Feature
    # ==================================================

    battery_df['inv_temperature'] = (

        1
        /
        (
            battery_df[
                'ambient_temperature'
            ]
            + 273.15
        )
    )

    # ==================================================
    # 초기 capacity
    # ==================================================

    initial_capacity = battery_df[
        'Capacity'
    ].max()

    # ==================================================
    # threshold 계산
    # ==================================================

    threshold = (

        initial_capacity
        *
        EOL_PERCENT
    )

    print("\n====================")

    print(f"Battery : {battery_id}")

    print(f"Initial Capacity : {initial_capacity}")

    print(f"Min Capacity : {battery_df['Capacity'].min()}")

    print(f"EOL Threshold : {threshold}")

    # ==================================================
    # EOL ?�이저장찾기
    # ==================================================

    eol_data = battery_df[
        battery_df['Capacity_monotone']
        <= threshold
    ]

    # ==================================================
    # EOL ?�는 경우 skip
    # ==================================================
    if len(eol_data) == 0:

        print("EOL not reached")

        print("Using last cycle as pseudo-EOL")

        eol_cycle = battery_df['cycle'].max()

    else:

        eol_cycle = eol_data.iloc[0]['cycle']

    # ==================================================
    # 최초 EOL cycle
    # ==================================================

    print(f"EOL Cycle : {eol_cycle}")

    # ==================================================
    # Absolute RUL ?�성
    # ==================================================

    battery_df['RUL'] = (

        eol_cycle
        -
        battery_df['cycle']

    ).clip(lower=0)

    # ==================================================
    # Relative RUL ?�성 (%)
    # ==================================================

    battery_df['Relative_RUL'] = (
        (battery_df['Capacity'] - threshold) 
        / (initial_capacity - threshold) 
        * 100
    ).clip(lower=0, upper=100)

    # ==================================================
    # EOL cycle ?�저장
    # ==================================================

    battery_df['EOL_cycle'] = (
        eol_cycle
    )

    # ==================================================
    # Delta Feature ?�성
    # ==================================================

    battery_df['delta_middle_voltage'] = (

        battery_df[
            'middle_voltage_mean'
        ].diff()
    )

    battery_df['delta_discharge_duration'] = (

        battery_df[
            'discharge_duration'
        ].diff()
    )

    battery_df['delta_Rct'] = (

        battery_df[
            'Rct'
        ].diff()
    )

    battery_df['delta_Re'] = (

        battery_df[
            'Re'
        ].diff()
    )

    battery_df['delta_interval_38_35'] = (

        battery_df[
            'interval_38_35'
        ].diff()
    )

    battery_df['delta_area_38_35'] = (

        battery_df[
            'area_38_35'
        ].diff()
    )

    # ==================================================
    # 리스저장추�?
    # ==================================================

    processed_list.append(
        battery_df
    )

# ==================================================
# 최종 ?�이저장결합
# ==================================================

final_df = pd.concat(

    processed_list,

    ignore_index=True
)

# ==================================================
# NaN ?�인
# ==================================================

print("\nNaN 개수")

print(final_df.isnull().sum())

# ==================================================
# NaN ?�거
# ==================================================

final_df = final_df.dropna()

# ==================================================
# 최종 feature ?�택
# ==================================================

feature_cols = [

    # voltage feature
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

    # voltage slope
    'voltage_slope',

    # resistance proxy
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

    # context feature
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
# X / y ?�성
# ==================================================

X = final_df[
    feature_cols
]

# Relative RUL ?�용
y = final_df[
    'Relative_RUL'
]

# ==================================================
# ?�이저장?�인
# ==================================================

print("\n최종 Feature")

print(feature_cols)

print("\nX shape")

print(X.shape)

print("\ny shape")

print(y.shape)

# ==================================================
# Relative RUL 분포 ?�인
# ==================================================

plt.figure(figsize=(10,6))

plt.hist(

    final_df['Relative_RUL'],

    bins=30
)

plt.title(
    'Relative RUL Distribution'
)

plt.xlabel(
    'Relative RUL (%)'
)

plt.ylabel(
    'Count'
)

plt.grid()


plt.savefig('results/figures/relative_rul_distribution.png', dpi=300, bbox_inches='tight')

# ==================================================
# Battery�?Relative RUL Trajectory
# ==================================================

plt.figure(figsize=(12,6))

for battery_id in final_df[
    'battery_id'
].unique():

    battery_df = final_df[

        final_df['battery_id']
        == battery_id
    ]

    plt.plot(

        battery_df['cycle'],

        battery_df['Relative_RUL'],

        label=battery_id
    )

plt.title(
    'Battery-wise Relative RUL'
)

plt.xlabel('Cycle')

plt.ylabel('Relative RUL (%)')

plt.legend()

plt.grid()

plt.savefig('results/figures/battery_relative_rul.png', dpi=300, bbox_inches='tight')

# ==================================================
# ?�저장
# ==================================================

final_df.to_csv(
    "data/processed/final_battery_dataset.csv",
    index=False
)

print("\nfinal_battery_dataset.csv ?�저장?�료")
