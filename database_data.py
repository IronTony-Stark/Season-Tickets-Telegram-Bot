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


def get_customer_cart(query_or_message):
    """
    Returns customer's cart in number format (database_tickets values).
    """
    awake_mysql_db()
    sql = "SELECT Cart FROM customers WHERE User_Id = %s"
    val = (query_or_message.from_user.id,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]


def get_customer_orders(query_or_message, month_of_order=None):
    """
    Returns customer's orders in number format (database_tickets values).
    """
    awake_mysql_db()
    sql = "SELECT Orders FROM customers WHERE User_Id = %s"
    val = (query_or_message.from_user.id,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if not result:
        return None
    orders = result[0][0]
    if not orders:
        return None
    if not month_of_order:
        month_of_order = get_month_of_order(query_or_message)
    months_orders = orders.split()
    for order in months_orders:
        if month_of_order in order:
            return order.replace(month_of_order, "")


def get_customer_orders_by_user_id(user_id, month_of_order):
    """
    Returns customer's orders in number format (database_tickets values) using user id.
    """
    awake_mysql_db()
    sql = "SELECT Orders FROM customers WHERE User_Id = %s"
    val = (user_id,)
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


def get_full_customer_orders(query_or_message):
    """
    Returns customer's orders in number format (database_tickets values).
    """
    awake_mysql_db()
    sql = "SELECT Orders FROM customers WHERE User_Id = %s"
    val = (query_or_message.from_user.id,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]


def get_customer_orders_after_refund(query_or_message):
    """
    Returns customer's orders after the refund in number format (database_tickets values).
    """
    awake_mysql_db()
    sql = "SELECT OrdersAfterRefund FROM customers WHERE User_Id = %s"
    val = (query_or_message.from_user.id,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]


def get_month_of_order(query_or_message):
    """
    Returns the month on which the user orders season tickets
    """
    awake_mysql_db()
    sql = "SELECT MonthOfOrder FROM customers WHERE User_Id = %s"
    val = (query_or_message.from_user.id,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]


def get_customer_id(query_or_message):
    """
    Returns database id of the user
    """
    awake_mysql_db()
    sql = "SELECT Customer_Id FROM customers WHERE User_Id = %s"
    val = (query_or_message.from_user.id,)
    cursor.execute(sql, val)
    return cursor.fetchall()[0][0]
