# Flaskのインポート
from flask import Flask

# init_dbのインポート
from lib.db import init_db

# Flaskのアプリケーション本体を作成して、変数appに代入
app = Flask(__name__)

# 「config.py」を設定ファイルとして扱う
app.config.from_object('shopping.config')
# libフォルダ配下の「config.py」を共通設定ファイルとして扱う
app.config.from_object('lib.config')

# dbの設定
init_db(app)

# 「views.py」をインポート
from shopping.views import top, items, carts, orders

# itemアプリケーションを登録
app.register_blueprint(items.item, url_prefix='/items')
# cartアプリケーションを登録
app.register_blueprint(carts.cart, url_prefix='/carts')
# orderアプリケーションを登録
app.register_blueprint(orders.order, url_prefix='/orders')