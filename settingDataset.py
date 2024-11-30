import geopandas as gpd
from dbfread import DBF
import pandas as pd
import chardet

# DBF 파일 읽기
dbf_file = "C:/Users/lovel/Downloads/FSN_26_20221130_G_001/FSN_26_20221130_G_001.dbf"
table = DBF(dbf_file, encoding="utf-8")

# DBF 데이터를 DataFrame으로 변환
df = pd.DataFrame(iter(table))

# CSV로 저장
csv_file = "C:/Users/lovel/Downloads/dataset.csv"
df.to_csv(csv_file, index=False)

print("DBF 데이터를 CSV로 변환 완료:", csv_file)

# CSV 파일 읽기
csv_file = "C:/Users/lovel/Downloads/dataset2.csv"
df = pd.read_csv(csv_file)

df = df[df["TYPE"] != "여성안전지킴이집"]
df = df[df["TYPE"] != "아동안전지킴이집"]
df = df[df["SIGUNGU"] == "서울"]

# 변경된 DataFrame을 다시 CSV로 저장
df.to_csv("C:/Users/lovel/Downloads/dataset3.csv", index=False)



# 인코딩 변환
# 기존 CSV 파일의 인코딩을 자동으로 감지
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

# 기존 CSV 파일을 UTF-8로 변환하는 함수
def convert_to_utf8(input_file_path, output_file_path):
    encoding = detect_encoding(input_file_path)
    with open(input_file_path, 'r', encoding=encoding) as infile:
        with open(output_file_path, 'w', encoding='utf-8', newline='') as outfile:
            for line in infile:
                outfile.write(line)

# 변환 예시
convert_to_utf8("C:/Users/lovel/Downloads/convenience_dataset.csv", "C:/Users/lovel/Downloads/converted_dataset.csv")
