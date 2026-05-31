const chatHistory = document.getElementById('chat-history');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');
    msgDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    msgDiv.textContent = text;
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    appendMessage(text, 'user');
    chatInput.value = '';

    // Typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('message', 'bot-message');
    typingDiv.textContent = 'Typing...';
    typingDiv.id = 'typing-indicator';
    chatHistory.appendChild(typingDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();

        // Remove typing indicator
        const currentTyping = document.getElementById('typing-indicator');
        if (currentTyping) currentTyping.remove();

        appendMessage(data.response, 'bot');
    } catch (error) {
        console.error('Error:', error);

        // Remove typing indicator
        const currentTyping = document.getElementById('typing-indicator');
        if (currentTyping) currentTyping.remove();

        appendMessage("Sorry, I'm having trouble connecting right now.", 'bot');
    }
}

sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
