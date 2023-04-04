import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    category = input("Anna kategorian nimi: ")

    check_category_query = ("SELECT * FROM categories WHERE category = (%s);")
    cursor.execute(check_category_query, (category, ))

    categories = cursor.fetchone()
    # PALAUTE
    # tämän rivin pitäisi olla vasta elsessä, koska jos categoriaa ei ole, siltä ei löydy id-saraketta
    category_id = categories['id']

    if categories is None:
        print("Kategoriaa ei löytynyt")
    else:        
        category_id = categories['id']     
        query = ("SELECT items_has_categories.*, items.*, categories.* FROM items_has_categories INNER JOIN items "
                "ON items_has_categories.items_id = items.id INNER JOIN categories ON items_has_categories.categories_id = categories.id WHERE items_has_categories.categories_id = (%s);")    
        cursor.execute(query, (category_id, ))
    
        items = cursor.fetchall()

        if items == []:
            print("Kategoriassa ei ollut itemeitä")
        else:
            for item in items:
                print(f"Nimi: {item['name']}, Vuosi: {item['year']}, Kesto: {item['duration']} min")


except mysql.connector.Error as err:
    print(err)

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()