//static/script/top_script.js

document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signup-form');
    const loginForm = document.getElementById('login-form');

    signupForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const username = event.target[0].value;
      const password = event.target[1].value;
    
      try {
        const response = await fetch('/api/v1/users/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password })
        });
    
        const data = await response.json();
    
        if (response.ok) {
          localStorage.setItem('userID', data.userId); // userId を使用
          setTimeout(() => {
            window.location.href = '/index';
          }, 100);
        } else {
          alert('エラー: ' + data.message);
        }
        
      } catch (error) {
        console.error('ネットワークエラーまたはその他のエラー:', error);
      }
    });
    

    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const username = event.target[0].value;
      const password = event.target[1].value;
    
      try {
        const response = await fetch('/api/v1/users/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password })
        });
    
        const data = await response.json();
    
        if (response.ok) {
          localStorage.setItem('userID', data.userId); // userId を使用
          setTimeout(() => {
            window.location.href = '/index';
          }, 100);
        } else {
          alert('エラー: ' + data.message);
        }
        
      } catch (error) {
        console.error('ネットワークエラーまたはその他のエラー:', error);
      }
    });
  });