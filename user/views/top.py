# flask関連のパッケージを取得
from flask import render_template, request, url_for, session, redirect, flash

# 「__init__.py」で宣言した変数appを取得
from shopping import app

# トップページを表示
@app.route('/')
def index():
  return render_template('top.html')