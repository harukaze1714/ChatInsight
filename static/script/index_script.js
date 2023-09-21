window.onload = async () => {
  // ローカルストレージからユーザーIDを取得
  const userID = localStorage.getItem('userID');

  if (!userID) {
    alert("ユーザーIDが見つかりません。再度ログインしてください。");
    window.location.href = '/'; // or any other login URL
    return;
  }

  // DOM要素の取得
  const chatList = document.getElementById('chat-list');
  const chatHistory = document.getElementById('chat-history');
  const messageInput = document.getElementById('message-input');
  const sendButton = document.getElementById('send-button');
  const addChatButton = document.getElementById('add-chat-button');
  // マネジメントページへの遷移ボタンを取得
  const manageButton = document.getElementById("manage-button");

  let activeChatID = null;

  async function loadUserChats(userID) {
    try {
      chatList.innerHTML = ''; // リストをクリア
      const response = await fetch(`/api/user_chats?userID=${userID}`);
      const userChats = await response.json();

      console.log(`/api/user_chats?userID=${userID}`);
      console.log('userChats:', userChats);
      userChats.forEach(chat => {
        const chatItem = document.createElement('li');
        chatItem.setAttribute('data-chat-id', chat.id);
        chatItem.textContent = chat.chat_name;
        chatList.appendChild(chatItem);
      });
    } catch (error) {
      console.error('Error loading user chats:', error);
    }
    const firstChatItem = document.querySelector('#chat-list li');
    if (firstChatItem) {
      activeChatID = firstChatItem.getAttribute('data-chat-id');
      loadMessages(userID, activeChatID);
    }
    // ボタンがクリックされたら、マネジメントページへ遷移する
    manageButton.addEventListener("click", function () {
      window.location.href = "/management";
    });
  }


  async function loadMessages(userID, chatID) {
    try {
      const response = await fetch(`/api/users/${userID}/chats/${chatID}/messages`);
      const messages = await response.json();

      chatHistory.innerHTML = '';
      console.log('messages:', messages);
      messages.forEach(message => {
        const messageDiv = document.createElement('div');

        // is_ai属性をもとにプレフィックスとクラスを決定
        const prefix = message.is_ai ? 'AI：' : 'あなた：';
        const cssClass = message.is_ai ? 'ai-message' : 'user-message';

        messageDiv.textContent = `${prefix} ${message.content}`;
        messageDiv.classList.add(cssClass); // クラスを追加

        chatHistory.appendChild(messageDiv);
      });
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  }

  addChatButton.addEventListener('click', async () => {
    const chatName = prompt('新しいチャットの名前を入力してください:');
    if (chatName) {
      try {
        const response = await fetch(`/api/user_chats`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ userID: userID, chat_name: chatName })
        });

        if (response.ok) {
          const result = await response.json();
          alert(result.message);
          // 新しく作成したチャットをロード
          loadUserChats(userID);
        } else {
          console.error('Error creating new chat:', await response.text());
        }
      } catch (error) {
        console.error('Error creating new chat:', error);
      }
    }
  });

  chatList.addEventListener('click', (event) => {
    if (event.target.tagName === 'LI') {
      activeChatID = event.target.getAttribute('data-chat-id');
      loadMessages(userID, activeChatID);
    }
  });

  sendButton.addEventListener('click', async () => {
    console.log('activeChatID:', activeChatID, 'messageInput.value:', messageInput.value);
    if (activeChatID && messageInput.value) {
      const userMessageDiv = document.createElement('div');
      userMessageDiv.textContent = `あなた： ${messageInput.value}`;
      userMessageDiv.classList.add('user-message');
      chatHistory.appendChild(userMessageDiv);

      const aiMessageDiv = document.createElement('div');
      aiMessageDiv.textContent = 'AI： 考え中...';
      aiMessageDiv.classList.add('ai-message');
      chatHistory.appendChild(aiMessageDiv);

      try {
        const response = await fetch(`/api/users/${userID}/chats/${activeChatID}/messages`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ userID: userID, content: messageInput.value })
        });

        if (response.ok) {
          messageInput.value = '';
          const responseData = await response.json();
          aiMessageDiv.textContent = `AI： ${responseData.aiResponse}`; // サーバから受け取ったAIのレスポンス
        } else {
          aiMessageDiv.textContent = 'AI： エラーが発生しました';
          console.error('Error sending message:', await response.text());
        }
      } catch (error) {
        aiMessageDiv.textContent = 'AI： エラーが発生しました';
        console.error('Error sending message:', error);
      }
    }
  });



  await loadUserChats(userID); // ユーザーIDを引数としてloadUserChatsを呼び出します
};
