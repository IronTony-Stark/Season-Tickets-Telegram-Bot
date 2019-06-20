import constants
import telebot
import flask
from flask import Flask

# import emoji
# from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)
bot = telebot.TeleBot(constants.bot_token, threaded=False)

markup_1 = telebot.types.InlineKeyboardMarkup()
markup_1.row(telebot.types.InlineKeyboardButton('Сортувати за 2 колонкою',
                                                callback_data="Sort by 2nd column"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро                                   46                147грн',
                                                callback_data="Underground-46"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро                                   62                197грн',
                                                callback_data="Underground-62"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро                              Безліміт         308грн',
                                                callback_data="Underground Unlimited"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро-Автобус                  46                288грн',
                                                callback_data="Underground-Bus-46"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро-Автобус                  62                338грн',
                                                callback_data="Underground-Bus-62"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро-Автобус            Безліміт         433грн',
                                                callback_data="Underground-Bus Unlimited"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро-Тролейбус             46                288грн',
                                                callback_data="Underground-Trolleybus-46"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро-Тролейбус             62                338грн',
                                                callback_data="Underground-Trolleybus-62"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро-Тролейбус       Безліміт         433грн',
                                                callback_data="Underground-Trolleybus Unlimited"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро-Трамвай                46                288грн',
                                                callback_data="Underground-Tram-46"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро-Трамвай                62                338грн',
                                                callback_data="Underground-Tram-62"))
markup_1.row(telebot.types.InlineKeyboardButton('Метро-Трамвай          Безліміт         433грн',
                                                callback_data="Underground-Tram Unlimited"))

markup_2 = telebot.types.InlineKeyboardMarkup()
markup_2.row(telebot.types.InlineKeyboardButton('Сортувати за 1 колонкою',
                                                callback_data="Sort by 1st column"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро                                   46                147грн',
                                                callback_data="Underground-46"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро-Автобус                  46                288грн',
                                                callback_data="Underground-Bus-46"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро-Тролейбус             46                288грн',
                                                callback_data="Underground-Trolleybus-46"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро-Трамвай                46                288грн',
                                                callback_data="Underground-Tram-46"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро                                   62                197грн',
                                                callback_data="Underground-62"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро-Автобус                  62                338грн',
                                                callback_data="Underground-Bus-62"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро-Тролейбус             62                338грн',
                                                callback_data="Underground-Trolleybus-62"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро-Трамвай                62                338грн',
                                                callback_data="Underground-Tram-62"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро                              Безліміт         308грн',
                                                callback_data="Underground Unlimited"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро-Автобус            Безліміт         433грн',
                                                callback_data="Underground-Bus Unlimited"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро-Тролейбус       Безліміт         433грн',
                                                callback_data="Underground-Trolleybus Unlimited"))
markup_2.row(telebot.types.InlineKeyboardButton('Метро-Трамвай          Безліміт         433грн',
                                                callback_data="Underground-Tram Unlimited"))


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


@bot.message_handler(commands=['buy'])
def handle_text(message):
    bot.send_message(message.chat.id, "М - Метро \nА - Автобус \nТрол - Тролейбус \nТрам - Трамвай",
                     reply_markup=markup_1)


@bot.callback_query_handler(lambda query: query.data == "Sort by 1st column")
def process_callback_1(query):
    bot.edit_message_text("Вибери проїзний або проїзні",
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_1)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Sort by 2nd column")
def process_callback_1(query):
    bot.edit_message_text("Вибери проїзний або проїзні",
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_2)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-46")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-62")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground Unlimited")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-Bus-46")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-Bus-62")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-Bus Unlimited")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-Trolleybus-46")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-Trolleybus-62")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-Trolleybus Unlimited")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-Tram-46")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-Tram-62")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Underground-Tram Unlimited")
def process_callback_1(query):
    bot.answer_callback_query(query.id)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_invoice(message.chat.id, "Season tickets", "Cheap season tickets for everyone", "Custom-Payload",
                     constants.payment_provider_token, "UAH", [telebot.types.LabeledPrice("Test", 147 * 100)],
                     "test-payment")


if __name__ == "__main__":
    app.run()
