from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# ============================================================
#  YAHAN APNI GROQ API KEY PASTE KAREIN (Quotes ke andar)
# ============================================================
GROQ_API_KEY = "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"
# ============================================================

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """Aap AliBot hain, ek friendly aur smart assistant hain jo Ali Arsh Khan ne Python se banaya hai.
Aap Urdu aur English dono mein baat kar sakte hain. Jawab hamesha chhota aur clear rakhein (2-3 lines se zyada nahi)."""

chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

def ask_groq(user_message):
    chat_history.append({"role": "user", "content": user_message})
    messages_to_send = [chat_history[0]] + chat_history[-10:]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    data = {
        "model": MODEL,
        "messages": messages_to_send,
        "temperature": 0.7,
        "max_tokens": 300
    }
    try:
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=20)
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            chat_history.append({"role": "assistant", "content": answer})
            return answer
        else:
            return f"Error {response.status_code}"
    except:
        return "Internet check karein."

# ============ HTML PAGE (App ka Design) ============
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AliBot - Made by Ali Arsh Khan</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            height: 100dvh; display: flex; justify-content: center; align-items: center;
        }
        .app {
            width: 100%; max-width: 480px; height: 100vh; 
            background: #0d0d15; display: flex; flex-direction: column;
            box-shadow: 0 0 40px rgba(100, 100, 255, 0.3);
        }
        .header {
            background: linear-gradient(90deg, #667eea, #764ba2);
            padding: 15px 20px; display: flex; align-items: center; gap: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }
        .avatar {
            width: 45px; height: 45px; border-radius: 50%;
            background: #fff; display: flex; align-items: center; justify-content: center;
            font-size: 24px;
        }
        .header-info h2 { color: #fff; font-size: 17px; }
        .header-info p { color: #d0d0ff; font-size: 12px; }
        .chat-area {
            flex: 1; overflow-y: auto; padding: 15px;
            background: #0d0d15; display: flex; flex-direction: column; gap: 10px;
        }
        .chat-area::-webkit-scrollbar { width: 5px; }
        .chat-area::-webkit-scrollbar-thumb { background: #444; border-radius: 5px; }
        .msg {
            max-width: 80%; padding: 10px 14px; border-radius: 18px;
            font-size: 14px; line-height: 1.4; word-wrap: break-word;
            animation: pop 0.3s ease;
        }
        @keyframes pop {
            0% { transform: scale(0.8); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }
        .user-msg {
            align-self: flex-end;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #fff; border-bottom-right-radius: 4px;
        }
        .bot-msg {
            align-self: flex-start;
            background: #1e1e2e; color: #e0e0e0;
            border-bottom-left-radius: 4px;
            border: 1px solid #333;
        }
        .typing {
            align-self: flex-start; color: #888; font-size: 13px;
            padding: 8px 14px; font-style: italic;
        }
        .input-area {
            padding: 12px 15px; background: #1a1a2e;
            display: flex; gap: 10px; border-top: 1px solid #333;
        }
        .input-area input {
            flex: 1; padding: 12px 15px; border: none; border-radius: 25px;
            background: #252540; color: #fff; font-size: 14px; outline: none;
        }
        .input-area input::placeholder { color: #666; }
        .input-area button {
            padding: 12px 22px; border: none; border-radius: 25px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #fff; font-weight: bold; font-size: 14px; cursor: pointer;
        }
        .input-area button:active { transform: scale(0.95); }
    </style>
</head>
<body>
    <div class="app">
        <div class="header">
            <div class="avatar">🤖</div>
            <div class="header-info">
                <h2>AliBot</h2>
                <p>● Online | Made by Ali Arsh Khan</p>
            </div>
        </div>
        <div class="chat-area" id="chat">
            <div class="msg bot-msg">Salam! Main AliBot hoon. Mujhse duniya ki koi bhi baat poochein! 🌟</div>
        </div>
        <div class="input-area">
            <input type="text" id="msgInput" placeholder="Yahan likhein..." onkeypress="if(event.key==='Enter') sendMsg()">
            <button onclick="sendMsg()">Send</button>
        </div>
    </div>

    <script>
        async function sendMsg() {
            const input = document.getElementById('msgInput');
            const chat = document.getElementById('chat');
            const text = input.value.trim();
            if (!text) return;

            // User ka message
            const userDiv = document.createElement('div');
            userDiv.className = 'msg user-msg';
            userDiv.innerText = text;
            chat.appendChild(userDiv);
            input.value = '';
            chat.scrollTop = chat.scrollHeight;

            // Typing indicator
            const typing = document.createElement('div');
            typing.className = 'typing';
            typing.innerText = 'AliBot typing...';
            chat.appendChild(typing);
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await res.json();
                typing.remove();

                const botDiv = document.createElement('div');
                botDiv.className = 'msg bot-msg';
                botDiv.innerText = data.reply;
                chat.appendChild(botDiv);
                chat.scrollTop = chat.scrollHeight;
            } catch (e) {
                typing.innerText = 'Error aa gaya.';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    reply = ask_groq(user_msg)
    return jsonify({'reply': reply})
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
