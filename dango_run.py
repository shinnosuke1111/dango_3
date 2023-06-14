# 「__init__.py」で宣言した変数appを取得
from user import app

# アプリケーションの起動
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5002, debug=True)
  # app.run()
