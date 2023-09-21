from models import db, Message, UserSummary
from sqlalchemy import func

def create_summary_logic():
    try:
        message_data = db.session.query(
            Message.user_id,
            func.strftime("%Y%m", Message.created_at),
            func.count(Message.id)
        ).group_by(Message.user_id, func.strftime("%Y%m", Message.created_at)).all()

        for user_id, year_month, chat_count in message_data:
            existing_summary = UserSummary.query.filter_by(user_id=user_id, year_month=year_month).first()

            if existing_summary is None:
                new_summary = UserSummary(
                    user_id=user_id,
                    year_month=year_month,
                    frequent_questions="",
                    unresolved_issues="",
                    chat_count=chat_count
                )
                db.session.add(new_summary)

        db.session.commit()
        return True, "Summaries created successfully"

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return False, "Error while creating summaries"
