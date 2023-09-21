# Full Path: CodeInsight/mock/v1/models/index_models.py

from datetime import datetime
from . import db

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', back_populates='chats')  # Relationship with the User model
    messages = db.relationship('Message', back_populates='chat')  # Relationship with the Message model



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)  # Foreign key to associate with a chat
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Foreign key to associate with a user, nullable for AI messages
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp of the message
    content = db.Column(db.String(500), nullable=False)  # Content of the message
    is_ai = db.Column(db.Boolean, default=False)  # Flag to determine if the message is from AI
    # Defining relationships
    chat = db.relationship('Chat', back_populates='messages')  # Relationship with the Chat model
    user = db.relationship('User', back_populates='messages')  # Relationship with the User model



