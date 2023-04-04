import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    query = ("SELECT items.*, item_types.item_type, age_limits.age_limit FROM items INNER JOIN item_types "
             "ON items.item_types_id = item_types.id INNER JOIN age_limits ON items.age_limits_id = age_limits.id ORDER BY items.id;")    
    cursor.execute(query)
   
    items = cursor.fetchall()

    for item in items:
        print(f"Nimi: {item['name']}, Vuosi: {item['year']}, Tyyppi: {item['item_type']}, Kesto: {item['duration']} min, Ikäraja: {item['age_limit']} v")


except Exception as err:
    print(err)

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()