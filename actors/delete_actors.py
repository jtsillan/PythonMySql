import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    first_name = input("Anna poistettavan näyttelijän etunimi: ")
    last_name = input("Anna poistettavan näyttelijän sukunimi: ")

    query = ("DELETE FROM actors WHERE first_name = (%s) AND last_name = (%s);")
    cursor.execute(query, (first_name, last_name))
    connection.commit()

    success = cursor.rowcount

    if success == 1:
        print(f"Näyttelijä {first_name} {last_name} poistettu")
    elif success == 0:
        print("Kohdetta ei löytynyt")


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()