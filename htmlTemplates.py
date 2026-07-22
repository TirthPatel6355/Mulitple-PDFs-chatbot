css = '''
<style>
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    max-width: 80%;
}

.chat-message.user {
    background-color: #2b313e;
    margin-left: auto;
    flex-direction: row-reverse;
}

.chat-message.bot {
    background-color: #475063;
    margin-right: auto;
    flex-direction: row;
}

.chat-message.avatar {
    width: 15%;
}

.chat-message.avatar img {
    max-width: 10px;
    max-height: 10px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    width: 85%;
    padding: 0 1rem;
    color: #fff;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/1077/1077114.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''