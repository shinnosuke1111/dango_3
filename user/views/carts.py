# flask関連のパッケージを取得
from flask import render_template, request, url_for, session, redirect, flash, Blueprint

# Itemモデルを取得
from lib.models import Item

# SQLAlchemyを取得
from lib.db import db

# Blueprintでcartアプリケーションを登録
cart = Blueprint('cart', __name__)

# カートを表示
@cart.route('/')
def index():
  cart = session.get('cart')
  # カートの情報を表示用に加工する
  cart_details = list()
  total_price = 0
  if type(cart) is dict:
    for item_id, item_num in cart.items():
      item = Item.query.get(int(item_id)) # 商品
      item_num = int(item_num) # 個数
      sub_total_price = item.price * item_num # 小計
      cart_details.append({'item': item, 'item_num': item_num, 'sub_total_price': sub_total_price})
      total_price += sub_total_price
  return render_template('carts/index.html', cart_details=cart_details, total_price=total_price)

# カート登録処理
@cart.route('/create', methods=['POST'])
def create():
  # 値を取得
  item_id = request.form.get('item_id') or ""
  item_num = request.form.get('item_num') or ""

  # 送信された値が数字かどうかチェック
  if not(str.isdigit(item_id) and str.isdigit(item_num)): 
    flash('数値を入力してください', 'error')
    return redirect(url_for('item.index'))

  # item_idが存在するかどうかチェック
  if Item.query.get(int(item_id)) == None:
    flash('対象の商品はありません', 'error')
    return redirect(url_for('item.index'))
  
  # cartに追加
  cart = session.get('cart')
  if type(cart) is dict:
    origin_item_num = cart.get(item_id) or 0
    cart[item_id] = origin_item_num + int(item_num)
  else:
    cart = {item_id: int(item_num)}
  session['cart'] = cart

  flash('カートに登録しました', 'success')
  return redirect(url_for('item.index'))

# カート削除処理
@cart.route('/<string:item_id>/delete', methods=['POST'])
def delete(item_id):
  if item_id == 'all':
    session.pop('cart', None)
  else:
    cart = session.get('cart')
    cart.pop(item_id, None)
    session['cart'] = cart
  flash('商品がカートから削除されました', 'success')
  return redirect(url_for('cart.index'))