import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    name = input("Anna itemin nimi: ")

    # Make query to get all items to compare to input
    check_items_query = ("SELECT items.*, item_types.item_type, age_limits.age_limit FROM items INNER JOIN item_types "
                "ON items.item_types_id = item_types.id INNER JOIN age_limits ON items.age_limits_id = age_limits.id WHERE items.name = (%s);")
    cursor.execute(check_items_query, (name, ))

    items = cursor.fetchall()

    # If item is not in database
    if items == []:
        print("Kohdetta ei löytynyt")

    else:
        for count, item in enumerate(items):
            print(f"({count}) Nimi: {item['name']}, Vuosi: {item['year']}, Tyyppi: {item['item_type']}, Kesto: {item['duration']} min, Ikäraja: {item['age_limit']} v")
        
        item_choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")
        item_id = items[int(item_choice)]['id']

        get_ites_has_actors_query = ("SELECT items_has_actors.*, actors.* FROM items_has_actors INNER JOIN actors ON items_has_actors.actors_id = actors.id WHERE items_has_actors.items_id = (%s);")
        cursor.execute(get_ites_has_actors_query, (item_id, ))
        items_in_actors = cursor.fetchall()

        if items_in_actors == []:
            print("Itemissä ei ole näyttelijöitä")
        else:
            for i in items_in_actors:
                print(i['first_name'], i['last_name'])



except mysql.connector.Error as err:
    print(err)

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()