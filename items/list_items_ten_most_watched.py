import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    # Query fixed, thanks to Mr. Guru again!
    query = ("SELECT *, item_types.item_type, COUNT(watch_count) AS num_watch FROM items INNER JOIN users_has_items ON items.id = users_has_items.items_id INNER JOIN"
             " users ON users_has_items.users_id = users.id INNER JOIN item_types ON items.item_types_id = item_types.id GROUP BY items.id ORDER BY watch_count DESC LIMIT 10;")    
    cursor.execute(query)
   
    items = cursor.fetchall()

    for item in items:
        print(f"Nimi: {item['name']}, Vuosi: {item['year']}, Tyyppi: {item['item_type']}, Näyttökerrat: {item['num_watch']}")


except mysql.connector.Error as err:
    print(err)

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()