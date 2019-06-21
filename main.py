import constants
import telebot
import flask
import mysql.connector
from flask import Flask
# import emoji
# from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)
bot = telebot.TeleBot(constants.bot_token, threaded=False)

db = constants.initialize_mysql()
cursor = db.cursor()


def awake_mysql_db():
    """"
    If there's no connection, creates one, else pings to wake up the connection
    """
    global db
    if db is None:
        db = constants.initialize_mysql()
    else:
        db.ping(True)


def get_username_or_first_name(chat_id, user_id):
    """"
    Returns username if exists. Else, returns first_name
    """
    chat_member_who_has_birthday = bot.get_chat_member(chat_id, user_id)
    if chat_member_who_has_birthday.user.username is None:
        name = chat_member_who_has_birthday.user.first_name
    else:
        name = "@" + chat_member_who_has_birthday.user.username
    return name


def get_customer_order(query):
    """"Returns customer's order. There must be a connection to the database"""
    sql = "SELECT ORDERS FROM customers WHERE User_Id = %s"
    val = (query.from_user.id,)
    cursor.execute(sql, val)
    return cursor.fetchall()[0][0]


database_tickets_keys = {"Underground-46": "0",
                         "Underground-62": "1",
                         "Underground Unlimited": "2",
                         "Underground-Bus-46": "3",
                         "Underground-Bus-62": "4",
                         "Underground-Bus Unlimited": "5",
                         "Underground-Trolleybus-46": "6",
                         "Underground-Trolleybus-62": "7",
                         "Underground-Trolleybus Unlimited": "8",
                         "Underground-Tram-46": "9",
                         "Underground-Tram-62": "A",
                         "Underground-Tram Unlimited": "B"}

markup_1 = telebot.types.InlineKeyboardMarkup()
markup_1.row(telebot.types.InlineKeyboardButton('Сортувати за 2 колонкою',
                                                callback_data="Sort by 2nd column"))
markup_1.row(telebot.types.InlineKeyboardButton("{:36}{:30}{}".format("Метро", "      46", "147грн"),
                                                callback_data="Underground-46"))
markup_1.row(telebot.types.InlineKeyboardButton("{:36}{:30}{}".format("Метро", "      62", "197грн"),
                                                callback_data="Underground-62"))
markup_1.row(telebot.types.InlineKeyboardButton("{:30}{:30}{}".format("Метро", "      Безліміт", "308грн"),
                                                callback_data="Underground Unlimited"))
markup_1.row(telebot.types.InlineKeyboardButton("{:32}{:25}{}".format("Метро-Автобус", " 46", "288грн"),
                                                callback_data="Underground-Bus-46"))
markup_1.row(telebot.types.InlineKeyboardButton("{:32}{:25}{}".format("Метро-Автобус", " 62", "388грн"),
                                                callback_data="Underground-Bus-62"))
markup_1.row(telebot.types.InlineKeyboardButton("{:26}{:25}{}".format("Метро-Автобус", " Безліміт", "433грн"),
                                                callback_data="Underground-Bus Unlimited"))
markup_1.row(telebot.types.InlineKeyboardButton("{:30}{:24}{}".format("Метро-Тролейбус", "46", "288грн"),
                                                callback_data="Underground-Trolleybus-46"))
markup_1.row(telebot.types.InlineKeyboardButton("{:30}{:24}{}".format("Метро-Тролейбус", "62", "388грн"),
                                                callback_data="Underground-Trolleybus-62"))
markup_1.row(telebot.types.InlineKeyboardButton("{:24}{:24}{}".format("Метро-Тролейбус", "Безліміт", "433грн"),
                                                callback_data="Underground-Trolleybus Unlimited"))
markup_1.row(telebot.types.InlineKeyboardButton("{:32}{:24}{}".format("Метро-Трамвай", "46", "288грн"),
                                                callback_data="Underground-Tram-46"))
markup_1.row(telebot.types.InlineKeyboardButton("{:32}{:24}{}".format("Метро-Трамвай", "62", "388грн"),
                                                callback_data="Underground-Tram-62"))
markup_1.row(telebot.types.InlineKeyboardButton("{:26}{:24}{}".format("Метро-Трамвай", "Безліміт", "433грн"),
                                                callback_data="Underground-Tram Unlimited"))

markup_2 = telebot.types.InlineKeyboardMarkup()
markup_2.row(telebot.types.InlineKeyboardButton('Сортувати за 1 колонкою',
                                                callback_data="Sort by 1st column"))
markup_2.row(telebot.types.InlineKeyboardButton("{:36}{:30}{}".format("Метро", "      46", "147грн"),
                                                callback_data="Underground-46"))
markup_2.row(telebot.types.InlineKeyboardButton("{:32}{:25}{}".format("Метро-Автобус", " 46", "288грн"),
                                                callback_data="Underground-Bus-46"))
markup_2.row(telebot.types.InlineKeyboardButton("{:30}{:24}{}".format("Метро-Тролейбус", "46", "288грн"),
                                                callback_data="Underground-Trolleybus-46"))
markup_2.row(telebot.types.InlineKeyboardButton("{:32}{:24}{}".format("Метро-Трамвай", "46", "288грн"),
                                                callback_data="Underground-Tram-46"))
markup_2.row(telebot.types.InlineKeyboardButton("{:36}{:30}{}".format("Метро", "      62", "197грн"),
                                                callback_data="Underground-62"))
markup_2.row(telebot.types.InlineKeyboardButton("{:32}{:25}{}".format("Метро-Автобус", " 62", "388грн"),
                                                callback_data="Underground-Bus-62"))
markup_2.row(telebot.types.InlineKeyboardButton("{:30}{:24}{}".format("Метро-Тролейбус", "62", "388грн"),
                                                callback_data="Underground-Trolleybus-62"))
markup_2.row(telebot.types.InlineKeyboardButton("{:32}{:24}{}".format("Метро-Трамвай", "62", "388грн"),
                                                callback_data="Underground-Tram-62"))
markup_2.row(telebot.types.InlineKeyboardButton("{:30}{:30}{}".format("Метро", "      Безліміт", "308грн"),
                                                callback_data="Underground Unlimited"))
markup_2.row(telebot.types.InlineKeyboardButton("{:26}{:25}{}".format("Метро-Автобус", " Безліміт", "433грн"),
                                                callback_data="Underground-Bus Unlimited"))
markup_2.row(telebot.types.InlineKeyboardButton("{:24}{:24}{}".format("Метро-Тролейбус", "Безліміт", "433грн"),
                                                callback_data="Underground-Trolleybus Unlimited"))
markup_2.row(telebot.types.InlineKeyboardButton("{:26}{:24}{}".format("Метро-Трамвай", "Безліміт", "433грн"),
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
    bot.send_message(message.chat.id, "Вибери проїзний або проїзні", reply_markup=markup_1)


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


@bot.callback_query_handler(lambda query: query.data in database_tickets_keys.keys())
def process_callback_1(query):
    awake_mysql_db()
    try:
        sql = "INSERT INTO customers (User_Id, Username, Orders) VALUES (%s, %s, %s)"
        val = (query.from_user.id,
               get_username_or_first_name(query.message.chat.id, query.from_user.id),
               database_tickets_keys.get(query.data))
        cursor.execute(sql, val)
    except mysql.connector.IntegrityError:
        customer_order = get_customer_order(query)
        if len(customer_order) == 10:
            bot.answer_callback_query(query.id, "Вибач, але ти можеш замовити максимум 10 проїзних", True)
            return
        sql = "UPDATE customers SET Orders = %s WHERE User_Id = %s"
        val = (customer_order + database_tickets_keys.get(query.data), query.from_user.id)
        cursor.execute(sql, val)
    db.commit()
    bot.answer_callback_query(query.id, "Added " + query.data)


# @bot.callback_query_handler(lambda query: query.data == "Underground-46")
# def process_callback_1(query):
#     number = database_tickets_keys.get(query.data)
#     bot.answer_callback_query(query.id, number)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground-62")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground Unlimited")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground-Bus-46")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground-Bus-62")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground-Bus Unlimited")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground-Trolleybus-46")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground-Trolleybus-62")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground-Trolleybus Unlimited")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground-Tram-46")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground-Tram-62")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)
#
#
# @bot.callback_query_handler(lambda query: query.data == "Underground-Tram Unlimited")
# def process_callback_1(query):
#     bot.answer_callback_query(query.id)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_invoice(message.chat.id, "Season tickets", "Cheap season tickets for everyone", "Custom-Payload",
                     constants.payment_provider_token, "UAH", [telebot.types.LabeledPrice("Test", 147 * 100)],
                     "test-payment")


if __name__ == "__main__":
    app.run()
