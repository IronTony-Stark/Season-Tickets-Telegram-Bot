import constants
import telebot
import flask
import mysql.connector
from flask import Flask

# from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)
bot = telebot.TeleBot(constants.bot_token, threaded=False)

db = constants.initialize_mysql()
cursor = db.cursor()

database_tickets = {
    "Метро 46 147": "0",
    "Метро 62 197": "1",
    "Метро Безліміт 308": "2",
    "Метро-Автобус 46 288": "3",
    "Метро-Автобус 62 388": "4",
    "Метро-Автобус Безліміт 433": "5",
    "Метро-Тролейбус 46 288": "6",
    "Метро-Тролейбус 62 388": "7",
    "Метро-Тролейбус Безліміт 433": "8",
    "Метро-Трамвай 46 288": "9",
    "Метро-Трамвай 62 388": "A",
    "Метро-Трамвай Безліміт 433": "B"
}

database_tickets_keys = list(database_tickets.keys())

# Sorted by first column
markup_buy_menu_1 = telebot.types.InlineKeyboardMarkup()
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton('Сортувати за 2 колонкою',
                                                         callback_data="Sort by 2nd column"))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:36}{:30}{}".format("Метро", "      46", "147грн"),
                                                         callback_data=database_tickets_keys[0]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:36}{:30}{}".format("Метро", "      62", "197грн"),
                                                         callback_data=database_tickets_keys[1]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:30}{:30}{}".format("Метро", "      Безліміт", "308грн"),
                                                         callback_data=database_tickets_keys[2]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:32}{:25}{}".format("Метро-Автобус", " 46", "288грн"),
                                                         callback_data=database_tickets_keys[3]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:32}{:25}{}".format("Метро-Автобус", " 62", "388грн"),
                                                         callback_data=database_tickets_keys[4]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:26}{:25}{}".format("Метро-Автобус", " Безліміт", "433грн"),
                                                         callback_data=database_tickets_keys[5]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:30}{:24}{}".format("Метро-Тролейбус", "46", "288грн"),
                                                         callback_data=database_tickets_keys[6]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:30}{:24}{}".format("Метро-Тролейбус", "62", "388грн"),
                                                         callback_data=database_tickets_keys[7]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:24}{:24}{}".format("Метро-Тролейбус", "Безліміт", "433грн"),
                                                         callback_data=database_tickets_keys[8]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:32}{:24}{}".format("Метро-Трамвай", "46", "288грн"),
                                                         callback_data=database_tickets_keys[9]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:32}{:24}{}".format("Метро-Трамвай", "62", "388грн"),
                                                         callback_data=database_tickets_keys[10]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("{:26}{:24}{}".format("Метро-Трамвай", "Безліміт", "433грн"),
                                                         callback_data=database_tickets_keys[11]))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("Купити", callback_data="buy"),
                      telebot.types.InlineKeyboardButton("Видалити проїзний", callback_data="remove_from_order_menu"))

# Sorted by second column
markup_buy_menu_2 = telebot.types.InlineKeyboardMarkup()
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton('Сортувати за 1 колонкою',
                                                         callback_data="Sort by 1st column"))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:36}{:30}{}".format("Метро", "      46", "147грн"),
                                                         callback_data=database_tickets_keys[0]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:32}{:25}{}".format("Метро-Автобус", " 46", "288грн"),
                                                         callback_data=database_tickets_keys[3]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:30}{:24}{}".format("Метро-Тролейбус", "46", "288грн"),
                                                         callback_data=database_tickets_keys[6]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:32}{:24}{}".format("Метро-Трамвай", "46", "288грн"),
                                                         callback_data=database_tickets_keys[9]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:36}{:30}{}".format("Метро", "      62", "197грн"),
                                                         callback_data=database_tickets_keys[1]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:32}{:25}{}".format("Метро-Автобус", " 62", "388грн"),
                                                         callback_data=database_tickets_keys[4]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:30}{:24}{}".format("Метро-Тролейбус", "62", "388грн"),
                                                         callback_data=database_tickets_keys[7]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:32}{:24}{}".format("Метро-Трамвай", "62", "388грн"),
                                                         callback_data=database_tickets_keys[10]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:30}{:30}{}".format("Метро", "      Безліміт", "308грн"),
                                                         callback_data=database_tickets_keys[2]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:26}{:25}{}".format("Метро-Автобус", " Безліміт", "433грн"),
                                                         callback_data=database_tickets_keys[5]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:24}{:24}{}".format("Метро-Тролейбус", "Безліміт", "433грн"),
                                                         callback_data=database_tickets_keys[8]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("{:26}{:24}{}".format("Метро-Трамвай", "Безліміт", "433грн"),
                                                         callback_data=database_tickets_keys[11]))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("Купити", callback_data="buy"),
                      telebot.types.InlineKeyboardButton("Видалити проїзний", callback_data="remove_from_order_menu"))

markup_contact_me = telebot.types.InlineKeyboardMarkup()
markup_contact_me.row(telebot.types.InlineKeyboardButton("@TonyStarkZal", url="https://t.me/TonyStarkZal"))

markup_invoice = telebot.types.InlineKeyboardMarkup()
markup_invoice.row(telebot.types.InlineKeyboardButton("Pay", pay=True))
markup_invoice.row(telebot.types.InlineKeyboardButton("Змінити замовлення", callback_data="return_to_buy_menu"))


def get_current_markup(query):
    json_markup = query.message.json.get('reply_markup').get('inline_keyboard')
    # If text is 'Sort by 2nd column' then the keyboard is sorted by 1st column
    if json_markup[0][0]['text'] == "Сортувати за 2 колонкою":
        return markup_buy_menu_1
    else:
        return markup_buy_menu_2


def awake_mysql_db():
    """
    If there's no connection, creates one, else pings to wake up the connection
    """
    global db
    if db is None:
        db = constants.initialize_mysql()
    else:
        db.ping(True)


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


def get_customer_order(query):
    """
    Returns customer's order in number format (database_tickets values).
    """
    awake_mysql_db()
    sql = "SELECT ORDERS FROM customers WHERE User_Id = %s"
    val = (query.from_user.id,)
    cursor.execute(sql, val)
    return cursor.fetchall()[0][0]


def get_order_description_and_total_price(query):
    """
    Returns customer's order in string format (database_tickets keys) and total price of this order.
    """
    customer_order = get_customer_order(query)
    price = 0
    description = ""
    for ticket in customer_order:
        db_tickets_key = database_tickets_keys[list(database_tickets.values()).index(ticket)]
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
        this_ticket_db_key = database_tickets_keys[list(database_tickets.values()).index(ticket)]
        markup_remove_from_order_menu.row(
            telebot.types.InlineKeyboardButton(this_ticket_db_key + "грн",
                                               callback_data=this_ticket_db_key + " remove_ticket"))
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
    update_order_description_and_total_price_in_message(query, get_current_markup(query))
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


@bot.message_handler(commands=['start'])
def handle_text(message):
    # TODO Access and admin
    bot.send_message(message.chat.id, "Лінк на мій телеграм", reply_markup=markup_contact_me)


if __name__ == "__main__":
    app.run()
