# DB操作に必要なパッケージを取得
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# db定義
db = SQLAlchemy()

# modelsはdb定義の後に記述する
import lib.models

def init_db(app):
    db.init_app(app)
    Migrate(app, db)