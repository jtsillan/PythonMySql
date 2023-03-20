import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    _id = input("Anna näyttelijän id: ")

    query = ("SELECT actors.*, TIMESTAMPDIFF(YEAR, date_of_birth, NOW()) AS age FROM actors WHERE id = (%s);")    
    cursor.execute(query, (_id, ))
   
    actor = cursor.fetchone()

    if actor is None:
        print("Tiedoilla ei löytynyt näyttelijää")

    else:
        print(f"Nimi: {actor['first_name']} {actor['last_name']}, Ikä: {actor['age']} v")


except mysql.connector.Error as err:
    print(err)

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()