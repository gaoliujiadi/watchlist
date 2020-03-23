from flask import Flask
from flask import url_for,escape
from flask import render_template

import os
import sys
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:# 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SWLALCHEMY_TRACK_MODIFICATIONS'] = False#关闭对模型修改的监控
#在扩展类实例化前加载配置
db = SQLAlchemy(app)

class User(db.Model):# 表名将会是 user（自动生成，小写处理
    id = db.Column(db.Integer,primary_key=True)#主键
    name = db.Column(db.String(20))#名字

class Movie(db.Model):#表名将会是movie
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))#电影标题
    year = db.Column(db.String(4))#年份


import click

@app.cli.command()
def forge():
    '''Generate fake data.'''
    db.create_all()
    #全局的两个变量移动到此函数
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.route('/user/<name>')
def user_page(name):
	return 'User: %s' % escape(name)

@app.route('/test')
def test_url_for():
	print(url_for('hello'))
	print(url_for('user_page',name='greyli'))
	print(url_for('user_page',name='peter'))
	print(url_for('test_url_for'))
	print(url_for('test_url_for',num=2))
	return 'Test page'
'''
name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]
'''
@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
	return render_template('index.html',uesr = user,movies=movies)