# Flaskのインポート
from flask import Flask

# init_dbのインポート
from lib.db import init_db

# Flaskのアプリケーション本体を作成して、変数appに代入
app = Flask(__name__)

# 「config.py」を設定ファイルとして扱う
app.config.from_object('admin.config')
# libフォルダ配下の「config.py」を共通設定ファイルとして扱う
app.config.from_object('lib.config')

# dbの設定
init_db(app)

# 「views.py」をインポート
import admin.views