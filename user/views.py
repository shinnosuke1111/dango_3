# flask関連のパッケージを取得
from flask import render_template, request, url_for, session, redirect, flash
# 「__init__.py」で宣言した変数appを取得
from user import app
# Itemモデルを取得
from lib.models import Account, Basic_information, Message
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
@app.route('/', methods=['GET', 'POST'])
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
        session['name'] = account.name
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
  messages = Message.query.order_by(Message.tweet_id.desc()).all()
  accounts = Account.query.order_by(Account.account_id.desc()).all()
  return render_template('users/top.html', accounts=accounts, messages=messages)
  
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

#画像拡張子確認
def allwed_file(filename):
  return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# ファイルを受け取る方法の指定
@app.route('/', methods=['GET', 'POST'])
def user_uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        # データの取り出し
        file = request.files['file']
        # ファイル名がなかった時の処理
        if file.filename == "":
            flash('ファイルがありません')
            return redirect(request.url)
        # ファイルのチェック
        if file and allwed_file(file.filename):
            # 危険な文字を削除（サニタイズ処理）
            filename = secure_filename(file.filename)
            # ファイルの保存
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # アップロード後のページに転送
            return redirect(url_for('uploaded_file', filename=filename))
@app.route('/upload', methods=['GET', 'POST'])
def user_upload():
    if request.method == 'GET':
      return render_template('upload.html')
    elif request.method == 'POST':
      account_id = request.form.get('account_id')
      file = request.files['example']
      account = Account.query.get(account_id)
      if str('.jpg') in file.filename:
        filename = (f'{account.account_id}.jpg')
      elif str('.png') in file.filename:
        filename = (f'{account.account_id}.png')
      elif str('.jpeg') in file.filename:
        filename = (f'{account.account_id}.jpeg')
      elif str('.gif') in file.filename:
        filename = (f'{account.account_id}.gif')
      else:
        flash('指定された拡張子の画像を選択してください', 'error')
        return render_template('update.html')
      file.save(os.path.join(app.static_folder, 'images', filename))
      return redirect(url_for('user_uploaded_file', filename=filename))
# アップロード完了画面を表示
@app.route('/uploaded_file/<string:filename>')
def user_uploaded_file(filename):
    flash('画像が更新されました', 'success')
    return redirect(url_for('user_index'))

@app.route("/tubuyaki/result", methods=['POST'])
def tubuyaki_result():
  if request.method == 'POST':
    message = Message(
      name = request.form.get('name'),
      message = request.form.get('message')
      )
    db.session.add(message)
    db.session.commit()
    flash('投稿が完了しました', 'success')
    return redirect(url_for('user_index'))
  else:
    pass

    # つぶやきの削除
# @app.route('/users/delete/<int:tweet_id>', methods=['POST'])
# @login_check
# def tubuyaki_delete(tweet_id):
#   print(tweet_id)

# つぶやきの削除
@app.route('/users/<int:tweet_id>/delete', methods=['POST'])
@login_check
def tubuyaki_delete(tweet_id):
  message = Message.query.get(tweet_id)
  db.session.delete(message)
  db.session.commit()
  flash('投稿が削除されました', 'success')
  return redirect(url_for('user_index'))[]