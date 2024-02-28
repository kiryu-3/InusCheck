import sqlite3
from datetime import datetime
from models import db, User, UserInfo, UserSkill
# データベースに接続
conn = sqlite3.connect('../instance/test.db')
cursor = conn.cursor()

# skill1 から skill66 までの列に対して、"hatena" を "unknown" に置き換える
# for i in range(1, 67):
#     column_name = f'skill{i}'
#     cursor.execute(f"UPDATE user_skill SET {column_name} = 'unknown' WHERE {column_name} = 'hatena';")

# user_idが16のデータを削除
# cursor.execute("DELETE FROM user_info WHERE user_id = 16 and date_added = '2024.01.12';")
# user_idが16のデータを削除
# cursor.execute("DELETE FROM user_skill WHERE user_id = 16 and date_added = '2024.01.12';")

# user_idが16のデータを削除
# cursor.execute("DELETE FROM user WHERE id = 16;")
# user_idが17のデータを削除
# cursor.execute("DELETE FROM user WHERE id = 17;")

# cursor.execute("DROP TABLE user_info")
# cursor.execute("DELETE FROM user_skill")
# cursor.execute("DROP TABLE user_anketo")

# 2024-01-09 00:00:00.000000 を '2024.01.09' に変換
# cursor.execute("UPDATE user_info SET date_added = strftime('%Y.%m.%d', date_added);")
# cursor.execute("UPDATE user_skill SET date_added = strftime('%Y.%m.%d', date_added);")

# 変更をコミット
conn.commit()

# 接続を閉じる
conn.close()


