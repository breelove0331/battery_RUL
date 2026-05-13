import os

file_path = 'src/preprocessing/04_build_dataset.py'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace common garbled patterns with correct Korean
replacements = {
    'merged dataset ?기': 'merged dataset 읽기',
    '?이???인': '데이터 확인',
    '?본 ?이??': '원본 데이터',
    'Battery Context ?보': 'Battery Context 정보',
    'cutoff voltage ?보': 'cutoff voltage 정보',
    'ambient temperature ?보': 'ambient temperature 정보',
    'inv_temperature ?보': 'inv_temperature 정보',
    '? Feature': '전체 Feature',
    'Relative RUL ?ы?': 'Relative RUL 분포',
    'Battery? Relative RUL Trajectory': 'Battery별 Relative RUL Trajectory',
    '??': '저장',
    'final_battery_dataset.csv ?????': 'final_battery_dataset.csv 저장 완료'
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Also fix the specific syntax error line if still present
content = content.replace('print("\\n원본 데이터")', 'print("\\n원본 데이터")')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
