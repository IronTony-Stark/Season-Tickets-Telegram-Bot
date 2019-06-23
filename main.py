from reply_markup_data import *
from database_data import *
import telebot
import flask
import mysql.connector
from flask import Flask

# from flask_sslify import SSLify
# TODO cashback
# TODO months
app = Flask(__name__)
# sslify = SSLify(app)
bot = telebot.TeleBot(constants.bot_token, threaded=False)


def get_username_or_first_name(chat_id, user_id):
    """
    Returns username if exists. Else, returns first_name
    """
    chat_member = bot.get_chat_member(chat_id, user_id)
    if chat_member.user.username is None:
        name = chat_member.user.first_name
    else:
        name = "@" + chat_member.user.username
    return name


def get_cart_description_and_total_price(query) -> tuple:
    """
    Returns customer's cart in string format (database_tickets keys) and total price of this cart.
    """
    customer_cart = get_customer_cart(query)
    if not customer_cart:
        return None, None
    price = 0
    description = ""
    for ticket in customer_cart:
        db_tickets_key = get_key_by_value(database_tickets_keys, ticket)
        price += int(db_tickets_key.split()[2])
        description += "\n" + db_tickets_key + "грн"
    return description, price


def get_updated_cart_description_and_total_price_message(query) -> str:
    """
    If customer's cart items exists returns string containing the cart items description and total price
    Else returns string with invitation to choose any season ticket
    """
    description, price = get_cart_description_and_total_price(query)
    if description:
        message_text = "Корзина: \n" + description + "\n\nЗагальна вартість: " + str(price) + " грн"
    else:
        message_text = "Спочатку вибери проїзний або проїзні, які хочеш замовити. Їх буде додано до корзини" \
                       "\n\nПотім натисни 'Купити' та оплати замовлення" \
                       "\n\nЯкщо потрібно видалити з корзини проїзний або проїзні натисни 'Видалити з корзини'."
    return message_text


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


@bot.message_handler(commands=['menu'])
def handle_text(message):
    bot.send_message(message.chat.id,
                     get_updated_cart_description_and_total_price_message(message),
                     reply_markup=markup_buy_menu_1)


@bot.callback_query_handler(lambda query: query.data == "Sort by 1st column")
def main_menu_sorted_by_1_column(query):
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_1)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Sort by 2nd column")
def main_menu_sorted_by_2_column(query):
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_2)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data in database_tickets_keys)
def add_ticket(query):
    awake_mysql_db()
    try:
        sql = "INSERT INTO customers (User_Id, Username, Cart) VALUES (%s, %s, %s)"
        val = (query.from_user.id,
               get_username_or_first_name(query.message.chat.id, query.from_user.id),
               database_tickets.get(query.data))
        cursor.execute(sql, val)
    except mysql.connector.IntegrityError:
        customer_cart = get_customer_cart(query)
        customer_order = get_customer_order(query)
        if not customer_order:
            customer_order_length = 0
        else:
            customer_order_length = len(customer_order)
        if len(customer_cart) + customer_order_length == 10:
            bot.answer_callback_query(query.id, "Вибач, але ти можеш замовити максимум 10 проїзних", True)
            return
        sql = "UPDATE customers SET Cart = %s WHERE User_Id = %s"
        val = (customer_cart + database_tickets.get(query.data), query.from_user.id)
        cursor.execute(sql, val)
    db.commit()
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=get_current_buy_menu_markup(query))
    bot.answer_callback_query(query.id, "\"" + query.data + "\" додано до корзини")


@bot.callback_query_handler(lambda query: query.data == "buy")
def buy(query):
    description, price = get_cart_description_and_total_price(query)
    if not description:
        bot.answer_callback_query(query.id, "Твоя корзина порожня. Вибери проїзні, які хочеш купити", True)
        return
    bot.send_invoice(query.message.chat.id,
                     "Season tickets",
                     "Твоє замовлення: \n" + description + "\n",
                     str(get_customer_id(query)) + " " + get_customer_cart(query),
                     constants.payment_provider_token,
                     "UAH",
                     [telebot.types.LabeledPrice("Season tickets", price * 100)],
                     "test-payment",
                     reply_markup=markup_invoice)
    bot.answer_callback_query(query.id)


@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Well... Looks like something went wrong. Please, contact me.")


@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    awake_mysql_db()
    sql = "UPDATE customers SET Cart = %s, Orders = %s WHERE Customer_Id = %s"
    val = ("",
           message.successful_payment.invoice_payload.split()[1],
           message.successful_payment.invoice_payload.split()[0])
    cursor.execute(sql, val)
    db.commit()
    bot.send_message(message.chat.id,
                     "Якщо потрбіно, ти можеш дозамовити проїзні. \n\nЯкщо ти передумав (-ла) і хочеш відмінити "
                     "замовлення проїзного або проїзних, натисни '' у головному меню (/menu)")


@bot.callback_query_handler(lambda query: query.data == "remove_from_cart_menu")
def remove_from_cart_menu(query):
    bot.edit_message_text("Вибери проїзні, які потрібно видалити з корзини",
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=generate_markup_remove_from_cart_menu(query))
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data in [key + " remove_ticket" for key in database_tickets_keys])
def remove_ticket(query):
    awake_mysql_db()
    old_cart = get_customer_cart(query)
    new_cart = old_cart.replace(database_tickets.get(query.data[:-14]), "", 1)
    sql = "UPDATE customers SET Cart = %s WHERE User_Id = %s"
    val = (new_cart, query.from_user.id)
    cursor.execute(sql, val)
    db.commit()
    bot.edit_message_text("Вибери проїзні, які потрібно видалити з корзини",
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=generate_markup_remove_from_cart_menu(query))
    bot.answer_callback_query(query.id, "\"" + query.data[:-14] + "грн\" видалено з корзини")


@bot.callback_query_handler(lambda query: query.data == "return_to_buy_menu")
def return_to_buy_menu(query):
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_1)
    bot.answer_callback_query(query.id)


@bot.message_handler(commands=['start'])
def handle_text(message):
    # TODO Access and admin
    bot.send_message(message.chat.id, "Лінк на мій телеграм", reply_markup=markup_contact_me)


if __name__ == "__main__":
    app.run()
