import logging
import os

from telegram.ext import Updater, CommandHandler, PicklePersistence


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm the SummaryBot!")


def new_message(update, context):
    if 'board' not in context.chat_data:
        context.chat_data['board'] = []

    message = ' '.join(context.args)
    if not message:
        update.message.reply_text("I didn't get any message!")
    else:
        context.chat_data['board'].append(message)
        update.message.reply_text('Message added to the board.')


def show_messages(update, context):
    messages = []
    if 'board' in context.chat_data:
        messages = context.chat_data['board']

    if len(messages) == 0:
        update.message.reply_text('No message on the board.')
    else:
        output = ''
        for i in range(len(messages)):
            output += str(i + 1) + '. ' + messages[i] + '\r\n\r\n'
        update.message.reply_text(output)


def clear(update, context):
    if 'board' in context.chat_data:
        context.chat_data['board'] = []
    update.message.reply_text('Done.')


def delete_message(update, context):
    messages = []
    if 'board' in context.chat_data:
        messages = context.chat_data['board']

    index = int(context.args[0])
    if index < 1 or index > len(messages):
        update.message.reply_text('Invalid number!')
    else:
        del messages[index - 1]
        update.message.reply_text('Done.')


def main():
    # Given by Heroku
    port = int(os.environ.get('PORT', '8443'))
    token = os.environ['TOKEN']
    name = os.environ['APP_NAME']

    persistence = PicklePersistence(filename='storage')
    updater = Updater(token=token, persistence=persistence, use_context=True)
    dispatcher = updater.dispatcher

    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add', new_message))
    dispatcher.add_handler(CommandHandler('see', show_messages))
    dispatcher.add_handler(CommandHandler('clear', clear))
    dispatcher.add_handler(CommandHandler('delete', delete_message))

    updater.start_webhook(listen="0.0.0.0",
                          port=port,
                          url_path=token)
    updater.bot.set_webhook('https://{}.herokuapp.com/{}'.format(name, token))
    updater.idle()


if __name__ == '__main__':
    main()
