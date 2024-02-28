import pyfile.RenderingTry as RT
from flask import Flask, render_template, request
import json
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json
import sys
import kaleido

PATH = "../data/ISBP_Question.csv"

class question:
    def __init__(self):
        pass

    def save(self, kekka, file_path, file_name):
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(kekka, f, ensure_ascii=False, indent=4)

        RT.rendering(f"question.j2", f"{file_name}.json", f"{file_name}.html")

    def questionmaker(self, category_idx, skills, user_info):
        category_list = ["オンライン・コラボレーション力", "データ利活用力", "情報システム開発力", "情報倫理力"]
        category = category_list[category_idx-1]

        df = pd.read_csv(PATH)
        df_category = df[df["カテゴリ"] == category]

        question_dict = {}

        question_dict["email"] = user_info['email']
        question_dict["university"] = user_info['university']
        question_dict["grade"] = user_info['grade']
        question_dict["department"] = user_info['department']

        question_dict["cnumber"] = category_idx
        question_dict["category"] = category

        nextpage_list = ["/dashboard", "/question1", "/question2", "/question3"]
        question_dict["nextpage"] = nextpage_list[category_idx-1]

        question_dict["question"] = list()

        for idx, row in df_category.iterrows():  # rowには各行のSeriesが入る

            process_dict = dict()

            process_dict["qnumber"] = row["通し番号"]
            process_dict["sentence"] = row["質問文"]
            if skills != {}:
                process_dict["radio_check"] = skills[f'skill{str(idx+1)}']
            else:
                process_dict["radio_check"] = None

            question_dict["question"].append(process_dict)

        return question_dict

