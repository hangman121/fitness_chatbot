from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv


load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


conversation_history = []

@app.route('/')
def home():
    return "Fitness Chatbot is live!"

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    
    conversation_history.append({"role": "user", "content": user_message})

    try:
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[ 
                {
                    "role": "system",
                    "content": "You are a helpful fitness assistant. When someone greets you with 'hey' or 'hi', respond with 'Hi! I am Fityy, your fitness assistant. How may I help you with your fitness goal today?'. Only respond to questions related to fitness, health, workouts, diet, or exercise. If the question is unrelated to fitness, respond with: 'I'm a fitness assistant! Please ask something related to workouts, nutrition, or health.'"
                }
            ] + conversation_history  
        )

        
        reply = response["choices"][0]["message"]["content"]

        
        conversation_history.append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

