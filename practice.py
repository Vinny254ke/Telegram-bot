from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import logging

# Set up logging to get information about the bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Store user IDs
user_ids = set()

# Define command start handler
def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    user_ids.add(user_id)
    
    keyboard = [
        [InlineKeyboardButton("Send a message", callback_data='send_message')],
        [InlineKeyboardButton("Send a file", callback_data='send_file')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome to the bot! What would you like to do?', reply_markup=reply_markup)

# Define button callback handler
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'send_message':
        context.bot.send_message(chat_id=query.message.chat_id, text="Please type the message you want to send to everyone:")
        context.user_data['mode'] = 'send_message'
    elif query.data == 'send_file':
        context.bot.send_message(chat_id=query.message.chat_id, text="Please send the file you want to distribute:")
        context.user_data['mode'] = 'send_file'

# Define message handler
def handle_message(update: Update, context: CallbackContext):
    mode = context.user_data.get('mode')
    if mode == 'send_message':
        message_to_send = update.message.text
        for user_id in user_ids:
            context.bot.send_message(chat_id=user_id, text=message_to_send)
        update.message.reply_text('Message sent to all users.')
    elif mode == 'send_file':
        # The file will be received in handle_document
        pass

# Define file handler
def handle_document(update: Update, context: CallbackContext):
    mode = context.user_data.get('mode')
    if mode == 'send_file':
        document = update.message.document
        for user_id in user_ids:
            context.bot.send_document(chat_id=user_id, document=document.file_id)
        update.message.reply_text('File sent to all users.')

# Define error handler
def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Main function to start the bot
def main():
    # Replace 'YOUR_API_TOKEN' with your bot's API token
    updater = Updater('YOUR_API_TOKEN', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.document, handle_document))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()