import pandas as pd
import numpy as np
import os

# ==================================================
# metadata.csv 불러오기
# ==================================================

metadata_df = pd.read_csv(
    "../../../metadata.csv"
)

# ==================================================
# 사용할 battery 목록
# ==================================================

battery_list = [

    # room temperature
    'B0005',
    'B0006',
    'B0007',
    'B0018',

    # dynamic load
    'B0025',
    'B0026',
    'B0027',
    'B0028',

     # high temperature (44°C)
    'B0029',
    'B0030',
    'B0031',
    'B0032'
]

# ==================================================
# 데이터 폴더 경로
# ==================================================

DATA_PATH = "../../../data"

# ==================================================
# feature 저장 리스트
# ==================================================

feature_list = []

# ==================================================
# Voltage Threshold Time 함수
# ==================================================

def get_time_at_voltage(

    df,

    voltage_threshold
):

    below_df = df[

        df['Voltage_measured']
        <= voltage_threshold
    ]

    if len(below_df) > 0:

        return below_df.iloc[0]['Time']

    else:

        return np.nan

# ==================================================
# Voltage Area 계산 함수
# ==================================================

def calculate_voltage_area(

    df,

    upper_v,

    lower_v
):

    section_df = df[

        (df['Voltage_measured'] <= upper_v)

        &

        (df['Voltage_measured'] >= lower_v)
    ]

    if len(section_df) > 1:

        return np.trapezoid(

            section_df[
                'Voltage_measured'
            ],

            section_df[
                'Time'
            ]
        )

    else:

        return np.nan

# ==================================================
# battery 반복
# ==================================================

for battery_id in battery_list:

    print("\n====================")

    print(f"Battery : {battery_id}")

    # ==================================================
    # discharge 데이터 선택
    # ==================================================

    battery_df = metadata_df[

        (metadata_df['battery_id'] == battery_id)

        &

        (metadata_df['type'] == 'discharge')

    ].copy()

    # ==================================================
    # cycle 생성
    # ==================================================

    battery_df['cycle'] = range(

        1,

        len(battery_df) + 1
    )

    # ==================================================
    # 각 cycle 반복
    # ==================================================

    for idx, row in battery_df.iterrows():

        # ------------------------------------------------
        # csv 파일명
        # ------------------------------------------------

        file_name = row['filename']

        # ------------------------------------------------
        # 파일 경로 생성
        # ------------------------------------------------

        file_path = os.path.join(

            DATA_PATH,

            file_name
        )

        # ------------------------------------------------
        # csv 읽기
        # ------------------------------------------------

        cycle_df = pd.read_csv(
            file_path
        )

        # ------------------------------------------------
        # 데이터 길이
        # ------------------------------------------------

        n = len(cycle_df)

        # ==================================================
        # 초기 / 중기 / 말기 분할
        # ==================================================

        early_df = cycle_df.iloc[
            : n // 3
        ]

        middle_df = cycle_df.iloc[
            n // 3 : 2 * n // 3
        ]

        late_df = cycle_df.iloc[
            2 * n // 3 :
        ]

        # ==================================================
        # 구간별 평균 전압
        # ==================================================

        early_voltage_mean = early_df[
            'Voltage_measured'
        ].mean()

        middle_voltage_mean = middle_df[
            'Voltage_measured'
        ].mean()

        late_voltage_mean = late_df[
            'Voltage_measured'
        ].mean()

        # ==================================================
        # 온도 feature
        # ==================================================

        max_temperature = cycle_df[
            'Temperature_measured'
        ].max()

        temperature_rise = (

            cycle_df[
                'Temperature_measured'
            ].iloc[-1]

            -

            cycle_df[
                'Temperature_measured'
            ].iloc[0]
        )

        # ==================================================
        # 평균 전류
        # ==================================================

        mean_current = cycle_df[
            'Current_measured'
        ].mean()

        # ==================================================
        # 방전 시간
        # ==================================================

        discharge_duration = cycle_df[
            'Time'
        ].max()

        # ==================================================
        # 전압 감소 기울기
        # ==================================================

        voltage_slope = (

            cycle_df[
                'Voltage_measured'
            ].iloc[-1]

            -

            cycle_df[
                'Voltage_measured'
            ].iloc[0]

        ) / n

        # ==================================================
        # 내부 저항 근사
        # ==================================================

        cycle_df[
            'internal_resistance'
        ] = (

            cycle_df[
                'Voltage_measured'
            ]

            /

            np.abs(

                cycle_df[
                    'Current_measured'
                ]
            )
        )

        mean_internal_resistance = cycle_df[
            'internal_resistance'
        ].mean()

        # ==================================================
        # Voltage Threshold Time 계산
        # ==================================================

        time_40 = get_time_at_voltage(

            cycle_df,

            4.0
        )

        time_38 = get_time_at_voltage(

            cycle_df,

            3.8
        )

        time_35 = get_time_at_voltage(

            cycle_df,

            3.5
        )

        time_32 = get_time_at_voltage(

            cycle_df,

            3.2
        )

        # ==================================================
        # Interval Duration 계산
        # ==================================================

        interval_40_38 = (
            time_38 - time_40
        )

        interval_38_35 = (
            time_35 - time_38
        )

        interval_35_32 = (
            time_32 - time_35
        )

        # ==================================================
        # 구간별 Voltage Area
        # ==================================================

        area_40_38 = calculate_voltage_area(

            cycle_df,

            4.0,

            3.8
        )

        area_38_35 = calculate_voltage_area(

            cycle_df,

            3.8,

            3.5
        )

        area_35_32 = calculate_voltage_area(

            cycle_df,

            3.5,

            3.2
        )

        # ==================================================
        # dV/dt 계산
        # ==================================================

        dv = cycle_df[
            'Voltage_measured'
        ].diff()

        dt = cycle_df[
            'Time'
        ].diff()

        dv_dt = dv / dt

        dv_dt = dv_dt.replace(

            [np.inf, -np.inf],

            np.nan
        )

        # ==================================================
        # 특정 구간 dV/dt
        # ==================================================

        dvdt_35_df = cycle_df[

            (cycle_df[
                'Voltage_measured'
            ] <= 3.6)

            &

            (cycle_df[
                'Voltage_measured'
            ] >= 3.4)
        ]

        if len(dvdt_35_df) > 1:

            dv_35 = dvdt_35_df[
                'Voltage_measured'
            ].diff()

            dt_35 = dvdt_35_df[
                'Time'
            ].diff()

            dvdt_35 = (

                dv_35 / dt_35

            ).mean()

        else:

            dvdt_35 = np.nan

        # ==================================================
        # 전체 dV/dt instability
        # ==================================================

        dv_dt_std = dv_dt.std()

        # ==================================================
        # Capacity
        # ==================================================

        capacity = pd.to_numeric(

            row['Capacity'],

            errors='coerce'
        )

        # ==================================================
        # feature dictionary
        # ==================================================

        feature_dict = {

            'battery_id':
                battery_id,

            'cycle':
                row['cycle'],

            'Capacity':
                capacity,

            # voltage feature
            'early_voltage_mean':
                early_voltage_mean,

            'middle_voltage_mean':
                middle_voltage_mean,

            'late_voltage_mean':
                late_voltage_mean,

            # temperature
            'max_temperature':
                max_temperature,

            'temperature_rise':
                temperature_rise,

            # current
            'mean_current':
                mean_current,

            # discharge
            'discharge_duration':
                discharge_duration,

            # slope
            'voltage_slope':
                voltage_slope,

            # resistance
            'mean_internal_resistance':
                mean_internal_resistance,

            # interval duration
            'interval_40_38':
                interval_40_38,

            'interval_38_35':
                interval_38_35,

            'interval_35_32':
                interval_35_32,

            # interval area
            'area_40_38':
                area_40_38,

            'area_38_35':
                area_38_35,

            'area_35_32':
                area_35_32,

            # collapse acceleration
            'dvdt_35':
                dvdt_35,

            # instability
            'dv_dt_std':
                dv_dt_std
        }

        # ==================================================
        # 리스트 추가
        # ==================================================

        feature_list.append(
            feature_dict
        )

# ==================================================
# 최종 dataframe 생성
# ==================================================

feature_df = pd.DataFrame(
    feature_list
)

# ==================================================
# 결과 확인
# ==================================================

print("\n====================")

print("Feature Dataset")

print(feature_df.head())

print("\nShape")

print(feature_df.shape)

print("\n컬럼 목록")

print(feature_df.columns)

# ==================================================
# NaN 확인
# ==================================================

print("\nNaN 개수")

print(feature_df.isnull().sum())

# ==================================================
# 저장
# ==================================================

    "../../data/processed/feature_dataset.csv",

    index=False
)

print("\nfeature_dataset.csv 저장 완료")