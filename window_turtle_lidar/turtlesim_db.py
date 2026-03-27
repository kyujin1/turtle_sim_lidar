import pymysql
import json
import pandas as pd

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='0000',
    database='ros_data',
    charset='utf8'
)
cursor = conn.cursor()
cursor.execute("SELECT ranges, action FROM lidardata")
rows = cursor.fetchall()

all_data = []
for r in rows:
    ranges_list = json.loads(r[0])
    action = r[1]

    ranges_list.append(action)
    all_data.append(ranges_list)

column_names = [f'dist_{i}' for i in range(360)] + ['action']
df = pd.DataFrame(all_data, columns=column_names)

# 5. 결과 확인 및 저장
print(" 변환 완료")
print(df.head())  # 상위 5개 행 출력
print(f" 총 데이터 개수: {len(df)}행, 컬럼 개수: {len(df.columns)}개")

df.to_csv('lidar_dataset_final.csv', index=False)
print("💾 'lidar_dataset_final.csv' 저장 성공")

cursor.close()
conn.close()