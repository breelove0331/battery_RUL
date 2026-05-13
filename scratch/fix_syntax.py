import os

file_path = 'src/preprocessing/04_build_dataset.py'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Fix the broken quote on line 17
    if 'print("\\n' in line and '?)' in line:
        new_lines.append('print("\\n원본 데이터")\n')
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
