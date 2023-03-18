import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    email = input("Anna sähköposti: ")
    first_name = input("Anna etunimi: ")
    last_name = input("Anna sukunimi: ")
    order_type = input("Valitse tilaustyyppi: (1) Standard, (2) Premium ")
    start_date = input("Anna alkamispäivä: (YYYY-MM-DD) ")

    order_query = ("INSERT INTO orders(start_date, order_type_id) VALUES((%s), (%s));")
    cursor.execute(order_query, (start_date, order_type))
    user_query = ("INSERT INTO users(email, first_name, last_name, orders_id) VALUES((%s), (%s), (%s), (%s));")
    cursor.execute(user_query, (email, first_name, last_name, cursor.lastrowid))
    connection.commit()

    print("Lisätyn käyttäjän id on: ", cursor.lastrowid)


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()