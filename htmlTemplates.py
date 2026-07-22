css = '''
<style>
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    max-width: 80%;
}

.chat-message.user {
    background-color: #2b313e;
    margin-left: auto;
    border-bottom-right-radius: 0;
}

.chat-message.bot {
    background-color: #475063;
    margin-right: auto;
    border-bottom-left-radius: 0;
}

.chat-message .label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.3rem;
}

.chat-message.user .label {
    color: #8ab4f8;
    text-align: right;
}

.chat-message.bot .label {
    color: #a5d6a7;
    text-align: left;
}

.chat-message .message {
    width: 100%;
    padding: 0;
    color: #fff;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="label">🤖 AI</div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="label">🧑 You</div>
    <div class="message">{{MSG}}</div>
</div>
'''