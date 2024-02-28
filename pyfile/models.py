from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_added = db.Column(db.String(15))
    university = db.Column(db.String(100))
    grade = db.Column(db.String(10))
    department = db.Column(db.String(100))

class UserAnketo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_added = db.Column(db.String(15))
    grade = db.Column(db.String(10))
    required_time_seconds = db.Column(db.Integer, nullable=False)
    qualification_status = db.Column(db.String(50), nullable=False)
    ease_of_question_understanding = db.Column(db.String(50), nullable=False)
    ease_of_answer_providing = db.Column(db.String(50), nullable=False)
    current_knowledge_and_skills = db.Column(db.String(50), nullable=False)
    knowledge_and_skills_at_graduation = db.Column(db.String(50), nullable=False)
    improvement_prediction = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(500), nullable=False)

class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_added = db.Column(db.String(15))
    # Dynamically create columns Q1 to Q66
    for i in range(1, 67):
        locals()[f'skill{i}'] = db.Column(db.String(10))



