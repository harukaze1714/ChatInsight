# views/management_views.py
from models import db, User  # Userをインポート
from flask import request, jsonify, render_template, abort
from models import db, User, UserSummary,Message  # UserSummaryもインポート
from logic.create_summary import create_summary_logic  # 関数をインポート
from sqlalchemy import distinct
from logic.recreate_summary import  recreateSummaryLogic
from sqlalchemy import and_
from datetime import datetime
from sqlalchemy import extract, and_


def show_management_page():
    users = User.query.all()  # ユーザーを全て取得
    return render_template('management.html', users=users)  # 取得したユーザーをテンプレートに渡す


def show_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

def show_user_summary():
    userId = request.args.get('userId')
    month = request.args.get('month')

    summary = UserSummary.query.filter_by(user_id=userId, year_month=month).first()
    if summary:
        return jsonify({
            'frequentQuestions': summary.frequent_questions,
            'unresolvedIssues': summary.unresolved_issues,
            'chatCount': summary.chat_count
        })
    else:
        return jsonify({'message': 'Summary not found'}), 404
    
# 新しいビュー関数
def show_user_summary_months():
    user_id = request.args.get('userId')
    if user_id is None:
        return jsonify({"message": "User ID must be provided"}), 400

    months = db.session.query(distinct(UserSummary.year_month)).filter_by(user_id=user_id).all()

    if months:
        return jsonify({"months": [month[0] for month in months]}), 200
    else:
        return jsonify({"message": "No summary found for this user"}), 404

def create_summary():
    success, message = create_summary_logic()  # 関数を呼び出し
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 500



def recreate_summary():
   # userIdとmonthをリクエストから取得
    userId = request.args.get('userId')
    month = request.args.get('month')

    # userIdを整数に変換（エラーハンドリングが必要かもしれません）
    userId = int(userId)

    # month（YYYYMM形式）をdatetimeオブジェクトに変換
    dt_object = datetime.strptime(month, "%Y%m")

    # SQLAlchemyのqueryを修正
    chat_messages = Message.query.filter(
        and_(
            Message.user_id == userId,
            extract('year', Message.created_at) == dt_object.year,
            extract('month', Message.created_at) == dt_object.month
        )
    ).order_by(Message.created_at).all()

    text, frequentQuestions, unresolvedIssues = recreateSummaryLogic(chat_messages)

     # 仮定：UserSummaryにはuser_idとmonthがユニークキーとなっている
    user_summary = UserSummary.query.filter_by(user_id=userId, year_month=month).first()
    if user_summary:
        user_summary.frequent_questions = frequentQuestions
        user_summary.unresolved_issues = unresolvedIssues
        db.session.commit()
        return jsonify({"success": True, "message": "サマリを再作成しました。"}), 200
    else:
        return jsonify({"success": False, "message": "該当のUserSummaryレコードが見つかりませんでした。"}), 404
