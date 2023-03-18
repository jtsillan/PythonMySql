import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    name = input("Anna itemin nimi: ")

    # Make query to get all items to compare to input
    check_query = ("SELECT items.*, item_types.item_type, age_limits.age_limit FROM items INNER JOIN item_types "
             "ON items.item_types_id = item_types.id INNER JOIN age_limits ON items.age_limits_id = age_limits.id WHERE items.name = (%s);")
    cursor.execute(check_query, (name, ))

    items = cursor.fetchall()

    # If item is not in database
    if items == []:
        print("Kohdetta ei löytynyt")

    # Item is found from database
    else:
        # Print all items
        for count, item in enumerate(items):
            print(f"({count}) Nimi: {item['name']}, Vuosi: {item['year']}, Tyyppi: {item['item_type']}, Kesto: {item['duration']} min, Ikäraja: {item['age_limit']}")

        choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")

        user_email = input("Anna käyttäjän sähköposti: ")

        # Make query and compare it to give email
        check_email_query = ("SELECT * FROM users WHERE email = (%s);")
        cursor.execute(check_email_query, (user_email, ))
        user = cursor.fetchall()

        if user == []:
            print("Sähköpostia ei löytynyt")
        else:
            item_id = items[int(choice)]['id']
            user_id = user[0]['id']
            
            # Delete given values from 'items_has_reviews' table
            delete_query = ("DELETE FROM items_has_reviews WHERE items_id = (%s) AND users_id = (%s);")
            cursor.execute(delete_query, (item_id, user_id))
            connection.commit()

            if cursor.rowcount == 0:
                print("Tiedoilla ei löytynyt arvostelua")

            elif cursor.rowcount == 1:
                print(f"Itemiltä '{items[int(choice)]['name']}' poistettu arvio.")

            else:
                print("Hups, joptain meni hassusti")


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()