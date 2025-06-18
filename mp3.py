import os
import subprocess
from pathlib import Path
import sys

# 入力フォルダ（結合したいMP3ファイルがある場所）
input_dir = r"C:\tenp1"

# 出力フォルダ（結合後のファイルを保存する場所）
output_dir = r"C:\tenp2"
os.makedirs(output_dir, exist_ok=True)

# 連結ファイル数
group_size = 10

# 保存ファイル名
output_prefix = 'output'

# .mp3ファイルを取得し、ソート
mp3_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.mp3')])
mp3_files = [os.path.join(input_dir, f) for f in mp3_files]

# ✅ ファイル数チェック：10未満なら終了
if len(mp3_files) < group_size:
    print(f"⚠️ 結合対象が {len(mp3_files)} 個しかありません。{group_size} 個未満なので処理を終了します。")
    sys.exit()

# 10個ずつに分割して結合
for i in range(0, len(mp3_files), group_size):
    group = mp3_files[i:i + group_size]
    if len(group) < group_size:
        print(f"⚠️ 残りファイル数が {len(group)} 個しかないためスキップ（必要数: {group_size}）")
        break

    concat_file = f'concat_list_{i//group_size}.txt'
    with open(concat_file, 'w') as f:
        for file in group:
            f.write(f"file '{file}'\n")

    output_file = os.path.join(output_dir, f'{output_prefix}_{i//group_size}.mp3')

    subprocess.run([
        'ffmpeg', '-f', 'concat', '-safe', '0',
        '-i', concat_file,
        '-c', 'copy', output_file
    ])

    print(f'✅ 結合完了: {output_file}')

    os.remove(concat_file)
