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
        new_item_type = input("Anna uusi tuotetyyppi: (1)Elokuva, (2)Videopeli, (3)Äänikirja: ")
        new_age_limit = input("Anna uusi ikäraja: (1)10, (2)12, (3)14, (4)16, (5)18: ")
        item_id = items[int(choice)]['id']
        
        edit_query = ("UPDATE items SET name = (%s), year = (%s), duration = (%s), discription = (%s), item_types_id = (%s), age_limits_id = (%s) WHERE id = (%s)")
        cursor.execute(edit_query, (new_name, new_year, new_duration, new_discription, new_item_type, new_age_limit, item_id))
        connection.commit()

        if cursor.rowcount == 1:
            print(f"Itemin {name} tiedot muutettu.")
            print(f"Uudet tiedot ovat: {new_name}, {new_year}, {new_duration}")


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()