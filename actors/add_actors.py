import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    first_name = input("Anna etunimi: ")
    last_name = input("Anna sukunimi: ")
    date_of_birth = input("Anna syntymäaika:(YYYY-MM-DD) ")

    query = ("INSERT INTO actors(first_name, last_name, date_of_birth) VALUES((%s), (%s), (%s));")
    cursor.execute(query, (first_name, last_name, date_of_birth))
    connection.commit()

    print("Lisätyn näyttelijän id on: ", cursor.lastrowid)


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()