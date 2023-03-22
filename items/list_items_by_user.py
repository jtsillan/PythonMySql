import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    email = input("Anna käyttäjän sähköposti: ")

    # Make query to get all items to compare to input
    check_user_query = ("SELECT * FROM users WHERE email = (%s);")
    cursor.execute(check_user_query, (email, ))

    user = cursor.fetchone()

    # If item is not in database
    if user is None:
        print("Kohdetta ei löytynyt")

    else:
        print(user['id'], user['first_name'], user['last_name'])
        user_choice = input("Valitse yllä olevista vaihtoehdoista: (1), (2) jne: ")

        get_user_has_items_query = ("SELECT * FROM users_has_items INNER JOIN items ON users_has_items.items_id = items.id WHERE users_has_items.users_id = (%s);")
        cursor.execute(get_user_has_items_query, (user_choice, ))
        items = cursor.fetchall()

        if items == []:
            print("Itemissä ei ole näyttelijöitä")
        else:
            for i in items:
                print(f"Nimi: {i['name']}, Vuosi: {i['year']}")



except mysql.connector.Error as err:
    print(err)

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()