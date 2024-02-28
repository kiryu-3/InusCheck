import csv
import pandas as pd
import json
import RenderingTry as RT

def save(kekka, file_path, file_name):
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(kekka, f, ensure_ascii=False, indent=4)

        RT.rendering(f"department.j2", "department.json", f"{file_name}.html")

# CSVファイルに書き込むデータ
PATH = "../data/university_data.csv"
df = pd.read_csv(PATH)
print(df)

# CSVファイルに書き込むデータ
data = {
    "name":["Chitose","Hokudai","Muroran"],
    "sex":["female","male","male"],
    "Age":[35,105,74]
}
file_path = "../result/json/department.json"

save(data, file_path, "dashboard")