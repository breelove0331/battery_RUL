import pandas as pd
import os

# -----------------------------
# metadata.csv 불러오기
# -----------------------------
metadata_df = pd.read_csv(
    "../../../metadata.csv"
)

# -----------------------------
# metadata 확인
# -----------------------------
print(metadata_df.head())

# -----------------------------
# 사용할 battery 선택
# -----------------------------
battery_id = 'B0005'

# -----------------------------
# discharge 데이터만 선택
# -----------------------------
battery_df = metadata_df[
    (metadata_df['battery_id'] == battery_id) &
    (metadata_df['type'] == 'discharge')
]

# -----------------------------
# 데이터 폴더 경로
# -----------------------------
DATA_PATH = "../../../data"

# -----------------------------
# 모든 discharge cycle 반복
# -----------------------------
for idx, row in battery_df.iterrows():

    # 실제 csv 파일명
    file_name = row['filename']

    # csv 경로 생성
    file_path = os.path.join(
        DATA_PATH,
        file_name
    )

    print("\n====================")
    print(f"파일명 : {file_name}")

    # csv 읽기
    cycle_df = pd.read_csv(
        file_path
    )

    # 데이터 확인
    print("\n데이터 head")
    print(cycle_df.head())

    # 컬럼 확인
    print("\n컬럼 목록")
    print(cycle_df.columns)

    # 데이터 shape 확인
    print("\n데이터 shape")
    print(cycle_df.shape)

    # 첫 번째 cycle만 확인 후 종료
    break