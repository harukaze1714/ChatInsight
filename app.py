#app.py
from flask import Flask
from models import db
import views

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatapp.db'  # SQLiteデータベースの設定
db.init_app(app)
views.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # データベースとテーブルの作成
    app.run(debug=True)
