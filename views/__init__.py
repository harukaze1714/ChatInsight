# views/__init__.py

from flask import Blueprint
from .top_views import signup, login, show_top_page, init_app as top_views_init_app
from .index_views import show_index_page,manage_chats, manage_messages, ai_response,manage_user_chats
from .management_views import show_management_page,show_users,show_user_summary,create_summary,show_user_summary_months,recreate_summary

views_blueprint = Blueprint('views', __name__)

# エンドポイントの登録
views_blueprint.add_url_rule('/', view_func=show_top_page)  
views_blueprint.add_url_rule('/index', view_func=show_index_page)  
views_blueprint.add_url_rule('/api/v1/users/signup', view_func=signup, methods=['POST'])
views_blueprint.add_url_rule('/api/v1/users/login', view_func=login, methods=['POST'])

views_blueprint.add_url_rule('/api/ai/response', view_func=ai_response, methods=['POST'])
views_blueprint.add_url_rule('/api/chats', view_func=manage_chats, methods=['GET', 'POST'])
views_blueprint.add_url_rule('/api/users/<int:user_id>/chats/<int:chat_id>/messages', view_func=manage_messages, methods=['GET', 'POST'])  
views_blueprint.add_url_rule('/api/user_chats', view_func=manage_user_chats, methods=['GET', 'POST'])

# エンドポイントの登録
views_blueprint.add_url_rule('/management', view_func=show_management_page)  
# 新しいAPIエンドポイントを追加
views_blueprint.add_url_rule('/api/users', view_func=show_users, methods=['GET'])
views_blueprint.add_url_rule('/api/user_summary', view_func=show_user_summary, methods=['GET'])
# 新しいAPIエンドポイントを追加
views_blueprint.add_url_rule('/api/user_summary_months', view_func=show_user_summary_months, methods=['GET'])

# 新しいAPIエンドポイントを追加
views_blueprint.add_url_rule('/api/createSummary', view_func=create_summary, methods=['POST'])
views_blueprint.add_url_rule('/api/recreateSummary', view_func=recreate_summary, methods=['POST'])


def init_app(app):
    app.register_blueprint(views_blueprint)
    top_views_init_app(app)  # top_viewsのinit_appを呼び出してbcryptを初期化します
