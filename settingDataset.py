import geopandas as gpd
from dbfread import DBF
import pandas as pd

# # DBF 파일 읽기
# dbf_file = "C:/Users/lovel/Downloads/FSN_26_20221130_G_001/FSN_26_20221130_G_001.dbf"
# table = DBF(dbf_file, encoding="utf-8")

# # DBF 데이터를 DataFrame으로 변환
# df = pd.DataFrame(iter(table))

# # CSV로 저장
# csv_file = "C:/Users/lovel/Downloads/dataset.csv"
# df.to_csv(csv_file, index=False)

# print("DBF 데이터를 CSV로 변환 완료:", csv_file)

# CSV 파일 읽기
csv_file = "C:/Users/lovel/Downloads/dataset2.csv"
df = pd.read_csv(csv_file)

# # 특정 열(column_name)의 값이 'A'인 행 삭제
# # df = df[df["TYPE"] != "여성안전지킴이집"]

# # 특정 열(column_name)의 값이 'A'인 행 삭제
# df = df[df["TYPE"] != "아동안전지킴이집"]

# 특정 열(column_name)의 값이 'A'인 행 삭제
df = df[df["SIGUNGU"] == "서울"]


# 변경된 DataFrame을 다시 CSV로 저장
df.to_csv("C:/Users/lovel/Downloads/dataset3.csv", index=False)

