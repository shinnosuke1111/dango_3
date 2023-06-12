# flask関連のパッケージを取得
from flask import render_template, request, url_for, session, redirect, flash




# 「__init__.py」で宣言した変数appを取得
from admin import app




# Itemモデルを取得
from lib.models import Account, Basic_information

import os




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
@app.route('/users')
@login_check
def index():
  accounts = Account.query.order_by(Account.account_id.desc()).all()
  return render_template('users/top.html', accounts=accounts)




# # 従業員詳細(基本情報)を表示
@app.route('/users/<int:account_id>')
@login_check
def show(account_id):
  account = Account.query.get(account_id)
  basic_information = Basic_information.query.get(account_id)
  return render_template('users/show.html', account=account, basic_information=basic_information)




# アカウント作成画面を表示(=admin用)
@app.route('/users/new')
@login_check
def new():
  return render_template('users/new.html')




# アカウント作成処理(=admin用)
@app.route('/users/create', methods=['POST'])
@login_check
def create():
  account = Account(
    # account_id = request.form.get('account_id'),
    email = request.form.get('email'),
    password = request.form.get('password'),
    name = request.form.get('name'),
    ruby = request.form.get('ruby'),
    dept = request.form.get('dept'),
    group_name = request.form.get('group_name'),
    year = request.form.get('year'))
  try:
    db.session.add(account)
    db.session.commit()
  except:
    flash('入力した値を再度確認してください', 'error')
    return redirect(url_for('new'))
  flash('アカウントが作成されました', 'success')
  return render_template('users/basic_new.html')




# 基本情報登録画面を表示
@app.route('/users/basic_new')
@login_check
def basic_new():
  return render_template('users/basic_new.html')




# 基本情報登録処理
@app.route('/users/basic_create', methods=['POST'])
@login_check
def basic_create():
  basic_information = Basic_information(
    # basic_id = request.form.get('basic_id'),
    # account_id = request.form.get('account_id'),
    birth_month = request.form.get('birth_month'),
    birth_day = request.form.get('birth_day'),
    team = request.form.get('team'),
    hobby = request.form.get('hobby'),
    word = request.form.get('word'))
  try:
    db.session.add(basic_information)
    db.session.commit()
  except:
    flash('入力した値を再度確認してください', 'error')
    return redirect(url_for('basic_new'))
  flash('基本情報が登録されました', 'success')
  return redirect(url_for('index'))




# 登録情報修正画面を表示
@app.route('/users/<int:account_id>/update')
@login_check
def edit(account_id):
  account = Account.query.get(account_id)
  basic_information = Basic_information.query.get(account_id)
  return render_template('users/update.html', account = account, basic_information = basic_information)


# 登録情報修正処理
@app.route('/users/<int:account_id>/edit', methods=['POST'])
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
    db.session.merge(account)
    db.session.merge(basic_information)
    db.session.commit()
  except:
    flash('入力した値を再度確認してください', 'danger')
    return redirect(url_for('edit'))
  flash('情報が更新されました', 'success')
  return redirect(url_for('show'))




# アカウント削除処理
@app.route('/users/<int:account_id>/delete', methods=['POST'])
@login_check
def delete(account_id):
  account =Account.query.get(account_id)
  basic_information = Basic_information(account_id)
  db.session.delete(accounts)
  db.session.delete(basic_information)
  db.session.commit()
  flash('商品が削除されました', 'success')
  return redirect(url_for('top'))

@app.template_filter('staticfile')
def staticfile_filter(fname):
    path = os.path.join(app.root_path, 'static', fname)
    mtime =  str(int(os.stat(path).st_mtime))
    return '/static/' + fname + '?v=' + str(mtime)