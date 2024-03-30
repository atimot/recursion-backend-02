import os

# 生成したいファイルのサイズ（バイト単位）
target_size = 100 * 1024  # 100MB

# ファイルパス
file_path = 'sample.txt'

# ファイルを開き、指定されたサイズに達するまでランダムな文字列を書き込む
with open(file_path, 'w') as file:
    while os.path.getsize(file_path) < target_size:
        # 英数字からランダムに選ばれた文字を書き込む
        file.write(os.urandom(1024).hex())

# 最終ファイルサイズを確認
final_size = os.path.getsize(file_path)
final_size, file_path
