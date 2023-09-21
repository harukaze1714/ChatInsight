#views/index_views.py

from models import db, Chat,Message
from logic.index_logic import get_ai_response
from flask import request, jsonify, render_template, abort
from datetime import datetime

def show_index_page():
    return render_template('index.html')

def manage_chats():
    user_id = request.args.get('userID')
    
    if request.method == 'GET':
        if user_id:
            chats = Chat.query.filter_by(user_id=user_id).all()
            return jsonify([{'id': c.id, 'chat_name': c.chat_name, 'userId': c.user_id, 'createdAt': c.created_at} for c in chats]), 200
        else:
            return jsonify({'message': 'User ID not provided'}), 400
    else: # POST
        data = request.get_json()
        new_chat = Chat(chat_name=data['chat_name'], user_id=data['userID'])
        db.session.add(new_chat)
        db.session.commit()
        return jsonify({'message': 'Chat created', 'chatId': new_chat.id}), 201


def manage_messages(user_id, chat_id):
    if request.method == 'GET':
        messages = Message.query.filter_by(user_id=user_id, chat_id=chat_id).all()
        return jsonify([{'id': m.id, 'content': m.content, 'userId': m.user_id, 'createdAt': m.created_at, 'is_ai': m.is_ai} for m in messages]), 200  
    else:  # POST
        data = request.get_json()
        user_message_content = data.get('content')

        if user_message_content:
            user_message = Message(chat_id=chat_id, content=user_message_content, user_id=user_id, is_ai=False)
            db.session.add(user_message)

            ai_response_message_content = get_ai_response(user_message_content)
            
            ai_response_message = Message(chat_id=chat_id, content=ai_response_message_content, user_id=user_id, is_ai=True)
            db.session.add(ai_response_message)

            db.session.commit()

            return jsonify({
                'message': 'Message exchanged', 
                'userMessageId': user_message.id, 
                'aiMessageId': ai_response_message.id,
                'aiResponse': ai_response_message_content
            }), 201
        else:
            return jsonify({'message': 'Message content not provided'}), 400


def manage_user_chats():
    if request.method == 'GET':
        user_id = request.args.get('userID')
        if user_id:
            # Get all chats associated with the user ID
            chats = Chat.query.filter_by(user_id=user_id).all()
            return jsonify([{'id': c.id, 'chat_name': c.chat_name, 'createdAt': c.created_at} for c in chats]), 200
        else:
            return jsonify({'message': 'User ID not provided'}), 400

    elif request.method == 'POST':
        data = request.get_json()
        user_id = data.get('userID')  # POSTデータからuserIDを取得
        if user_id and 'chat_name' in data:
            # Create a new chat associated with the user ID
            new_chat = Chat(chat_name=data['chat_name'], user_id=user_id, created_at=datetime.utcnow())
            db.session.add(new_chat)
            db.session.commit()
            return jsonify({'message': 'Chat created successfully', 'chatId': new_chat.id}), 201
        else:
            return jsonify({'message': 'User ID or Chat name not provided'}), 400

def ai_response():
    data = request.get_json()
    user_message = data.get('message')

    if user_message:
        ai_response_message = get_ai_response(user_message)
        return jsonify({'message': 'AI response', 'response': ai_response_message}), 200
    else:
        return jsonify({'message': 'Message not provided'}), 400
