from reply_markup_data import *
from database_data import *
import telebot
import flask
import mysql.connector
import datetime
from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)
bot = telebot.TeleBot(constants.bot_token, threaded=False)
is_opened = True


def bold(string):
    """
    Surrounds the string with asterisks (*) so it will be parsed bold when using markdown
    """
    if not isinstance(string, str):
        raise TypeError("Must be given a string")
    return "*" + string + "*"


def italic(string):
    """
    Surrounds the string with underscores (_) so it will be parsed italic when using markdown
    """
    if not isinstance(string, str):
        raise TypeError("Must be given a string")
    return "_" + string + " _"


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
    customer_cart = select_customer_db_column_value(query, "Cart")
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
    month_of_order = "Місяць замовлення: " + bold(select_customer_db_column_value(query, "MonthOfOrder"))
    if description:
        message_text = month_of_order + "\n\n" + italic("Корзина") + ": \n" + description + "\n\nЗагальна вартість: " \
                       + bold(str(price)) + " грн"
    else:
        message_text = month_of_order + \
                       "\n\nСпочатку вибери проїзний або проїзні, які хочеш замовити. Їх буде додано до " + \
                       italic("корзини") + \
                       "\n\nПотім натисни " + italic("'Купити'") + " та оплати замовлення" + \
                       "\n\nЯкщо потрібно видалити з " + italic("корзини") + \
                       " проїзний або проїзні, натисни " + italic("'Видалити з корзини'") + "."
    return message_text


def is_opened_and_chose_the_right_month(query, month_of_order):
    """
    :return: True if it is possible to order tickets now and it is allowed to order tickets for the chosen month.
    Else returns False
    """
    if not is_opened:
        bot.answer_callback_query(query.id, "Замовлення проїзних заверешено. Зміна замовлень неможлива", True)
        bot.edit_message_text("Замовлення проїзних заверешено. Зміна замовлень неможлива",
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id)
        return False
    if month_of_order not in constants.months_for_which_tickets_can_be_ordered:
        bot.answer_callback_query(query.id,
                                  "Неправильний місяць замовлення. Неможливо замовити на {}".format(month_of_order),
                                  True)
        bot.edit_message_text("Вибери місяць, на який будеш замовляти проїзний (проїзні)",
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id,
                              reply_markup=generate_markup_choose_orders_month(order_month=True))
        return False
    return True


def check_max_tickets_sold_to_1_user_per_month(query_or_message, equal_sign, specified_customer_cart=None):
    """
    Checks if the customer's order exceeds the maximum amount of tickets that can't be ordered for one month.
    In other words checks if the user wants to order more tickets than allowed (
    constants.max_tickets_sold_to_1_user_per_month)
    :param query_or_message: used in get_customer_cart and get_customer_orders functions
    :param equal_sign: Bool. If true equal sign will be used comparing the amount of tickets user wants to order and
    allowed amount of tickets to order
    :param specified_customer_cart: used in pre_checkout_query when customer cart is empty to specify order
    :return: True if user wants to order an allowed amount of tickets. Else returns False
    """
    customer_cart = select_customer_db_column_value(query_or_message, "Cart")
    customer_order = get_customer_month_orders(
        select_customer_db_column_value(query_or_message, "MonthOfOrder"),
        query_or_message=query_or_message)
    if not customer_cart:
        if not specified_customer_cart:
            customer_cart_length = 0
        else:
            customer_cart_length = len(specified_customer_cart)
    else:
        customer_cart_length = len(customer_cart)
    if not customer_order:
        customer_order_length = 0
    else:
        customer_order_length = len(customer_order)
    if equal_sign:
        check_max = not customer_cart_length + customer_order_length == constants.max_tickets_sold_to_1_user_per_month
    else:
        check_max = not (customer_cart_length + customer_order_length > constants.max_tickets_sold_to_1_user_per_month)
    return check_max


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
    if not is_opened:
        bot.reply_to(message, "Замовлення проїзних заверешено. Зміна замовлень неможлива")
        return
    bot.send_message(message.chat.id,
                     "Вибери місяць, на який будеш замовляти проїзний (проїзні)",
                     reply_markup=generate_markup_choose_orders_month(order_month=True))


@bot.callback_query_handler(lambda query: query.data.startswith("buy choose month"))
def choose_month(query):
    awake_mysql_db()
    current_month = query.data.split()[3]
    if current_month not in constants.months_for_which_tickets_can_be_ordered:
        bot.answer_callback_query(query.id,
                                  "Неправильний місяць замовлення. Неможливо замовити на {}".format(current_month),
                                  True)
        bot.edit_message_text("Вибери місяць, на який будеш замовляти проїзний (проїзні)",
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id,
                              reply_markup=generate_markup_choose_orders_month(order_month=True))
        return
    # -------------------------------------------------------------------------------------------------
    try:
        sql = "INSERT INTO customers (User_Id, Username, MonthOfOrder, Cart, Orders, OrdersAfterRefund) " \
              "VALUES (%s, %s, %s, %s, %s, %s)"
        val = (query.from_user.id,
               get_username_or_first_name(query.message.chat.id, query.from_user.id),
               current_month,
               "", "", "")
        cursor.execute(sql, val)
    except mysql.connector.IntegrityError:
        sql = "UPDATE customers SET MonthOfOrder = %s, Cart = %s WHERE User_Id = %s"
        val = (current_month,
               "",
               query.from_user.id)
        cursor.execute(sql, val)
    db.commit()
    # -------------------------------------------------------------------------------------------------
    orders_month = "Місяць замовлення: " + select_customer_db_column_value(query, "MonthOfOrder")
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_1,
                          parse_mode='markdown')
    bot.answer_callback_query(query.id, orders_month)


@bot.callback_query_handler(lambda query: query.data == "Sort by 1st column")
def buy_menu_sorted_by_1_column(query):
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_1,
                          parse_mode='markdown')
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Sort by 2nd column")
def buy_menu_sorted_by_2_column(query):
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_2,
                          parse_mode='markdown')
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data in database_tickets_keys)
def add_ticket_to_cart(query):
    if not is_opened_and_chose_the_right_month(query, select_customer_db_column_value(query, "MonthOfOrder")):
        return
    customer_cart = select_customer_db_column_value(query, "Cart")
    if not check_max_tickets_sold_to_1_user_per_month(query, True):
        bot.answer_callback_query(query.id, "Ти можеш замовити максимум 10 проїзних на 1 місяць", True)
        return
    awake_mysql_db()
    sql = "UPDATE customers SET Cart = %s WHERE User_Id = %s"
    val = (customer_cart + database_tickets.get(query.data), query.from_user.id)
    cursor.execute(sql, val)
    db.commit()
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=get_current_buy_menu_markup(query),
                          parse_mode='markdown')
    bot.answer_callback_query(query.id, "\"" + query.data + "\" додано до корзини")


@bot.callback_query_handler(lambda query: query.data == "buy")
def buy(query):
    month_of_order = select_customer_db_column_value(query, "MonthOfOrder")
    if not is_opened_and_chose_the_right_month(query, month_of_order):
        return
    customer_cart = select_customer_db_column_value(query, "Cart")
    if not customer_cart:
        bot.answer_callback_query(query.id, "Твоя корзина порожня. Вибери проїзні, які хочеш купити", True)
        return
    if not check_max_tickets_sold_to_1_user_per_month(query, False):
        bot.answer_callback_query(query.id, "Ти можеш замовити максимум 10 проїзних на 1 місяць", True)
        return
    price = 0
    description = ""
    for ticket in customer_cart:
        db_tickets_key = get_key_by_value(database_tickets_keys, ticket)
        tickets_key_split_name_amount_prise = db_tickets_key.split()
        tickets_key_split_name = tickets_key_split_name_amount_prise[0].split("-")
        # Take first letter in first word
        tickets_key_name = tickets_key_split_name[0][0]
        if len(tickets_key_split_name) == 2:
            # Take first letter in first word
            tickets_key_name += "-" + tickets_key_split_name[1][:3]
        tickets_key_name += \
            " " + tickets_key_split_name_amount_prise[1] + " " + tickets_key_split_name_amount_prise[2] + "грн"
        price += int(db_tickets_key.split()[2])
        description += "\n" + tickets_key_name
    bot.send_invoice(
        query.message.chat.id,
        "Season tickets",
        "Твоє замовлення на " + month_of_order + ":\n" + description + "\n",

        str(select_customer_db_column_value(query, "Customer_Id")) + " " + month_of_order + " " +
        select_customer_db_column_value(query, "Cart"),

        constants.payment_provider_token,
        "UAH",
        [telebot.types.LabeledPrice("Season tickets", price * 100)],
        "season-tickets",
        reply_markup=markup_invoice)
    bot.answer_callback_query(query.id)


@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(pre_checkout_query):
    if not is_opened_and_chose_the_right_month(pre_checkout_query,
                                               month_of_order=pre_checkout_query.invoice_payload.split()[1]):
        return
    if pre_checkout_query.from_user.id not in constants.customers_IDs:
        bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            False,
            "Помилка доступу - невідомий покупець. Деталі у останньому повідомленні")
        bot.send_message(pre_checkout_query.from_user.id,
                         "Схоже, ти купуєш проїзні у мене вперше. Я не можу продавати незнайомцям."
                         "\n\nЯкщо хочеш замовляти у мене, натисни " + italic("\"Відправити заявку\"") +
                         "Я зв'яжусь с тобою і ми узгодимо всі деталі: коли можна замовляти, чи зручно тобі "
                         "буде їх забирати у мене тощо."
                         "\n\nПотім бот додасть тебе в список покупців, повідомить тебе про це, і ти зможеш замовляти "
                         "у мене проїзні",
                         reply_markup=markup_user_requests_registration)
        return
    if not check_max_tickets_sold_to_1_user_per_month(
            pre_checkout_query,
            False,
            specified_customer_cart=pre_checkout_query.invoice_payload.split()[2]):
        bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            False,
            "Ти можеш замовити максимум 10 проїзних на 1 місяць")
        return
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Well... Looks like something went wrong. Please, contact me.")


@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    awake_mysql_db()
    old_order = select_customer_db_column_value(message, "Orders")
    customer_id = message.successful_payment.invoice_payload.split()[0]
    month_of_order = message.successful_payment.invoice_payload.split()[1]
    customer_cart = message.successful_payment.invoice_payload.split()[2]
    if month_of_order in old_order:
        month_order_old = get_customer_month_orders(month_of_order, query_or_message=message)
        new_order = old_order.replace(month_order_old, month_order_old + customer_cart)
    else:
        new_order = old_order + " " + month_of_order + customer_cart
    sql = "UPDATE customers SET Cart = %s, Orders = %s WHERE Customer_Id = %s"
    val = ("",
           new_order,
           customer_id)
    cursor.execute(sql, val)
    db.commit()
    bot.send_message(message.chat.id,
                     "Якщо потрбіно, в тебе ще є можливість дозамовити проїзні. \n(/buy)"
                     "\n\nЯкщо ти передумав (-ла) і хочеш скасувати замовлення проїзного (або проїзних) та повернути "
                     "гроші, напиши \n/refund")


@bot.callback_query_handler(lambda query: query.data == "remove_from_cart_menu")
def remove_from_cart_menu(query):
    if not is_opened_and_chose_the_right_month(query, select_customer_db_column_value(query, "MonthOfOrder")):
        return
    bot.edit_message_text("Вибери проїзні, які потрібно видалити з корзини",
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=generate_markup_remove_from_cart_or_refund_order_menu(query, cart_remove=True))
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data in [key + " remove_ticket" for key in database_tickets_keys])
def remove_ticket(query):
    if not is_opened_and_chose_the_right_month(query, select_customer_db_column_value(query, "MonthOfOrder")):
        return
    awake_mysql_db()
    old_cart = select_customer_db_column_value(query, "Cart")
    new_cart = old_cart.replace(database_tickets.get(query.data[:-14]), "", 1)
    if old_cart == new_cart:
        bot.answer_callback_query(query.id)
        return
    sql = "UPDATE customers SET Cart = %s WHERE User_Id = %s"
    val = (new_cart, query.from_user.id)
    cursor.execute(sql, val)
    db.commit()
    bot.edit_message_text("Вибери проїзні, які потрібно видалити з корзини",
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=generate_markup_remove_from_cart_or_refund_order_menu(query, cart_remove=True))
    bot.answer_callback_query(query.id, "\"" + query.data[:-14] + "грн\" видалено з корзини")


@bot.callback_query_handler(lambda query: query.data == "return_to_buy_menu")
def return_to_buy_menu(query):
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_1,
                          parse_mode='markdown')
    bot.answer_callback_query(query.id)


@bot.message_handler(commands=['refund'])
def handle_text(message):
    if not is_opened:
        bot.edit_message_text("Замовлення проїзних заверешено. Зміна замовлень неможлива",
                              chat_id=message.chat.id,
                              message_id=message.message_id)
        return
    words = message.text.split()
    if len(words) != 2:
        bot.send_message(message.chat.id,
                         "Неправильний формат"
                         "\nБудь ласка, напиши \"/refund [[номер твоєї картки]]\""
                         "\nНаприклад, \"/refund 5168424242424242\""
                         "\n" + bold("Будь уважний, адже саме на цю картку я перерахую твої гроші за проїзні!"),
                         parse_mode='markdown')
        return

    card_number = words[1]

    if not constants.card_number_pattern.match(card_number):
        bot.send_message(message.chat.id,
                         "Неправильний формат номера картки. Має бути 16 цифр"
                         "\nБудь ласка, напиши \"/refund [[номер твоєї картки]]\""
                         "\nНаприклад, \"/refund 5168424242424242\""
                         "\n" + bold("Будь уважний, адже саме на цю картку я перерахую твої гроші за проїзні!"),
                         parse_mode='markdown')
        return

    bot.send_message(message.chat.id,
                     "Вибери місяць, де ти хочеш скасувати замовлення проїзного або проїзних та повернути гроші на "
                     "картку " + bold(card_number),
                     reply_markup=generate_markup_choose_orders_month(refund_month=True),
                     parse_mode='markdown')


@bot.callback_query_handler(lambda query: query.data.startswith("refund choose month"))
def remove_ticket(query):
    month = query.data.split()[3]
    if month not in constants.months_for_which_tickets_can_be_ordered:
        bot.answer_callback_query(query.id, "Замовлення на цей місяць змінити не можна", True)
        return

    orders = get_customer_month_orders(month, query_or_message=query)
    if not orders:
        bot.answer_callback_query(query.id, "Твоє замовлення на {} порожнє".format(month), True)
        return

    awake_mysql_db()
    sql = "UPDATE customers SET OrdersAfterRefund = %s WHERE User_Id = %s"
    val = (orders, query.from_user.id)
    cursor.execute(sql, val)

    bot.edit_message_text("Спочатку вибери проїзні, які хочеш видалити з замовлення на " + bold(month) +
                          "\n\nПотім натисни " + italic("\"Видалити проїзні з замовлення\".") +
                          "\n\nКоли у мене буде час я перерахую кошти на твою картку " +
                          bold(query.message.text[-16:]) + " та повідомлю тебе про це",
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=generate_markup_remove_from_cart_or_refund_order_menu(
                              query, refund_order_remove=True),
                          parse_mode='markdown')

    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data in [key + " refund_ticket" for key in database_tickets_keys])
def remove_ticket(query):
    if not is_opened:
        bot.answer_callback_query(query.id, "Замовлення проїзних заверешено. Зміна замовлень неможлива", True)
        bot.edit_message_text("Замовлення проїзних заверешено. Зміна замовлень неможлива",
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id)
        return
    old_message = query.message.text
    split_old_message = old_message.split()
    if old_message.startswith("Спочатку"):
        month_of_order = split_old_message[9]
        card_number = split_old_message[27]
    else:
        month_of_order = split_old_message[2]
        card_number = split_old_message[5]
    if month_of_order not in constants.months_for_which_tickets_can_be_ordered:
        bot.answer_callback_query(query.id,
                                  "Неправильний місяць замовлення. Неможливо скасувати замовлення на {}".format(
                                      month_of_order),
                                  True)
        bot.edit_message_text("Спочатку вибери проїзні, які хочеш видалити з замовлення на " + bold(month_of_order) +
                              "\n\nПотім натисни " + italic("\"Видалити проїзні з замовлення\".") +
                              "\n\nКоли у мене буде час я перерахую кошти на твою картку " +
                              bold(card_number) + " та повідомлю тебе про це",
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id,
                              reply_markup=generate_markup_remove_from_cart_or_refund_order_menu(
                                  query, refund_order_remove=True),
                              parse_mode='markdown')
        return
    awake_mysql_db()
    old_orders_after_refund = select_customer_db_column_value(query, "OrdersAfterRefund")
    tickets_to_delete_from_order = query.data[:-14]
    new_orders_after_refund = old_orders_after_refund.replace(database_tickets.get(tickets_to_delete_from_order), "", 1)
    # If this ticket has already been deleted from the order
    if old_orders_after_refund != new_orders_after_refund:
        sql = "UPDATE customers SET OrdersAfterRefund = %s WHERE User_Id = %s"
        val = (new_orders_after_refund, query.from_user.id)
        cursor.execute(sql, val)
        db.commit()
    orders_of_month = get_customer_month_orders(month_of_order, query_or_message=query)
    for ticket in new_orders_after_refund:
        orders_of_month = orders_of_month.replace(ticket, "", 1)
    tickets_to_refund_message = ""
    tickets_to_refund_price = 0
    for ticket in orders_of_month:
        ticket = get_key_by_value(database_tickets_keys, ticket)
        tickets_to_refund_message += ticket + "\n"
        tickets_to_refund_price += int(ticket.split()[2])
    message = "Місяць замовлення: " + month_of_order + \
              "\n\nНомер картки: " + card_number + \
              "\n\nБуде видалено з замовлення: \n" + tickets_to_refund_message + \
              "\nБуде повернуто: " + str(tickets_to_refund_price) + "грн"
    bot.edit_message_text(message,
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=generate_markup_remove_from_cart_or_refund_order_menu(
                              query, refund_order_remove=True))
    bot.answer_callback_query(query.id, "\"" + tickets_to_delete_from_order + "грн\"")


@bot.callback_query_handler(lambda query: query.data == "user requests refund")
def user_requests_refund(query):
    if not is_opened:
        bot.answer_callback_query(query.id, "Замовлення проїзних заверешено. Зміна замовлень неможлива", True)
        bot.edit_message_text("Замовлення проїзних заверешено. Зміна замовлень неможлива",
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id)
        return
    old_message = query.message.text
    split_old_message = old_message.split()
    if old_message.startswith("Спочатку"):
        month_of_order = split_old_message[9]
        card_number = split_old_message[27]
    else:
        month_of_order = split_old_message[2]
        card_number = split_old_message[5]
    if month_of_order not in constants.months_for_which_tickets_can_be_ordered:
        bot.answer_callback_query(query.id,
                                  "Неправильний місяць замовлення. Неможливо скасувати замовлення на {}".format(
                                      month_of_order),
                                  True)
        bot.edit_message_text("Спочатку вибери проїзні, які хочеш видалити з замовлення на " + bold(month_of_order) +
                              "\n\nПотім натисни " + italic("\"Видалити проїзні з замовлення\".") +
                              "\n\nКоли у мене буде час я перерахую кошти на твою картку " +
                              bold(card_number) + " та повідомлю тебе про це",
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id,
                              reply_markup=generate_markup_remove_from_cart_or_refund_order_menu(
                                  query, refund_order_remove=True),
                              parse_mode='markdown')
        return
    if get_customer_month_orders(select_customer_db_column_value(query, "OrdersAfterRefund"), query_or_message=query) \
            == select_customer_db_column_value(query, "OrdersAfterRefund"):
        bot.answer_callback_query(query.id, "Ти не змінив замовлення", True)
        return
    month_orders_old = get_customer_month_orders(month_of_order, query_or_message=query)
    full_old_orders = select_customer_db_column_value(query, "Orders")
    month_orders_new = select_customer_db_column_value(query, "OrdersAfterRefund")
    if month_orders_new != "":
        new_orders = full_old_orders.replace(month_of_order + month_orders_old, month_of_order + month_orders_new)
    else:
        new_orders = full_old_orders.replace(month_of_order + month_orders_old, "").strip()
    if not new_orders == full_old_orders:
        awake_mysql_db()
        sql = "UPDATE customers SET Orders = %s WHERE User_Id = %s"
        val = (new_orders, query.from_user.id)
        cursor.execute(sql, val)
        db.commit()
        bot.send_message(constants.admin_id,
                         "#Refund " + str(datetime.date.today().strftime("%d.%m.%Y")) +
                         "\n\n" + get_username_or_first_name(query.message.chat.id, query.from_user.id) +
                         "\n\n" + query.message.text +
                         "\n\nId: " + str(query.from_user.id),
                         reply_markup=markup_admin_confirms_refund)
    # Sends user his new orders for this month -----------------------------------------------------------
    new_orders = get_customer_month_orders(month_of_order, query_or_message=query)
    description = ""
    if new_orders:
        for ticket in new_orders:
            db_tickets_key = get_key_by_value(database_tickets_keys, ticket)
            description += "\n" + db_tickets_key + "грн"
    else:
        description += "Порожнє"
    bot.edit_message_text("Твоє нове замовлення на " + month_of_order + ":\n" + description,
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id)
    bot.answer_callback_query(query.id)


@bot.message_handler(commands=['admin'])
def handle_text(message):
    if message.from_user.id == constants.admin_id:
        bot.send_message(message.chat.id, "Greetings, Admin", reply_markup=markup_admin)


@bot.message_handler(commands=['add_month'])
def handle_text(message):
    words = message.text.split()
    if len(words) != 2:
        bot.send_message(constants.admin_id, "Wrong format. "
                                             "\nPlease write add_month [month name]."
                                             "\nFor example, \"add_month September\"")
        return
    if words[1] in constants.months_for_which_tickets_can_be_ordered:
        bot.send_message(constants.admin_id, "This month is already present")
        return
    constants.months_for_which_tickets_can_be_ordered.append(words[1])
    bot.reply_to(message, "Added " + words[1])


@bot.callback_query_handler(lambda query: query.data == "admin confirms refund")
def admin_confirms_refund(query):
    # Remove reply_markup
    bot.edit_message_text(query.message.text,
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id)
    new_user_id = int(query.message.text.split()[-1])
    bot.send_message(new_user_id, "Відправив кошти, скоро мають прийти")
    bot.edit_message_text("Successful refund\n" + query.message.text,
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "open")
def open_form(query):
    global is_opened
    is_opened = True
    bot.answer_callback_query(query.id, "Opened")
    for customer_id in constants.customers_IDs:
        try:
            bot.send_message(customer_id, "Замовлення відкрито!")
        except telebot.apihelper.ApiException:
            # If user has blocked the bot
            constants.customers_IDs.remove(customer_id)


@bot.callback_query_handler(lambda query: query.data == "close")
def close_form(query):
    global is_opened
    is_opened = False
    awake_mysql_db()
    sql = "SELECT User_Id, Username from customers"
    val = ()
    cursor.execute(sql, val)
    result = cursor.fetchall()
    for month in constants.months_for_which_tickets_can_be_ordered:
        admin_final_order_for_month = {}
        for customer in result:
            customer_orders = {}
            user_id = customer[0]
            username = customer[1]
            orders = get_customer_month_orders(month, user_id=user_id)
            if not orders:
                continue
            for ticket in orders:
                # Fills 'admin_final_order_for_month' with season tickets that were ordered. Sums up which and how many
                # season tickets were ordered
                ticket_name = get_key_by_value(database_tickets_keys, ticket)
                if ticket_name in admin_final_order_for_month:
                    admin_final_order_for_month[ticket_name] = admin_final_order_for_month[ticket_name] + 1
                else:
                    admin_final_order_for_month[ticket_name] = 1
                # Fills 'customer_orders' with season tickets that were ordered by him/her
                ticket_name = get_key_by_value(database_tickets_keys, ticket)
                if ticket_name in customer_orders:
                    customer_orders[ticket_name] = customer_orders[ticket_name] + 1
                else:
                    customer_orders[ticket_name] = 1
            # Sends to each customer his/her 'customer_orders'. Duplicate the message to admin -------------------
            final_order_message = month + "\n\n" + username + "\n\n"
            for ticket_key in database_tickets_keys:
                if ticket_key in customer_orders:
                    final_order_message += ticket_key + "  ---  " + str(customer_orders[ticket_key]) + "\n"
            bot.send_message(constants.admin_id, final_order_message)
            bot.send_message(user_id, final_order_message)
        # Creates message based on 'admin_final_order_for_month' dict and sends it to admin. Sums up which and how many
        # season tickets were ordered
        final_order_message = month + " Final Order " + datetime.date.today().strftime("%d.%m.%Y") + "\n\n"
        for ticket_key in database_tickets_keys:
            if ticket_key in admin_final_order_for_month:
                final_order_message += ticket_key + "  ---  " + str(admin_final_order_for_month[ticket_key]) + "\n"
        bot.send_message(constants.admin_id, final_order_message)
    # Truncate Cart, Orders, OrdersAfterRefund, MonthOfOrder columns and months_for_which_tickets_can_be_ordered ---
    sql = "UPDATE customers SET Cart = %s, Orders = %s, OrdersAfterRefund = %s, MonthOfOrder = %s"
    val = ("", "", "", "")
    cursor.execute(sql, val)
    db.commit()
    constants.months_for_which_tickets_can_be_ordered.clear()
    # Answers callback query ---------------------------------------------------------------------------------------
    bot.answer_callback_query(query.id, "Closed")


@bot.callback_query_handler(lambda query: query.data == "user requests registration")
def user_requests_registration(query):
    bot.send_message(constants.admin_id, "#Register " + str(query.from_user.id) + "\n" + get_username_or_first_name(
        query.message.chat.id, query.from_user.id), reply_markup=markup_admin_confirms_user_registration)
    bot.answer_callback_query(query.id, "Чудово! Почекай, будь ласка, на мою відповідь", True)


@bot.callback_query_handler(lambda query: query.data == "admin confirms registration")
def admin_confirms_registration(query):
    id_of_new_user = int(query.message.text.split()[1])
    constants.customers_IDs.append(id_of_new_user)
    bot.send_message(id_of_new_user, "Вітаю, тепер ти можеш замовляти у мене проїзні :) Натисни /buy")
    bot.edit_message_text("Confirmed\n" + query.message.text,
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "admin rejects registration")
def admin_rejects_registration(query):
    id_of_new_user = int(query.message.text.split()[1])
    bot.send_message(id_of_new_user,
                     "Вибач, але я не можу продавати тобі проїзні :("
                     "\nЩоб дізнатися деталі, напиши мені в приватні повідомлення",
                     reply_markup=markup_contact_me)
    bot.edit_message_text("Rejected\n" + query.message.text,
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id)
    bot.answer_callback_query(query.id)


@bot.message_handler(commands=['start'])
def handle_text(message):
    if message.from_user.id not in constants.customers_IDs:
        bot.send_message(message.chat.id,
                         "Схоже, ти купуєш проїзні у мене вперше. Я не можу продавати незнайомцям."
                         "\n\nЯкщо хочеш замовляти у мене, натисни " + italic("\"Відправити заявку\"") +
                         "Я зв'яжусь с тобою і ми узгодимо всі деталі: коли можна замовляти, чи зручно тобі "
                         "буде їх забирати у мене тощо."
                         "\n\nПотім бот додасть тебе в список покупців, повідомить тебе про це, і ти зможеш замовляти "
                         "у мене проїзні",
                         reply_markup=markup_user_requests_registration)
    else:
        bot.send_message(message.chat.id, "Лінк на мій телеграм", reply_markup=markup_contact_me)
        bot.send_message(message.chat.id, "Напиши /buy, щоб замовити проїзний (проїзні)")


if __name__ == "__main__":
    app.run()
