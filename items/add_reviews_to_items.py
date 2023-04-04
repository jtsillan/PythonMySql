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

        # Make query to get all reviews from database
        get_reviews_query = ("SELECT * FROM reviews;")
        cursor.execute(get_reviews_query)

        reviews = cursor.fetchall()
        
        for review in reviews:
            print(f"({review['id']}) {review['review']}")

        chosen_review = input("Valitse itemille arvostelu yllä olevista vaihtoehdoista: (1), (2), jne ")
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
            
            # Insert given values to 'items_has_reviews' table
            add_query = ("INSERT INTO items_has_reviews(items_id, reviews_id, users_id) VALUES((%s), (%s), (%s));")
            cursor.execute(add_query, (item_id, chosen_review, user_id, ))
            connection.commit()

            if cursor.rowcount == 1:
                print(f"Itemille '{items[int(choice)]['name']}' annettu arvio.")


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