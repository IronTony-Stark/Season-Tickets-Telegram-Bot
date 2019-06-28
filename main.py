from reply_markup_data import *
from database_data import *
import telebot
import flask
import mysql.connector
import datetime
from flask import Flask
# from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)
bot = telebot.TeleBot(constants.bot_token, threaded=False)
is_opened = True


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
    month_of_order = "Місяць замовлення: " + get_month_of_order(query)
    if description:
        message_text = month_of_order + "\n\nКорзина: \n" + description + "\n\nЗагальна вартість: " + str(
            price) + " грн"
    else:
        message_text = month_of_order + \
                       "\n\nСпочатку вибери проїзний або проїзні, які хочеш замовити. Їх буде додано до корзини" \
                       "\n\nПотім натисни 'Купити' та оплати замовлення" \
                       "\n\nЯкщо потрібно видалити з корзини проїзний або проїзні, натисни 'Видалити з корзини'."
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


@bot.message_handler(commands=['buy'])
def handle_text(message):
    if not is_opened:
        bot.reply_to(message, "Замовлення проїзних заверешено. Зміна замовлень неможлива")
        return
    bot.send_message(message.chat.id,
                     "Вибери місяць, на який будеш замовляти проїзний (проїзні)",
                     reply_markup=generate_markup_choose_orders_month())


@bot.callback_query_handler(lambda query: query.data.startswith("buy choose month"))
def choose_month(query):
    current_month = query.data.split()[3]
    if current_month not in constants.months_for_which_tickets_can_be_ordered:
        bot.answer_callback_query(query.id, "Неправильний місяць замовлення", True)
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
    orders_month = "Місяць замовлення: " + get_month_of_order(query)
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_1)
    bot.answer_callback_query(query.id, orders_month)


@bot.callback_query_handler(lambda query: query.data == "Sort by 1st column")
def buy_menu_sorted_by_1_column(query):
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_1)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "Sort by 2nd column")
def buy_menu_sorted_by_2_column(query):
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_2)
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data in database_tickets_keys)
def add_ticket_to_cart(query):
    if not is_opened:
        bot.answer_callback_query(query.id, "Замовлення проїзних заверешено. Зміна замовлень неможлива", True)
        return
    awake_mysql_db()
    customer_cart = get_customer_cart(query)
    # ---------------------------------------------------------------------------------------------------------
    customer_order = get_customer_orders(query)
    if not customer_cart:
        customer_cart_length = 0
    else:
        customer_cart_length = len(customer_cart)
    if not customer_order:
        customer_order_length = 0
    else:
        customer_order_length = len(customer_order)
    if customer_cart_length + customer_order_length == constants.max_tickets_sold_to_1_user_per_month:
        bot.answer_callback_query(query.id,
                                  "Вибач, але ти можеш замовити максимум {} проїзних на 1 місяць"
                                  .format(str(constants.max_tickets_sold_to_1_user_per_month)),
                                  True)
        return
    # ---------------------------------------------------------------------------------------------------------
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
    if not is_opened:
        bot.answer_callback_query(query.id, "Замовлення проїзних заверешено. Зміна замовлень неможлива", True)
        return
    description, price = get_cart_description_and_total_price(query)
    if not description:
        bot.answer_callback_query(query.id, "Твоя корзина порожня. Вибери проїзні, які хочеш купити", True)
        return
    bot.send_invoice(query.message.chat.id,
                     "Season tickets",
                     "Твоє замовлення на " + get_month_of_order(query) + ":\n" + description + "\n",
                     str(get_customer_id(query)) + " " + get_month_of_order(query) + " " + get_customer_cart(query),
                     constants.payment_provider_token,
                     "UAH",
                     [telebot.types.LabeledPrice("Season tickets", price * 100)],
                     "test-payment",
                     reply_markup=markup_invoice)
    bot.answer_callback_query(query.id)


@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(pre_checkout_query):
    if not is_opened:
        bot.answer_callback_query(pre_checkout_query.id,
                                  "Замовлення проїзних заверешено. Зміна замовлень неможлива", True)
        return
    if pre_checkout_query.from_user.id not in constants.customers_IDs:
        bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            False,
            "Помилка доступу - невідомий покупець. Деталі у останньому повідомленні")
        bot.send_message(pre_checkout_query.from_user.id,
                         "Схоже, ти купуєш проїзні у мене вперше. Я не можу продавати незнайомцям. "
                         "\n\nЯкщо хочеш замовляти у мене, натисни \"Відправити заявку\" Я зв'яжусь с тобою і ми "
                         "узгодимо всі деталі: коли можна замовляти, чи зручно тобі буде їх забирати у мене тощо. "
                         "\n\nПотім бот додасть тебе в список покупців, повідомить тебе про це, і ти зможеш замовляти "
                         "у мене проїзні",
                         reply_markup=markup_user_requests_registration)
        return
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Well... Looks like something went wrong. Please, contact me.")


@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    awake_mysql_db()
    old_order = get_full_customer_orders(message)
    month_of_order = get_month_of_order(message)
    if month_of_order in old_order:
        month_order_old = get_customer_orders(message, message.successful_payment.invoice_payload.split()[1])
        new_order = old_order.replace(month_order_old, month_order_old +
                                      message.successful_payment.invoice_payload.split()[2])
    else:
        new_order = old_order + " " + month_of_order + message.successful_payment.invoice_payload.split()[2]
    sql = "UPDATE customers SET Cart = %s, Orders = %s WHERE Customer_Id = %s"
    val = ("",
           new_order,
           message.successful_payment.invoice_payload.split()[0])
    cursor.execute(sql, val)
    db.commit()
    bot.send_message(message.chat.id,
                     "Якщо потрбіно, в тебе ще є можливість дозамовити проїзні. \n(/buy)"
                     "\n\nЯкщо ти передумав (-ла) і хочеш скасувати замовлення проїзного (або проїзних) та повернути "
                     "гроші, напиши \n/refund")


@bot.callback_query_handler(lambda query: query.data == "remove_from_cart_menu")
def remove_from_cart_menu(query):
    if not is_opened:
        bot.answer_callback_query(query.id, "Замовлення проїзних заверешено. Зміна замовлень неможлива", True)
        return
    bot.edit_message_text("Вибери проїзні, які потрібно видалити з корзини",
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=generate_markup_remove_from_cart_menu(query))
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data in [key + " remove_ticket" for key in database_tickets_keys])
def remove_ticket(query):
    if not is_opened:
        bot.answer_callback_query(query.id, "Замовлення проїзних заверешено. Зміна замовлень неможлива", True)
        return
    awake_mysql_db()
    old_cart = get_customer_cart(query)
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
                          reply_markup=generate_markup_remove_from_cart_menu(query))
    bot.answer_callback_query(query.id, "\"" + query.data[:-14] + "грн\" видалено з корзини")


@bot.callback_query_handler(lambda query: query.data == "return_to_buy_menu")
def return_to_buy_menu(query):
    bot.edit_message_text(get_updated_cart_description_and_total_price_message(query),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=markup_buy_menu_1)
    bot.answer_callback_query(query.id)


@bot.message_handler(commands=['refund'])
def handle_text(message):
    if not is_opened:
        bot.reply_to(message, "Замовлення проїзних заверешено. Зміна замовлень неможлива")
        return
    words = message.text.split()
    if len(words) != 2:
        bot.send_message(message.chat.id, "Неправильний формат"
                                          "\nБудь ласка, напиши \"/refund [номер твоєї картки]\""
                                          "\nБудь уважний, адже саме на цю картку я перерахую твої гроші за проїзні!"
                                          "\nНаприклад, \"/refund 5168424242424242\"")
        return

    card_number = words[1]

    if not constants.card_number_pattern.match(card_number):
        bot.send_message(message.chat.id, "Неправильний формат номера картки. Має бути 16 цифр"
                                          "\nБудь ласка, напиши \"/refund [номер твоєї картки]\""
                                          "\nБудь уважний, адже саме на цю картку я перерахую твої гроші за проїзні!"
                                          "\nНаприклад, \"/refund 5168424242424242\"")
        return

    bot.send_message(message.chat.id,
                     "Вибери місяць, де ти хочеш скасувати замовлення проїзного або проїзних та повернути гроші на "
                     "картку " + card_number,
                     reply_markup=generate_markup_choose_refund_month())


@bot.callback_query_handler(lambda query: query.data.startswith("refund choose month"))
def remove_ticket(query):
    month = query.data.split()[3]
    if month not in constants.months_for_which_tickets_can_be_ordered:
        bot.answer_callback_query(query.id, "Замовлення на цей місяць змінити не можна", True)
        return

    orders = get_customer_orders(query, month)
    if not orders:
        bot.answer_callback_query(query.id, "Твоє замовлення на {} порожнє".format(month), True)
        return

    awake_mysql_db()
    sql = "UPDATE customers SET OrdersAfterRefund = %s WHERE User_Id = %s"
    val = (orders, query.from_user.id)
    cursor.execute(sql, val)

    bot.send_message(query.message.chat.id,
                     "Спочатку вибери проїзні, які хочеш видалити з замовлення на " + month +
                     "\n\nПотім натисни \"Видалити проїзні з "
                     "замовлення.\" \n\nКоли у мене буде час я перерахую кошти на твою картку " +
                     query.message.text[-16:] +
                     " та повідомлю тебе про це",
                     reply_markup=generate_markup_remove_from_order_menu(query))

    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data in [key + " refund_ticket" for key in database_tickets_keys])
def remove_ticket(query):
    if not is_opened:
        bot.answer_callback_query(query.id, "Замовлення проїзних заверешено. Зміна замовлень неможлива", True)
        return
    awake_mysql_db()
    old_orders_after_refund = get_customer_orders_after_refund(query)
    new_orders_after_refund = old_orders_after_refund.replace(database_tickets.get(query.data[:-14]), "", 1)
    # If this ticket has already been deleted from the order
    if old_orders_after_refund == new_orders_after_refund:
        bot.edit_message_text(query.message.text,
                              chat_id=query.message.chat.id,
                              message_id=query.message.message_id,
                              reply_markup=generate_markup_remove_from_order_menu(query))
        bot.answer_callback_query(query.id)
        return
    sql = "UPDATE customers SET OrdersAfterRefund = %s WHERE User_Id = %s"
    val = (new_orders_after_refund, query.from_user.id)
    cursor.execute(sql, val)
    db.commit()
    old_message = query.message.text
    split_old_message = old_message.split()
    deleted_ticket = query.data[:-14]
    deleted_ticket_price = deleted_ticket.split()[2]
    if old_message.startswith("Спочатку"):
        new_message = "Місяць замовлення: " + split_old_message[9] + \
                      "\n\nНомер картки: " + split_old_message[27] + \
                      "\n\nБуде видалено з замовлення: \n" + deleted_ticket + \
                      "\n\nБуде повернуто: " + deleted_ticket_price + "грн"
    else:
        refund_money = int(old_message.split("Буде повернуто: ")[1].replace("грн", "").strip()) + \
                       int(deleted_ticket_price)
        new_message = old_message.split("\nБуде повернуто: ")[0] + deleted_ticket + "\n\nБуде повернуто: " + str(
            refund_money) + "грн"
    bot.edit_message_text(new_message,
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=generate_markup_remove_from_order_menu(query))
    bot.answer_callback_query(query.id, "\"" + deleted_ticket + "грн\"")


@bot.callback_query_handler(lambda query: query.data == "user requests refund")
def user_requests_refund(query):
    if not is_opened:
        bot.answer_callback_query(query.id, "Замовлення проїзних заверешено. Зміна замовлень неможлива", True)
        return
    if get_customer_orders(query) == get_customer_orders_after_refund(query):
        bot.answer_callback_query(query.id, "Ти не змінив замовлення", True)
        return
    month = query.message.text.split()[2]
    month_orders_old = get_customer_orders(query, month)
    full_old_orders = get_full_customer_orders(query)
    month_orders_new = get_customer_orders_after_refund(query)
    new_orders = full_old_orders.replace(month + month_orders_old, month + month_orders_new)
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
    new_orders = get_customer_orders(query, month)
    description = ""
    for ticket in new_orders:
        db_tickets_key = get_key_by_value(database_tickets_keys, ticket)
        description += "\n" + db_tickets_key + "грн"
    bot.edit_message_text("Твоє нове замовлення на " + month + ":\n" + description,
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
            # If the user has blocked the bot
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
            orders = get_customer_orders_by_user_id(user_id, month)
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
    bot.answer_callback_query(query.id)


@bot.callback_query_handler(lambda query: query.data == "admin rejects registration")
def admin_rejects_registration(query):
    id_of_new_user = int(query.message.text.split()[1])
    bot.send_message(id_of_new_user,
                     "Вибач, але я не можу продавати тобі проїзні :("
                     "\nЩоб дізнатися деталі, напиши мені в приватні повідомлення",
                     reply_markup=markup_contact_me)
    bot.answer_callback_query(query.id)


@bot.message_handler(commands=['start'])
def handle_text(message):
    if message.from_user.id not in constants.customers_IDs:
        bot.send_message(message.chat.id,
                         "Схоже, ти купуєш проїзні у мене вперше. Я не можу продавати незнайомцям. "
                         "\n\nЯкщо хочеш замовляти у мене, натисни \"Відправити заявку\" Я зв'яжусь с тобою і ми "
                         "узгодимо всі деталі: коли можна замовляти, чи зручно тобі буде їх забирати у мене тощо. "
                         "\n\nПотім бот додасть тебе в список покупців, повідомить тебе про це, і ти зможеш замовляти "
                         "у мене проїзні",
                         reply_markup=markup_user_requests_registration)
    else:
        bot.send_message(message.chat.id, "Лінк на мій телеграм", reply_markup=markup_contact_me)
        bot.send_message(message.chat.id, "Напиши /buy, щоб замовити проїзний (проїзні)")


if __name__ == "__main__":
    app.run()
