import telebot.types
from database_data import *

# Buy menu sorted by first column
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
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("Видалити з корзини", callback_data="remove_from_cart_menu"))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("Купити", callback_data="buy"), )

# Buy menu sorted by second column
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
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("Видалити з корзини", callback_data="remove_from_cart_menu"))
markup_buy_menu_2.row(telebot.types.InlineKeyboardButton("Купити", callback_data="buy"), )

markup_invoice = telebot.types.InlineKeyboardMarkup()
markup_invoice.row(telebot.types.InlineKeyboardButton("Заплатити", pay=True))

markup_admin_confirms_refund = telebot.types.InlineKeyboardMarkup()
markup_admin_confirms_refund.row(telebot.types.InlineKeyboardButton("Done", callback_data="admin confirms refund"))

markup_user_requests_registration = telebot.types.InlineKeyboardMarkup()
markup_user_requests_registration.row(telebot.types.InlineKeyboardButton("Відправити заявку",
                                                                         callback_data="user requests registration"))
markup_user_requests_registration.row(telebot.types.InlineKeyboardButton("@TonyStarkZal",
                                                                         url="https://t.me/TonyStarkZal"))

markup_admin_confirms_user_registration = telebot.types.InlineKeyboardMarkup()
markup_admin_confirms_user_registration.row(
    telebot.types.InlineKeyboardButton("Ok", callback_data="admin confirms registration"))
markup_admin_confirms_user_registration.row(
    telebot.types.InlineKeyboardButton("Reject", callback_data="admin rejects registration"))

markup_contact_me = telebot.types.InlineKeyboardMarkup()
markup_contact_me.row(telebot.types.InlineKeyboardButton("@TonyStarkZal", url="https://t.me/TonyStarkZal"))

markup_admin = telebot.types.InlineKeyboardMarkup()
markup_admin.row(telebot.types.InlineKeyboardButton("Відкрити", callback_data="open"))
markup_admin.row(telebot.types.InlineKeyboardButton("Закрити", callback_data="close"))


def generate_markup_remove_from_cart_or_refund_order_menu(
        query_or_message, *, cart_remove=False, refund_order_remove=False):
    """
    :param query_or_message: used to get user id
    :param cart_remove: if True creates markup consisting of tickets in customer's CART or order
    :param refund_order_remove: if True creates markup consisting of tickets in customer's OrdersAfterRefund or order
    :return: keyboard markup consisting of tickets in customer's cart or order
    """
    markup_remove_from_cart_menu = telebot.types.InlineKeyboardMarkup()
    if cart_remove:
        customer_cart_or_order = select_customer_db_column_value(query_or_message, "Cart")
        callback_data_message = " remove_ticket"
        mark_up_last_row = telebot.types.InlineKeyboardButton("Назад", callback_data="return_to_buy_menu")
    elif refund_order_remove:
        customer_cart_or_order = select_customer_db_column_value(query_or_message, "OrdersAfterRefund")
        callback_data_message = " refund_ticket"
        mark_up_last_row = telebot.types.InlineKeyboardButton(
            "Видалити проїзні з замовлення", callback_data="user requests refund")
    else:
        raise ValueError("Either cart_remove or order_remove parameters must be specified")
    for ticket in customer_cart_or_order:
        this_ticket_db_key = get_key_by_value(database_tickets_keys, ticket)
        markup_remove_from_cart_menu.row(
            telebot.types.InlineKeyboardButton(this_ticket_db_key + "грн",
                                               callback_data=this_ticket_db_key + callback_data_message))
    markup_remove_from_cart_menu.row(mark_up_last_row)
    return markup_remove_from_cart_menu


def generate_markup_choose_orders_month(*, order_month=False, refund_month=False):
    """
    :param order_month: if True creates markup consisting of months on which it is possible to BUY season tickets
    :param refund_month: if True creates markup consisting of months on which it is possible to Refund season tickets
    :returns keyboard markup consisting of months on which it is possible to buy or refund season tickets
    """
    if order_month:
        callback_data_message = "buy choose month "
    elif refund_month:
        callback_data_message = "refund choose month "
    else:
        raise ValueError("Either month_of_order or month_of_refund parameters must be specified")
    markup_choose_month = telebot.types.InlineKeyboardMarkup()
    for month in constants.months_for_which_tickets_can_be_ordered:
        markup_choose_month.row(telebot.types.InlineKeyboardButton(month, callback_data=callback_data_message + month))
    return markup_choose_month


def get_current_buy_menu_markup(query):
    """
    Helps to get to know which buy_menu_markup the user uses (sorted by 1st or 2nd columns)
    Returns the current markup (sorted by 1st or 2nd columns) if it's the buy_menu_markup. Else returns None
    """
    json_markup = query.message.json.get('reply_markup').get('inline_keyboard')
    if json_markup[0][0]['text'] != "Сортувати за 1 колонкою":
        return markup_buy_menu_1
    elif json_markup[0][0]['text'] != "Сортувати за 2 колонкою":
        return markup_buy_menu_2
    else:
        return None
