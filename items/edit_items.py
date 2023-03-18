import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    name = input("Anna muokattavan itemin nimi: ")

    check_query = ("SELECT items.*, item_types.item_type FROM items INNER JOIN item_types ON items.item_types_id = item_types.id WHERE items.name = (%s);")
    cursor.execute(check_query, (name, ))

    items = cursor.fetchall()

    if items == []:
        print("Kohdetta ei löytynyt")
    else:
        for count, item in enumerate(items):
            print(f"({count}) Nimi: {item['name']}, Vuosi: {item['year']}, Tyyppi: {item['item_type']}, Kesto: {item['duration']} min")

        choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")
        new_name = input("Anna uusi nimi: ")
        new_year = input("Anna uusi vuosiluku: ")
        new_duration = input("Anna uusi kestoaika: ")
        new_discription = input("Anna uusi kuvaus: ")

        # Make query and get all item_types
        cursor.execute("SELECT * FROM item_types GROUP BY id;")
        item_types = cursor.fetchall()

        # Print all item_types
        for item_type in item_types:
            print(f"{item_type['id']} {item_type['item_type']}")

        new_item_type = input("Anna uusi tuotetyyppi yllä olevista vaihtoehdoista: (1), (2), jne. ")

        # Make query to get all age_limits
        check_age_limits_query = ("SELECT * FROM age_limits;")
        cursor.execute(check_age_limits_query)
        age_limits = cursor.fetchall()

        # Print all age_limits
        for age_limit in age_limits:
            print(f"({age_limit['id']}) {age_limit['age_limit']}")

        new_age_limit = input("Anna uusi ikäraja yllä olevista vaihtoehdoista: (0), (1), jne ")
        item_id = items[int(choice)]['id']
        
        # Update query with given inputs
        edit_query = ("UPDATE items SET name = (%s), year = (%s), duration = (%s), discription = (%s), item_types_id = (%s), age_limits_id = (%s) WHERE id = (%s)")
        cursor.execute(edit_query, (new_name, new_year, new_duration, new_discription, new_item_type, new_age_limit, item_id))
        connection.commit()

        if cursor.rowcount == 1:
            print(f"Itemin '{name}' tiedot muutettu.")
            print(f"Uudet tiedot ovat: Nimi: {new_name}, Vuosi: {new_year}, Kesto: {new_duration} min, Ikäraja: {age_limits[int(new_age_limit)]['age_limit']} v")


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()