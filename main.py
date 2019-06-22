from reply_markup_data import *
from database_data import *
import telebot
import flask
import mysql.connector
from flask import Flask

# from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)
bot = telebot.TeleBot(constants.bot_token, threaded=False)


def get_username_or_first_name(chat_id, user_id):
    """
    Returns username if exists. Else, returns first_name
    """
    chat_member_who_has_birthday = bot.get_chat_member(chat_id, user_id)
    if chat_member_who_has_birthday.user.username is None:
        name = chat_member_who_has_birthday.user.first_name
    else:
        name = "@" + chat_member_who_has_birthday.user.username
    return name


def get_key_by_value(dict_keys, value):
    return dict_keys[list(database_tickets.values()).index(value)]


def get_order_description_and_total_price(query):
    """
    Returns customer's order in string format (database_tickets keys) and total price of this order.
    """
    customer_order = get_customer_order(query)
    price = 0
    description = ""
    for ticket in customer_order:
        db_tickets_key = get_key_by_value(database_tickets_keys, ticket)
        price += int(db_tickets_key.split()[2])
        description += "\n" + db_tickets_key + "грн"
    return description, price


def update_order_description_and_total_price_in_message(query, reply_markup):
    """
    Changes the text of the message to contain current customer's order and total price of this order
    """
    description, price = get_order_description_and_total_price(query)
    if description:
        message_text = "Твоє замовлення: \n" + description + "\n\nЗагальна вартість: " + str(price) + " грн"
    else:
        message_text = "Вибери проїзний або проїзні"
    bot.edit_message_text(message_text,
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


def generate_markup_remove_from_order_menu(query):
    """
    Generates keyboard markup consisting of tickets in customer's order, so he can delete this tickets from the order
    """
    markup_remove_from_order_menu = telebot.types.InlineKeyboardMarkup()
    customer_order = get_customer_order(query)
    for ticket in customer_order:
        this_ticket_db_key = get_key_by_value(database_tickets_keys, ticket)
        markup_remove_from_order_menu.row(telebot.types.InlineKeyboardButton(this_ticket_db_key + "грн",
                                                                             callback_data=
                                                                             this_ticket_db_key + " remove_ticket"))
    markup_remove_from_order_menu.row(
        telebot.types.InlineKeyboardButton("Назад", callback_data="return_to_buy_menu"))
    return markup_remove_from_order_menu


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
    bot.send_message(message.chat.id, "Вибери проїзний або проїзні", reply_markup=markup_buy_menu_1)


@bot.callback_query_handler(lambda query: query.data == "Sort by 1st column")
def process_callback_1(query):
    update_order_description_and_total_price_in_message(query, markup_buy_menu_1)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Sort by 2nd column")
def process_callback_1(query):
    update_order_description_and_total_price_in_message(query, markup_buy_menu_2)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data in database_tickets_keys)
def process_callback_1(query):
    awake_mysql_db()
    try:
        sql = "INSERT INTO customers (User_Id, Username, Orders) VALUES (%s, %s, %s)"
        val = (query.from_user.id,
               get_username_or_first_name(query.message.chat.id, query.from_user.id),
               database_tickets.get(query.data))
        cursor.execute(sql, val)
    except mysql.connector.IntegrityError:
        customer_order = get_customer_order(query)
        if len(customer_order) == 10:
            bot.answer_callback_query(query.id, "Вибач, але ти можеш замовити максимум 10 проїзних", True)
            return
        sql = "UPDATE customers SET Orders = %s WHERE User_Id = %s"
        val = (customer_order + database_tickets.get(query.data), query.from_user.id)
        cursor.execute(sql, val)
    db.commit()
    update_order_description_and_total_price_in_message(query, get_current_buy_menu_markup(query))
    bot.answer_callback_query(query.id, "Додано " + query.data)


@bot.callback_query_handler(lambda query: query.data == "buy")
def process_callback_1(query):
    description, price = get_order_description_and_total_price(query)
    if not description:
        bot.answer_callback_query(query.id, "Ти нічого не замовив", True)
        return
    bot.delete_message(query.message.chat.id, query.message.message_id)
    bot.send_invoice(query.message.chat.id, "Season tickets", "Твоє замовлення: \n" + description + "\n",
                     "Custom-Payload",
                     constants.payment_provider_token, "UAH", [telebot.types.LabeledPrice("Test", price * 100)],
                     "test-payment", reply_markup=markup_invoice)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "remove_from_order_menu")
def process_callback_1(query):
    bot.delete_message(query.message.chat.id, query.message.message_id)
    bot.send_message(query.message.chat.id, "Вибери проїзні, які потрібно видалити з замовлення",
                     reply_markup=generate_markup_remove_from_order_menu(query))
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data in [key + " remove_ticket" for key in database_tickets_keys])
def process_callback_1(query):
    awake_mysql_db()
    old_order = get_customer_order(query)
    new_order = old_order.replace(database_tickets.get(query.data[:-14]), "", 1)
    sql = "UPDATE customers SET Orders = %s WHERE User_Id = %s"
    val = (new_order, query.from_user.id)
    cursor.execute(sql, val)
    db.commit()
    bot.edit_message_text("Вибери проїзні, які потрібно видалити з замовлення",
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=generate_markup_remove_from_order_menu(query))
    bot.answer_callback_query(query.id, "\"" + query.data[:-14] + "грн\" видалено з замовлення")


@bot.callback_query_handler(lambda query: query.data == "return_to_buy_menu")
def process_callback_1(query):
    description, price = get_order_description_and_total_price(query)
    if description:
        message_text = "Твоє замовлення: \n" + description + "\n\nЗагальна вартість: " + str(price) + " грн"
    else:
        message_text = "Вибери проїзний або проїзні"
    bot.send_message(query.message.chat.id, message_text, reply_markup=markup_buy_menu_1)
    bot.delete_message(query.message.chat.id, query.message.message_id)
    bot.answer_callback_query(query.id)


@bot.message_handler(commands=['start'])
def handle_text(message):
    # TODO Access and admin
    bot.send_message(message.chat.id, "Лінк на мій телеграм", reply_markup=markup_contact_me)


if __name__ == "__main__":
    app.run()
