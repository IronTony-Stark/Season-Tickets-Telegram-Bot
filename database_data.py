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


def awake_mysql_db():
    """
    If there's no connection, creates one, else pings to wake up the connection
    """
    global db
    if db is None:
        db = constants.initialize_mysql()
    else:
        db.ping(True)


def get_customer_order(query):
    """
    Returns customer's order in number format (database_tickets values).
    """
    awake_mysql_db()
    sql = "SELECT ORDERS FROM customers WHERE User_Id = %s"
    val = (query.from_user.id,)
    cursor.execute(sql, val)
    return cursor.fetchall()[0][0]