import logging

from telegram.ext import Updater, CommandHandler
from secret import TOKEN


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm the SummaryBot!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
