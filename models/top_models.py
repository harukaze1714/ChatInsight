# Full Path: CodeInsight/mock/v1/models/top_models.py
import string
import random
from sqlalchemy import event
from . import db
from .index_models import Chat
from sqlalchemy import text
from datetime import datetime
from . import db


class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_identifier = db.Column(db.String(8), unique=True, nullable=False, default=lambda: generate_user_identifier())
    chats = db.relationship('Chat', back_populates='user', lazy=True)  # One-to-Many relationship with the Chat model
    messages = db.relationship('Message', back_populates='user')  # Relationship with the Message model

def generate_user_identifier(size=8, chars=string.ascii_letters + string.digits):
    """ランダムな8桁の英数字の識別IDを生成します"""
    return ''.join(random.choice(chars) for _ in range(size))

# top_models.py
def create_chat_after_user(mapper, connection, target):
    stmt = text("""
        INSERT INTO chat (user_id, chat_name, created_at) 
        VALUES (:user_id, :chat_name, :created_at)
    """)
    connection.execute(stmt, {'user_id': target.id, 'chat_name': "デフォルトのチャット", 'created_at': datetime.utcnow()})
    
    # 最後に挿入された行のIDを取得
    result = connection.execute(text("SELECT last_insert_rowid()"))
    chat_id = result.fetchone()[0]
    print("result: ", result, "chat_id: ", chat_id)


     # メッセージを挿入
    stmt = text("""
        INSERT INTO message (chat_id, user_id, content, created_at, is_ai) 
        VALUES (:chat_id, :user_id, :content, :created_at, :is_ai)
    """)

    connection.execute(stmt, {'chat_id': chat_id, 'user_id': target.id, 'content': "ようこそ新しいチャットへ！", 'created_at': datetime.utcnow(), 'is_ai': True})
    
event.listen(User, 'after_insert', create_chat_after_user)

# top_models.py または index_models.py にこの関数を追加します
def create_message_after_chat(mapper, connection, target):
    stmt = text("""
        INSERT INTO message (chat_id, content, created_at) 
        VALUES (:chat_id, :content, :created_at)
    """)

    connection.execute(stmt, {'chat_id': target.id, 'content': "ようこそ新しいチャットへ！", 'created_at': datetime.utcnow()})

event.listen(Chat, 'after_insert', create_message_after_chat)
