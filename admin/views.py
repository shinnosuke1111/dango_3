# flask関連のパッケージを取得
from flask import render_template, request, url_for, session, redirect, flash


# 「__init__.py」で宣言した変数appを取得
from admin import app


# Itemモデルを取得
from lib.models import Account, Basic_information


# SQLAlchemyを取得
from lib.db import db


# デコレーターに使用
from functools import wraps


# ログインチェック処理
def login_check(view):
  @wraps(view)
  def inner(*args, **kwargs):
    if not session.get('admin_logged_in'):
      flash('ログインしてください', 'error')
      return redirect(url_for('login'))    
    return view(*args, **kwargs)
  return inner


# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    if request.form.get('email') != app.config['ADMIN_USER_ID']:
      flash('ユーザIDが異なります', 'error')
    elif request.form.get('password') != app.config['ADMIN_PASSWORD']:
      flash('パスワードが異なります', 'error')
    else:
      session['admin_logged_in'] = True
      flash('ログインしました', 'success')
      return redirect(url_for('index'))
  return render_template('login.html')


# ログアウト
@app.route('/logout')
def logout():
  session.pop('admin_logged_in', None)
  flash('ログアウトしました', 'success')
  return redirect(url_for('login'))


# 従業員一覧(アカウント情報)を表示
@app.route('/items')
@login_check
def index():
  account = Account.query.order_by(Account.id.desc()).all()
  return render_template('items/top.html', account=account)


# 従業員詳細(基本情報)を表示
@app.route('/items/<int:id>')
@login_check
def show(account_id):
  account = Account.query.get(account_id)
  basic_information = Basic_information.query.get(account_id)
  return render_template('items/show.html', account=account, basic_information=basic_information, name=name, ruby=ruby, dept=dept, group=group, team=team, year=year, birth_month=birth_month, birth_day=birth_day, hobby=hobby, word=word)


# アカウント作成画面を表示(=admin用)
@app.route('/items/new')
@login_check
def new():
  return render_template('items/new.html')


# アカウント作成処理(=admin用)
@app.route('/items/create', methods=['POST'])
@login_check
def create():
  account = Account(
    account_id = request.form.get('account_id'),
    email = request.form.get('email'),
    password = request.form.get('password'),
    name = request.form.get('name'),
    ruby = request.form.get('ruby'),
    dept = request.form.get('dept'),
    group = request.form.get('group'),
    year = request.form.get('year'))
  try:
    db.session.add(account)
    db.session.commit()
  except:
    flash('入力した値を再度確認してください', 'error')
    return redirect(url_for('new'))
  flash('アカウントが作成されました', 'success')
  return render_template('items/basic_new.html')


# 基本情報登録画面を表示
@app.route('/items/new')
@login_check
def new():
  return render_template('items/basic_new.html')


# 基本情報登録処理
@app.route('/items/create', methods=['POST'])
@login_check
def create():
  basic_information = Basic_information(
    basic_id = request.form.get('basic_id'),
    account_id = request.form.get('account_id'),
    birth_month = request.form.get('birth_month'),
    birth_day = request.form.get('birth_day'),
    team = request.form.get('team'),
    hobby = request.form.get('hobby'),
    word = request.form.get('word'))
  try:
    db.session.add(account)
    db.session.commit()
  except:
    flash('入力した値を再度確認してください', 'error')
    return redirect(url_for('new'))
  flash('商品が作成されました', 'success')
  return redirect(url_for('index'))


# 登録情報修正画面を表示
@app.route('/<int:id>/update')
@login_check
def edit(account_id):
  account = Account.query.get(account_id)
  basic_information = basic_information.query.get(account_id)
  return render_template('items/update.html', account = account, basic_information = basic_information, email=email, password=password, name=name, ruby=ruby, team=team, year=year, hobby=hobby, word=word)


# 登録情報修正処理
@app.route('/<int:id>/edit', methods=['POST'])
@login_check
def update(account_id):
  account = Account.query.get(account_id)
  basic_information = Basic_information(account_id)
  email = request.form.get('email'),
  password = request.form.get('password'),
  name = request.form.get('name'),
  ruby = request.form.get('ruby'),
  dept = request.form.get('dept'),
  group = request.form.get('group'),
  year = request.form.get('year'),
  birth_month = request.form.get('birth_month'),
  birth_day = request.form.get('birth_day'),
  team = request.form.get('team'),
  hobby = request.form.get('hobby'),
  word = request.form.get('word')
  
  try:
    db.session.merge(item)
    db.session.commit()
  except:
    flash('入力した値を再度確認してください', 'danger')
    return redirect(url_for('edit'))
  flash('商品が更新されました', 'success')
  return redirect(url_for('show'))


# アカウント削除処理
@app.route('/<int:id>/delete', methods=['POST'])
@login_check
def delete(account_id):
  account =Account.query.get(account_id)
  basic_information = Basic_information(account_id)
  db.session.delete(account)
  db.session.delete(basic_information)
  db.session.commit()
  flash('商品が削除されました', 'success')
  return redirect(url_for('index'))