import constants
import telebot
import flask
from flask import Flask
# from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)
bot = telebot.TeleBot(constants.bot_token, threaded=False)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return '<h1>Season Tickets Bot</h1>'


@app.route('/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, "Ping")


if __name__ == "__main__":
    app.run()
