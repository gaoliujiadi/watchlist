# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_moment import Moment

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),os.getenv('DATABASE_FILE','data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False#关闭对模型修改的监控
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','dev')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
moment = Moment(app)

@login_manager.user_loader
def load_user(user_id):#创建用户加载回调函数，接受用户ID作为参数
    user = User.query.get(int(user_id))#用ID作为User模型的主键查询对应的用户
    return user

login_manager.login_view = 'login'

@app.context_processor
def inject_user():
	from watchlist.models import User
	user = User.query.first()
	return dict(user=user)

from watchlist import views, errors, commands
from watchlist import app, db
from watchlist.models import User, Movie,Message