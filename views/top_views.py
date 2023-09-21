#viwes/top_views.py
from flask import request, jsonify, render_template
from models import db, User

# bcryptをインポートします（bcryptがまだインポートされていない場合）
from flask_bcrypt import Bcrypt
# bcryptインスタンスを作成します（appインスタンスが必要）

bcrypt = Bcrypt()

def init_app(app):
    bcrypt.init_app(app)

def show_top_page():
    return render_template('top.html')

def signup():
    data = request.get_json()

    # ユーザー名とパスワードのバリデーション
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'ユーザー名とパスワードを提供してください'}), 400

    # ユーザー名が既に存在するかどうかを確認
    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({'message': 'ユーザー名が既に存在します'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'アカウントが正常に作成されました', 'userId': new_user.id}), 201


def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'ユーザー名とパスワードを提供してください'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        # ここでトークンを生成し、フロントエンドに送信できます
        return jsonify({'message': 'ログイン成功', 'userId': user.id}), 200

    return jsonify({'message': '無効なユーザー名またはパスワード'}), 400