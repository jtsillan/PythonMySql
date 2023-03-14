import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    email = input("Anna sähköposti: ")
    first_name = input("Anna etunimi: ")
    last_name = input("Anna sukunimi: ")

    query = ("INSERT INTO users(email, first_name, last_name) VALUES((%s), (%s), (%s));")
    cursor.execute(query, (email, first_name, last_name))
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