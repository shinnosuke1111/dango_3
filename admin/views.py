# flask関連のパッケージを取得
from flask import render_template, request, url_for, session, redirect, flash

# 「__init__.py」で宣言した変数appを取得
from admin import app

# Itemモデルを取得
from lib.models import Item, Category

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
    if request.form.get('user_id') != app.config['ADMIN_USER_ID']:
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

# 商品一覧を表示
@app.route('/items')
@login_check
def index():
  items = Item.query.order_by(Item.id.desc()).all()
  return render_template('items/index.html', items=items)

# 商品詳細を表示
@app.route('/items/<int:id>')
@login_check
def show(id):
  item = Item.query.get(id)
  return render_template('items/show.html', item=item)

# 商品作成画面を表示
@app.route('/items/new')
@login_check
def new():
  categories = Category.query.all()
  return render_template('items/new.html', categories=categories)

# 商品作成処理
@app.route('/items/create', methods=['POST'])
@login_check
def create():
  item = Item(
    name=request.form.get('name'),
    category_id=request.form.get('category_id'),
    price=request.form.get('price'),
  )
  try:
    db.session.add(item)
    db.session.commit()
  except: 
    flash('入力した値を再度確認してください', 'error')
    return redirect(url_for('new'))
  flash('商品が作成されました', 'success')
  return redirect(url_for('index'))

# 商品更新画面を表示
@app.route('/<int:id>/edit')
@login_check
def edit(id):
  item = Item.query.get(id)
  categories = Category.query.all()
  return render_template('items/edit.html', item=item, categories=categories)

# 商品更新処理
@app.route('/<int:id>/update', methods=['POST'])
@login_check
def update(id):
  item = Item.query.get(id)
  item.name = request.form.get('name')
  item.category_id = request.form.get('category_id')
  item.price = request.form.get('price')
  try:
    db.session.merge(item)
    db.session.commit()
  except: 
    flash('入力した値を再度確認してください', 'danger')
    return redirect(url_for('new'))
  flash('商品が更新されました', 'success')
  return redirect(url_for('index'))

# 商品削除処理
@app.route('/<int:id>/delete', methods=['POST'])
@login_check
def delete(id):
  item = Item.query.get(id)
  db.session.delete(item)
  db.session.commit()
  flash('商品が削除されました', 'success')
  return redirect(url_for('index'))