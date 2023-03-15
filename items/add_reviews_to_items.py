import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    name = input("Anna itemin nimi: ")

    check_query = ("SELECT items.*, item_types.item_type, age_limits.age_limit FROM items INNER JOIN item_types "
             "ON items.item_types_id = item_types.id INNER JOIN age_limits ON items.age_limits_id = age_limits.id WHERE items.name = (%s);")
    cursor.execute(check_query, (name, ))

    items = cursor.fetchall()

    if items == []:
        print("Kohdetta ei löytynyt")
    else:
        for count, item in enumerate(items):
            print(f"({count}) Nimi: {item['name']}, Vuosi: {item['year']}, Tyyppi: {item['item_type']}, Kesto: {item['duration']} min, Ikäraja: {item['age_limit']}")

        choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")
        review = input("Anna itemille arvostelu: (1)1p (2)1.5p (3)2p (4)2.5p (5)3p (6)3.5p (7)4p (8)4.5p (9)5p ")
        user_email = input("Anna käyttäjän sähköposti: ")
        check_email_query = ("SELECT * FROM users WHERE email = (%s)")
        cursor.execute(check_email_query, (user_email, ))
        user = cursor.fetchall()

        if user == []:
            print("Sähköpostia ei löytynyt")
        else:
            item_id = items[int(choice)]['id']
            user_id = user[0]['id']
            
            add_query = ("INSERT INTO items_has_reviews(items_id, reviews_id, users_id) VALUES((%s), (%s), (%s))")
            cursor.execute(add_query, (item_id, review, user_id ))
            connection.commit()

            if cursor.rowcount == 1:
                print(f"Itemille {name} annettu arvio.")


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()