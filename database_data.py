import constants

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


def get_key_by_value(dict_keys, value):
    return dict_keys[list(database_tickets.values()).index(value)]


def awake_mysql_db():
    """
    If there's no connection, creates one, else pings to wake up the connection
    """
    global db
    if db is None:
        db = constants.initialize_mysql()
    else:
        db.ping(True)


def select_customer_db_column_value(query_or_message, select_option):
    """
    Returns selected database column value of the user, which is specified by :param query_or_message
    :param query_or_message: used to get user id
    :param select_option: One of the following: "Customer_Id", "User_Id", "Username", "Cart", "Orders",
    "OrdersAfterRefund", "MonthOfOrder"
    :return: database value of the :param select_option
    """
    awake_mysql_db()
    sql = "SELECT {} FROM customers WHERE User_Id = %s".format(select_option)
    val = (query_or_message.from_user.id,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]


def get_customer_month_orders(month_of_order, *, query_or_message=None, user_id=None):
    """
    Returns customer's order for :param month_of_order in number format (database_tickets values).
    :param month_of_order: specifies the month of order that will be returned
    :param query_or_message: used to get user id. Use either this or :param user_id
    :param user_id: used to get user id. Use either this or :param query_or_message
    :return: customer's order in number format (database_tickets values).
    """
    awake_mysql_db()
    sql = "SELECT Orders FROM customers WHERE User_Id = %s"
    if query_or_message:
        val = (query_or_message.from_user.id,)
    elif user_id:
        val = (user_id,)
    else:
        raise ValueError("Either query_or_message or user_id parameters must be specified")
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if not result:
        return None
    orders = result[0][0]
    if not orders:
        return None
    months_orders = orders.split()
    for order in months_orders:
        if month_of_order in order:
            return order.replace(month_of_order, "")
