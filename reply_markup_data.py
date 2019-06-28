import telebot.types
from database_data import *

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
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("Видалити з корзини", callback_data="remove_from_cart_menu"))
markup_buy_menu_1.row(telebot.types.InlineKeyboardButton("Купити", callback_data="buy"), )

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


def generate_markup_remove_from_cart_menu(query_or_message):
    """
    Returns keyboard markup consisting of tickets in customer's CART
    """
    markup_remove_from_cart_menu = telebot.types.InlineKeyboardMarkup()
    customer_cart = get_customer_cart(query_or_message)
    for ticket in customer_cart:
        this_ticket_db_key = get_key_by_value(database_tickets_keys, ticket)
        markup_remove_from_cart_menu.row(
            telebot.types.InlineKeyboardButton(this_ticket_db_key + "грн",
                                               callback_data=this_ticket_db_key + " remove_ticket"))
    markup_remove_from_cart_menu.row(
        telebot.types.InlineKeyboardButton("Назад", callback_data="return_to_buy_menu"))
    return markup_remove_from_cart_menu


def generate_markup_remove_from_order_menu(query_or_message):
    """
    Returns keyboard markup consisting of tickets in customer's ORDER
    """
    markup_remove_from_order_menu = telebot.types.InlineKeyboardMarkup()
    customer_order_after_refund = get_customer_orders_after_refund(query_or_message)
    for ticket in customer_order_after_refund:
        this_ticket_db_key = get_key_by_value(database_tickets_keys, ticket)
        markup_remove_from_order_menu.row(
            telebot.types.InlineKeyboardButton(this_ticket_db_key + "грн",
                                               callback_data=this_ticket_db_key + " refund_ticket"))
    markup_remove_from_order_menu.row(
        telebot.types.InlineKeyboardButton("Видалити проїзні з замовлення", callback_data="user requests refund"))
    return markup_remove_from_order_menu


def generate_markup_choose_orders_month():
    """
    Returns keyboard markup consisting of months on which it is possible to buy season tickets
    """
    markup_choose_orders_month = telebot.types.InlineKeyboardMarkup()
    for month in constants.months_for_which_tickets_can_be_ordered:
        markup_choose_orders_month.row(telebot.types.InlineKeyboardButton(month,
                                                                          callback_data="buy choose month " + month))
    return markup_choose_orders_month


def generate_markup_choose_refund_month():
    """
    Returns keyboard markup consisting of months on which it is possible to request a refund for season tickets
    """
    markup_choose_refund_month = telebot.types.InlineKeyboardMarkup()
    for month in constants.months_for_which_tickets_can_be_ordered:
        markup_choose_refund_month.row(telebot.types.InlineKeyboardButton(month,
                                                                          callback_data="refund choose month " + month))
    return markup_choose_refund_month


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
