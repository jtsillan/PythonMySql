import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    name = input("Anna lisättävän itemin nimi: ")
    year = input("Anna vuosiluku: ")
    duration = input("Anna kesto: ")
    discription = input("Anna kuvaus: ")
    type = input("Anna tyyppi: (1)Elokuva, (2)Videopeli, (3)Äänikirja: ")
    age_limit = input("Anna ikäraja: (1)10, (2)12, (3)14, (4)16, (5)18: ")

    query = ("INSERT INTO items(name, year, duration, discription, item_types_id, age_limits_id) VALUES((%s), (%s), (%s), (%s), (%s), (%s))")
    cursor.execute(query, (name, year, duration, discription, type, age_limit))
    connection.commit()

    print("Lisätyn itemin id on: ", cursor.lastrowid)

except mysql.connector.Error as err:
    print(err)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()