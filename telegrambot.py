import telebot
from telebot import types

# Replace 'YOUR_API_TOKEN' with your bot's API token
API_TOKEN = 'YOUR_API_TOKEN'

# Initialize the bot
bot = telebot.TeleBot(API_TOKEN)

# Store user IDs
user_ids = set()

# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_ids.add(user_id)
    
    markup = types.InlineKeyboardMarkup()
    message_button = types.InlineKeyboardButton("Send a message", callback_data='send_message')
    file_button = types.InlineKeyboardButton("Send a file", callback_data='send_file')
    
    markup.add(message_button, file_button)
    
    bot.send_message(message.chat.id, "Welcome to the bot! What would you like to do?", reply_markup=markup)

# Callback query handler for button presses
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'send_message':
        msg = bot.send_message(call.message.chat.id, "Please type the message you want to send to everyone:")
        bot.register_next_step_handler(msg, broadcast_message)
    elif call.data == 'send_file':
        msg = bot.send_message(call.message.chat.id, "Please send the file you want to distribute:")
        bot.register_next_step_handler(msg, handle_file)

# Function to broadcast message to all users
def broadcast_message(message):
    message_to_send = message.text
    for user_id in user_ids:
        bot.send_message(user_id, message_to_send)
    bot.send_message(message.chat.id, "Message sent to all users.")

# Function to handle file upload and broadcast
def handle_file(message):
    if message.document:
        for user_id in user_ids:
            bot.send_document(user_id, message.document.file_id)
        bot.send_message(message.chat.id, "File sent to all users.")
    else:
        bot.send_message(message.chat.id, "Please upload a valid file.")

# Start the bot
bot.polling()