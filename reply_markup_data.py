import telebot.types
from database_data import database_tickets_keys

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
