# flask関連のパッケージを取得
from flask import render_template, request, url_for, session, redirect, flash
# 「__init__.py」で宣言した変数appを取得
from user import app
# Itemモデルを取得
from lib.models import Account, Basic_information
# osを取得
import os
# SQLAlchemyを取得
from lib.db import db
# デコレーターに使用
from functools import wraps
ALLOWED_EXTENSIONS = set(['png','jpeg','gif', 'jpg'])
UPLOAD_FOLDER = './uploads'

# ログインチェック処理
def login_check(view):
  @wraps(view)
  def inner(*args, **kwargs):
    if not session.get('logged_in'):
      flash('ログインしてください', 'error')
      return redirect(url_for('user_login'))
    return view(*args, **kwargs)
  return inner

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def user_login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    account = Account.query.filter_by(email=email).first()
    if not account:
      flash('正しいメールアドレスとパスワードを入力して下さい。', 'error')
      return render_template('login.html')
    else:
      if account.password == password:
        session['logged_in'] = True
        session['account_id'] = account.account_id
        flash('ログインしました', 'success')
        return redirect(url_for('user_index'))
      else:
        flash('正しいパスワードを入力して下さい。', 'error')
        return render_template('login.html')
  elif session.get('logged_in'):
    return redirect(url_for('user_index'))
  else:
    return render_template('login.html')

# ログアウト
@app.route('/logout')
def user_logout():
  session.pop('logged_in', None)
  flash('ログアウトしました', 'success')
  return render_template('login.html')

# 従業員一覧(アカウント情報)を表示
@app.route('/users')
@login_check
def user_index():
  accounts = Account.query.order_by(Account.account_id.desc()).all()
  return render_template('users/top.html', accounts=accounts)
  
# 従業員詳細(基本情報)を表示
@app.route('/users/<int:account_id>')
@login_check
def user_show(account_id):
  account = Account.query.get(account_id)
  basic_information = Basic_information.query.get(account_id)
  file_name = f'{account.account_id}.jpg'
  check_path = os.path.join(app.static_folder, 'images', file_name)
  if os.path.isfile(check_path):
    file_path = f'/static/images/{file_name}'
  else:
    file_path = False
  return render_template('users/show.html', account=account, basic_information=basic_information, file_path=file_path)

# アカウント登録画面を表示(=user用)
@app.route('/users/new')
def user_new():
  return render_template('users/new.html')

# アカウント登録処理(=user用)
@app.route('/users/create', methods=['POST'])
def user_create():
  account = Account(
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
    return redirect(url_for('user_new'))
  flash('アカウントが作成されました', 'success')
  return render_template('users/basic_new.html')

# 基本情報登録画面を表示
@app.route('/users/basic_new')
def user_basic_new():
  return render_template('users/basic_new.html')

# 基本情報登録処理
@app.route('/users/basic_create', methods=['POST'])
def user_basic_create():
  basic_information = Basic_information(
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
    return redirect(url_for('user_basic_new'))
  flash('登録されました', 'success')
  return redirect(url_for('user_login'))

# 登録情報修正画面を表示
@app.route('/<int:account_id>/update')
@login_check
def user_edit(account_id):
  account = Account.query.get(account_id)
  basic_information = Basic_information.query.get(account_id)
  return render_template('users/update.html', account = account, basic_information = basic_information)

# 登録情報修正処理
@app.route('/<int:account_id>/edit', methods=['POST'])
@login_check
def user_update(account_id):
  account = Account.query.get(account_id)
  basic_information = Basic_information.query.get(account_id)
  account.email = request.form.get('email')
  account.password = request.form.get('password')
  account.name = request.form.get('name')
  account.ruby = request.form.get('ruby')
  account.dept = request.form.get('dept')
  account.group_name = request.form.get('group_name')
  account.year = request.form.get('year')
  basic_information.birth_month = request.form.get('birth_month')
  basic_information.birth_day = request.form.get('birth_day')
  basic_information.team = request.form.get('team')
  basic_information.hobby = request.form.get('hobby')
  basic_information.word = request.form.get('word')
  try:
    db.session.merge(account)
    db.session.merge(basic_information)
    db.session.commit()
  except:
    flash('入力した値を再度確認してください', 'danger')
    return redirect(url_for('user_edit'))
  flash('登録情報が更新されました', 'success')
  return redirect(url_for('user_index'))
@app.template_filter('staticfile')
def staticfile_filter(fname):
    path = os.path.join(app.root_path, 'static', fname)
    mtime =  str(int(os.stat(path).st_mtime))
    return '/static/' + fname + '?v=' + str(mtime)