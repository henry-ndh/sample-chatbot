from flask import Flask, request, jsonify, render_template
import nltk
from nltk.chat.util import Chat, reflections

app = Flask(__name__)

# Nếu bạn chưa tải dữ liệu NLTK cần thiết, hãy bật các dòng dưới đây một lần
# nltk.download('punkt')

# Định nghĩa các cặp mẫu câu hỏi và câu trả lời
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today?",]
    ],
    [
        r"hi|hey|hello",
        ["Hello!", "Hey there!", "Hi! How can I assist you today?"]
    ],
    [
        r"what is your name\??",
        ["I am a chatbot created using NLTK.", "You can call me ChatBot."]
    ],
    [
        r"What are the university's hours of operation\??",
        ["The university is open Monday to Friday from 8 AM to 6 PM.\n"]
    ],
    [
        r"When are admissions open\??",
        ["Admissions are open until the end of the month. You can apply online via the university website.\n"]
    ],
    [
        r"How can I contact the admissions office?(.*)",
        ["You can contact the admissions office at admissions@university.edu or call 555-1234.\n"]
    ],
    [
        r"What courses are available at the university?",
        ["Courses available include Computer Science, Business Administration, Engineering, and more. Visit the website for a full list.\n"]
    ],
    [
        r"quit",
        ["Bye! Take care. See you soon :)", "It was nice talking to you. Goodbye!"]
    ],
    [
        r".*\bhours\b.*",
        ["The university is open from 8 AM to 6 PM."]
    ],
    [
        r".*\badmissions\b.*",
        ["Admissions are open until the end of the month. You can apply online via the university website."]
    ],
    [
        r".*\boffice\b.*",
        ["You can contact the admissions office at admissions@university.edu or call 555-1234."]
    ],
    [
        r".*\bcourses\b.*",
        ["Courses available include Computer Science, Business Administration, Engineering, and more. Visit the website for a full list."]
    ],
]
# Khởi tạo chatbot với các cặp câu hỏi và câu trả lời
chatbot = Chat(pairs, reflections)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    
    if not user_input:
        return jsonify({"response": "Xin lỗi, tôi không nhận được nội dung bạn gửi."}), 400
    
    response = chatbot.respond(user_input)
    
    if response is None:
        response = "I'm sorry, I don't understand that. Could you please rephrase?"
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
