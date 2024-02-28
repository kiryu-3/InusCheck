import pyfile.RenderingTry as RT
from pyfile.department import department
from flask import Flask, render_template, request
import json
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json
import sys

DP = department()

PATH = "../data/ISBP_Question.csv"

class check:
    def __init__(self):
        pass

    def save(self, kekka, file_path, file_name):
        with open(file_path, "w",encoding='utf-8') as f:
            json.dump(kekka, f, ensure_ascii=False, indent=4)

        RT.rendering(f"check.j2", f"{file_name}.json", f"{file_name}.html")

    def checkmaker(self, user_info, skills):
        df = pd.read_csv(PATH)

        question_dict = {}

        question_dict["email"] = user_info['email']
        question_dict["university"] = user_info['university']
        question_dict["grade"] = user_info['grade']
        question_dict["department"] = user_info['department']
        question_dict["universities"] = DP.departmentmaker(user_info['email'])

        question_dict["categories"] = df["カテゴリ"].unique().tolist()
        question_dict["question"] = list()

        for idx, row in df.iterrows():  # rowには各行のSeriesが入る

            process_dict = dict()

            process_dict["qnumber"] = row["通し番号"]
            process_dict["sentence"] = row["質問文"]
            process_dict["radio_check"] = skills[f'skill{str(idx+1)}']

            question_dict["question"].append(process_dict)

        # file_path = "mysite/result/json/check.json"

        # self.save(question_dict, file_path, "check")

        return question_dict
