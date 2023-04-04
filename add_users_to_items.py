import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    user_email = input("Anna käyttäjän sähköposti: ")

    # Make query and compare it to give email
    check_email_query = ("SELECT * FROM users WHERE email = (%s);")
    cursor.execute(check_email_query, (user_email, ))
    user = cursor.fetchone()

    if user is None:
        print("Sähköpostia ei löytynyt")

    else:        
        name = input("Anna itemin nimi: ")

        # Make query to get all items to compare to input
        check_items_query = ("SELECT items.*, item_types.item_type, age_limits.age_limit FROM items INNER JOIN item_types "
                    "ON items.item_types_id = item_types.id INNER JOIN age_limits ON items.age_limits_id = age_limits.id WHERE items.name = (%s);")
        cursor.execute(check_items_query, (name, ))

        items = cursor.fetchall()

        # If item is not in database
        if items == []:
            print("Kohdetta ei löytynyt")

        # Item found from database
        else:
            # Print all items
            for count, item in enumerate(items):
                print(f"({count}) Nimi: {item['name']}, Vuosi: {item['year']}, Tyyppi: {item['item_type']}, Kesto: {item['duration']} min, Ikäraja: {item['age_limit']}")

            choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")
            
            item_id = items[int(choice)]['id']
            user_id = user['id']

            check_query = ("SELECT * FROM users_has_items WHERE users_id = (%s) AND items_id = (%s)")
            cursor.execute(check_query, (user_id, item_id))
            user_item = cursor.fetchone()


            if user_item is None:        

                add_user_to_items_query = ("INSERT INTO users_has_items(users_id, items_id, watch_count) VALUES((%s), (%s), (%s));")
                cursor.execute(add_user_to_items_query, (user_id, item_id, 1))
                connection.commit()
                print("Katsojaluku lisätty.")

            else:
                watch_count = user_item['watch_count']

                if watch_count != 0:
                    update_query = ("UPDATE users_has_items SET watch_count = (%s) WHERE users_id = (%s) AND items_id = (%s);")
                    cursor.execute(update_query, (watch_count + 1, user_id, item_id))
                    connection.commit()
                    print("Katsojaluku päivitetty.")
                    


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

except Exception as e:
    print(e)

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()