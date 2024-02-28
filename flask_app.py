from pyfile.models import db, User, UserInfo, UserSkill, UserAnketo # models.pyから必要なものをインポート
from pyfile.department import department
from pyfile.submit import submit
from pyfile.question import question
from pyfile.check import check
from pyfile.graph import graph
from pyfile.history import history

from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pyfile.submit import submit

import datetime
from datetime import datetime
import plotly.graph_objects as go
import plotly.io as pio
import pytz
import warnings
import sys
import csv
import json

# すべての警告を無視する
warnings.filterwarnings("ignore")

app = Flask(__name__, template_folder='view', static_folder='./result')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # ここを修正
app.config['SECRET_KEY'] = 'your-secret-key'

# dbを初期化
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # ログインが必要な場合にリダイレクトする先のエンドポイント

DP = department()
QT = question()
CH = check()
SB = submit()
GR = graph()
HS = history()

# セッションでdatetime.now().date()を管理
@app.before_request
def before_request():
    session['current_date'] = datetime.now().strftime('%Y.%m.%d')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def top():

    return render_template('top.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 現在のユーザーが有効な権限を保持している(ログインしている)場合
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        user = User.query.filter_by(email=email).first()

        if check_password_hash(user.password, password):
            next_page = request.args.get('next')  # ログイン前にアクセスしようとしていたページ
            login_user(user)
            return redirect(next_page or url_for('dashboard'))

        else:
            return redirect(url_for('login'))

    return render_template('login.html')



from sqlalchemy.exc import IntegrityError

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return render_template('register.html', error='Email already exists. Please choose another email.')

        new_user = User(email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()  # Rollback the transaction in case of an IntegrityError
            return render_template('register.html', error='Error creating user. Please try again.')

    return render_template('register.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    try:
        universities = DP.departmentmaker(current_user.email)
    except:
        with open('error4.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(sys.exc_info())
            writer.writerow(str(sys.exc_info()[-1].tb_lineno))
    print(universities)
    return render_template('dashboard.html', email=current_user.email, universities=universities)


@app.route('/question1', methods=['GET', 'POST'])
@login_required
def question1():
    japan_timezone = pytz.timezone('Asia/Tokyo')
    session['start_time'] = datetime.now(japan_timezone)

    # タプルから辞書に変換
    output_data = dict(request.form)

    if request.method == 'POST':
        university = request.form.get('university')
        grade = request.form.get('grade')
        department = request.form.get('department')

        user_info = UserInfo(user_id=current_user.id, university=university, grade=grade, department=department, date_added=session['current_date'])

        session['university'] = user_info.university
        session['grade'] = user_info.grade
        session['department'] = user_info.department

    global USER_INFO
    USER_INFO = dict()
    USER_INFO['email'] = current_user.email
    USER_INFO['university'] = session['university']
    USER_INFO['grade'] = session['grade']
    USER_INFO['department'] = session['department']

    if request.method == 'POST':
        question_dict = QT.questionmaker(1, {}, USER_INFO)

    elif request.method == 'GET':

        for key in output_data.keys():
            session[key] = output_data[key]

        # GETリクエストの場合、セッション変数から値を取得
        skills = {f'skill{i}': session.get(f'skill{i}', '') for i in range(1, 16)}
        question_dict = QT.questionmaker(1, skills, USER_INFO)

    all_dict = {**question_dict, **USER_INFO}

    return render_template('question1.html', all_dict=all_dict)

@app.route('/question2', methods=['GET', 'POST'])
@login_required
def question2():

    # タプルから辞書に変換
    output_data = dict(request.form)
    for key in output_data.keys():
        session[key] = output_data[key]

    global USER_INFO
    USER_INFO = dict()
    USER_INFO['email'] = current_user.email
    USER_INFO['university'] = session['university']
    USER_INFO['grade'] = session['grade']
    USER_INFO['department'] = session['department']

    if request.method == 'POST':
        question_dict = QT.questionmaker(2, {}, USER_INFO)

    elif request.method == 'GET':

        for key in output_data.keys():
            session[key] = output_data[key]

        # GETリクエストの場合、セッション変数から値を取得
        skills = {f'skill{i}': session.get(f'skill{i}', '') for i in range(16, 31)}
        question_dict = QT.questionmaker(2, skills, USER_INFO)

    all_dict = {**question_dict, **USER_INFO}

    return render_template('question2.html', all_dict=all_dict)

@app.route('/question3', methods=['GET', 'POST'])
@login_required
def question3():

    # タプルから辞書に変換
    output_data = dict(request.form)
    for key in output_data.keys():
        session[key] = output_data[key]

    global USER_INFO
    USER_INFO = dict()
    USER_INFO['email'] = current_user.email
    USER_INFO['university'] = session['university']
    USER_INFO['grade'] = session['grade']
    USER_INFO['department'] = session['department']

    if request.method == 'POST':
        question_dict = QT.questionmaker(3, {}, USER_INFO)

    elif request.method == 'GET':

        for key in output_data.keys():
            session[key] = output_data[key]

        # GETリクエストの場合、セッション変数から値を取得
        skills = {f'skill{i}': session.get(f'skill{i}', '') for i in range(31, 45)}
        question_dict = QT.questionmaker(3, skills, USER_INFO)

    all_dict = {**question_dict, **USER_INFO}

    return render_template('question3.html', all_dict=all_dict)

@app.route('/question4', methods=['GET', 'POST'])
@login_required
def question4():

    # タプルから辞書に変換
    output_data = dict(request.form)
    for key in output_data.keys():
        session[key] = output_data[key]

    global USER_INFO
    USER_INFO = dict()
    USER_INFO['email'] = current_user.email
    USER_INFO['university'] = session['university']
    USER_INFO['grade'] = session['grade']
    USER_INFO['department'] = session['department']

    if request.method == 'POST':
        question_dict = QT.questionmaker(4, {}, USER_INFO)

    elif request.method == 'GET':

        for key in output_data.keys():
            session[key] = output_data[key]

        # GETリクエストの場合、セッション変数から値を取得
        skills = {f'skill{i}': session.get(f'skill{i}', '') for i in range(45, 67)}
        question_dict = QT.questionmaker(4, skills, USER_INFO)

    all_dict = {**question_dict, **USER_INFO}

    return render_template('question4.html', all_dict=all_dict)

@app.route('/check', methods=['GET', 'POST'])
@login_required
def check():
    # タプルから辞書に変換
    output_data = dict(request.form)

    for key, value in output_data.items():
        session[key] = value

    skills = {}

    for i in range(1, 67):
        skills[f'skill{i}'] = session.get(f'skill{i}', '')

    USER_INFO = dict()
    USER_INFO['user_id'] = current_user.id
    USER_INFO['email'] = current_user.email
    USER_INFO['university'] = session['university']
    USER_INFO['grade'] = session['grade']
    USER_INFO['department'] = session['department']

    question_dict = CH.checkmaker(USER_INFO, skills)
    session["universities"] = question_dict["universities"]
    session["categories"] = question_dict["categories"]

    return render_template('check.html', question_dict=question_dict)

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    # 日本時間の取得
    japan_timezone = pytz.timezone('Asia/Tokyo')
    session['end_time'] = datetime.now(japan_timezone)
    print(session['end_time'], session['start_time'])
    elapsed_time = session['end_time'] - session['start_time']
    session['total_seconds'] = int(elapsed_time.total_seconds())

    USER_INFO = dict()
    USER_INFO['user_id'] = current_user.id
    USER_INFO['email'] = current_user.email
    USER_INFO['university'] = session['university']
    USER_INFO['grade'] = session['grade']
    USER_INFO['department'] = session['department']
    USER_INFO['date'] = session['current_date']


    # タプルから辞書に変換
    output_data = dict(request.form)

    skills = {}
    for key, value in output_data.items():
        session[key] = value

        if "skill" in key:
            skills[key] = value

    # 同じ日付のデータを検索
    existing_data_info = UserInfo.query.filter_by(user_id=current_user.id, date_added=session['current_date']).first()
    existing_data_skill = UserSkill.query.filter_by(user_id=current_user.id, date_added=session['current_date']).first()

    # 同じ日付のデータが存在する場合は削除
    # 同じ日付のデータが存在する場合は削除
    # print(f"existing_data_info:{existing_data_info}")
    if existing_data_info:
        db.session.delete(existing_data_info)
        db.session.commit()

    user_info = UserInfo(user_id=current_user.id, university=session['university'], grade=session['grade'], department=session['department'], date_added=session['current_date'])
    db.session.add(user_info)
    db.session.commit()

    # 同じ日付のデータが存在する場合は削除
    # print(f"existing_data_skill:{existing_data_skill}")
    if existing_data_skill:
        db.session.delete(existing_data_skill)
        db.session.commit()

    # データベースに保存
    user_skill = UserSkill(user_id=current_user.id, date_added=session['current_date'], **skills)
    db.session.add(user_skill)
    db.session.commit()

    submit_dict = SB.csv_to_json(USER_INFO, {"universities": session["universities"], "categories": session["categories"]})

    return render_template('submit.html', submit_dict=submit_dict)


@app.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():

    # 同じ日付のデータを検索
    existing_data_anketo = UserAnketo.query.filter_by(user_id=current_user.id, date_added=session['current_date']).first()
    if existing_data_anketo:
        db.session.delete(existing_data_anketo)
        db.session.commit()

    seconds_to_minutes_and_seconds = lambda seconds: divmod(seconds, 60)
    minutes, seconds = seconds_to_minutes_and_seconds(session['total_seconds'])
    time = f"{minutes}分{seconds}秒"
    return render_template('questionnaire.html', time=time)

@app.route('/finish', methods=['GET', 'POST'])
@login_required
def finish():

    question_column_mapping = {
        "question1": "qualification_status",
        "question2": "ease_of_question_understanding",
        "question3": "ease_of_answer_providing",
        "question4": "current_knowledge_and_skills",
        "question5": "knowledge_and_skills_at_graduation",
        "question6": "improvement_prediction",
        "question7": "comment",
    }
    answers = {}

    # タプルから辞書に変換
    output_data = dict(request.form)

    for key, value in output_data.items():
        session[key] = value
        answers[question_column_mapping[key]] = value

    # データベースに保存
    user_answer = UserAnketo(user_id=current_user.id, date_added=session['current_date'], grade=session["grade"], required_time_seconds=session['total_seconds'], **answers)
    db.session.add(user_answer)
    db.session.commit()

    return render_template('finish.html')

@app.route('/selectUniversity', methods=['GET', 'POST'])
@login_required
def selectUniversity():

    if 'university' in request.form:
        # 'university'がフォームから送信された場合の処理
        session['university'] = request.form.get('university')
        return redirect(url_for('history'))
    else:
        # 'university'がフォームから送信されていない場合の処理
        universities = DP.departmentmaker(current_user.email)
        return render_template('selectUniversity.html', email=current_user.email, universities=universities)



@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():

    USER_INFO = dict()
    USER_INFO['user_id'] = current_user.id
    USER_INFO['email'] = current_user.email
    USER_INFO['university'] = session['university']

    submit_dict = HS.csv_to_json(USER_INFO)

    return render_template('history.html', submit_dict=submit_dict)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)
