from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .top_models import User
from .index_models import Chat, Message
from .management_models import UserSummary