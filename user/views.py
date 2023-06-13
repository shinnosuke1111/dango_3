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
    if not session.get('logged_in'):
      flash('ログインしてください', 'error')
      return redirect(url_for('login'))    
    return view(*args, **kwargs)
  return inner


# 初回ログイン
@app.route('/first_login', methods=['GET', 'POST'])
def first_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        try:
            account = Account.query.filter_by(email=email).first()
            if account.password == password:
              login_user(account) 
              return render_template('users/basic_new.html')
        except:
            flash('正しいメールアドレスとパスワードを入力して下さい。')
            # get_flashed_messages()
            return redirect('/first_login')




# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        try:
            account = Account.query.filter_by(email=email).first()
            if account.password == password:
              login_user(account) 
              return redirect('/users')
        except:
            flash('正しいメールアドレスとパスワードを入力して下さい。')
            # get_flashed_messages()
            return render_template('login.html')


# ログアウト
@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('ログアウトしました', 'success')
  return redirect(url_for('login'))


# 従業員一覧(アカウント情報)を表示
@app.route('/users')
@login_check
def index():
  account = Account.query.order_by(Account.id.desc()).all()
  return render_template('users/top.html', account=account)


# 従業員詳細(基本情報)を表示
@app.route('/users/<int:id>')
@login_check
def show(basic_id):
  account = Account.query.get(account_id)
  basic_information = Basic_information.query.get(account_id)
  return render_template('users/show.html', basic_information=basic_information, account=account)


# アカウント登録画面を表示(=user用)
@app.route('/users/new')
@login_check
def new():
  return render_template('users/new.html')


# アカウント登録処理(=user用)
@app.route('/users/create', methods=['POST'])
@login_check
def create():
  account = Account(
    account_id = request.form.get('account_id'),
    email = request.form.get('email'),
    password = request.form.get('password'),
    name = request.form.get('name'),
    ruby = request.form.get('ruby'),
    dept = request.form.get('dept'),
    group_name = request.form.get('group_name'),
    year = request.form.get('year'))
  try:
    db.session.add(accounts)
    db.session.commit()
  except:
    flash('入力した値を再度確認してください', 'error')
    return redirect(url_for('new'))
  flash('アカウントが作成されました', 'success')
  return render_template('users/first.html')


# 基本情報登録画面を表示
@app.route('/users/new')
@login_check
def basic_new():
  return render_template('users/basic_new.html')


# 基本情報登録処理
@app.route('/users/create', methods=['POST'])
@login_check
def basic_create():
   basic_information = Basic_information(
    basic_id = request.form.get('basic_id'),
    account_id = request.form.get('account_id'),
    birth_month = request.form.get('birth_month'),
    birth_day = request.form.get('birth_day'),
    team = request.form.get('team'),
    hobby = request.form.get('hobby'),
    word = request.form.get('word'))
  try:
    db.session.add(accounts)
    db.session.commit()
  except:
    flash('入力した値を再度確認してください', 'error')
    return redirect(url_for('new'))
  flash('登録されました', 'success')
  return redirect(url_for('index'))


# 登録情報修正画面を表示
@app.route('/<int:id>/update')
@login_check
def edit(account_id):
  account = Account.query.get(account_id)
  basic_information = basic_information.query.get(account_id)
  return render_template('users/update.html', account = account, basic_information = basic_information, email=email, password=password, name=name, ruby=ruby, team=team, year=year, hobby=hobby, word=word)


# 登録情報修正処理
@app.route('/<int:id>/edit', methods=['POST'])
@login_check
def update(account_id):
  account = Account.query.get(account_id)
  basic_information = Basic_information(account_id)
  email = request.form.get('email')
  password = request.form.get('password')
  name = request.form.get('name')
  ruby = request.form.get('ruby')
  dept = request.form.get('dept')
  group_name = request.form.get('group_name')
  year = request.form.get('year')
  birth_month = request.form.get('birth_month')
  birth_day = request.form.get('birth_day')
  team = request.form.get('team')
  hobby = request.form.get('hobby')
  word = request.form.get('word')
  
  try:
    db.session.merge(item)
    db.session.commit()
  except:
    flash('入力した値を再度確認してください', 'danger')
    return redirect(url_for('edit'))
  flash('登録情報が更新されました', 'success')
  return redirect(url_for('show'))

@app.template_filter('staticfile')
def staticfile_filter(fname):
    path = os.path.join(app.root_path, 'static', fname)
    mtime =  str(int(os.stat(path).st_mtime))
    return '/static/' + fname + '?v=' + str(mtime)