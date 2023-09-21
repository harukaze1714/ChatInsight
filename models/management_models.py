# Full Path: CodeInsight/mock/v1/models/top_models.py
from . import db
from .index_models import Chat
from sqlalchemy import text
from datetime import datetime


class UserSummary(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    year_month = db.Column(db.String(6), nullable=False)  # YYYYMM format
    frequent_questions = db.Column(db.Text)
    unresolved_issues = db.Column(db.Text)
    chat_count = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)