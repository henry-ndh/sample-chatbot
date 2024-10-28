// chat.js

document.addEventListener("DOMContentLoaded", function () {
    const sendButton = document.getElementById("send-button");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const sampleQuestionsList = document.getElementById(
        "sample-questions-list"
    );
    const sampleQuestions = document.querySelectorAll(".sample-question");

    // Hàm để thêm tin nhắn vào chat box
    function addMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);

        const textSpan = document.createElement("span");
        textSpan.classList.add("text");
        textSpan.textContent = message;

        messageDiv.appendChild(textSpan);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Hàm để gửi yêu cầu tới backend
    function sendMessage(message) {
        if (message.trim() === "") return;

        // Hiển thị tin nhắn của người dùng
        addMessage(message, "user");

        // Nếu gửi từ danh sách mẫu, không cần nhập lại vào input
        if (userInput.value.trim() !== "") {
            userInput.value = "";
        }

        // Gửi yêu cầu POST tới /chat
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.response) {
                    addMessage(data.response, "bot");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                addMessage("Có lỗi xảy ra. Vui lòng thử lại sau.", "bot");
            });
    }

    // Sự kiện khi nhấn nút gửi
    sendButton.addEventListener("click", function () {
        const message = userInput.value.trim();
        sendMessage(message);
    });

    // Sự kiện khi nhấn phím Enter
    userInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            const message = userInput.value.trim();
            sendMessage(message);
        }
    });

    // Sự kiện khi nhấp vào một câu hỏi mẫu
    sampleQuestions.forEach(function (question) {
        question.addEventListener("click", function () {
            const message = this.textContent;
            sendMessage(message);
        });
    });
});
