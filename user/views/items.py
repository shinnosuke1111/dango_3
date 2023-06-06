# flask関連のパッケージを取得
from flask import render_template, request, url_for, session, redirect, flash, Blueprint

# Itemモデルを取得
from lib.models import Item, Category

# SQLAlchemyを取得
from lib.db import db

# Blueprintでitemアプリケーションを登録
item = Blueprint('item', __name__)

# 商品一覧を表示
@item.route('/')
def index():
  categories = Category.query.order_by(Category.id.desc()).all()
  items = Item.query.order_by(Item.id.desc())

  category_id = request.args.get('category_id') or ""

  if str.isdigit(category_id):
    items = items.filter(Item.category_id==category_id)
  return render_template('items/index.html', items=items, categories=categories)