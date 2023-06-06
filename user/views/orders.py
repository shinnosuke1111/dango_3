# flask関連のパッケージを取得
from flask import render_template, request, url_for, session, redirect, flash, Blueprint

# Itemモデルを取得
from lib.models import Order, Customer, Item

# SQLAlchemyを取得
from lib.db import db

# Blueprintでitemアプリケーションを登録
order = Blueprint('order', __name__)

# 注文フォームを表示
@order.route('/new')
def new():
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
  return render_template('orders/new.html', cart_details=cart_details, total_price=total_price)

# 注文登録
@order.route('/create', methods=['POST'])
def create():
  # 送信情報を取得
  name = request.form.get('name')
  address = request.form.get('address')
  tel = request.form.get('tel')
  email = request.form.get('email')


  # 顧客の作成
  if name and address and tel and email:
    customer = Customer(
      name = request.form.get('name'),
      address = request.form.get('address'),
      tel = request.form.get('tel'),
      email = request.form.get('email')
    )
    db.session.add(customer)
    db.session.commit()
  else:
    flash('顧客情報を入力してください', 'error')
    return redirect(url_for('order.new'))


  # 注文の作成
  cart = session.get('cart')
  for item_id, item_num in cart.items():
    item = Item.query.get(int(item_id))
    item_num = int(item_num)
    order = Order(
      customer_id=customer.id,
      item_id=item.id,
      item_num=item_num,
      total_price=item.price * item_num
    )
    db.session.add(order)
    db.session.commit()
  session.pop('cart', None)

  flash('注文が完了しました', 'success') 
  return redirect(url_for('item.index'))