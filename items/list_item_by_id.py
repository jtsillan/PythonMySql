import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    _id = input("Anna itemin id: ")

    # TODO: FIX QUERY || NOT WORKING NOW!
    query = ("SELECT * FROM items WHERE id IN (SELECT items_id FROM items_has_reviews WHERE items_id = (%s)) ORDER BY id")
    cursor.execute(query, (_id, ))

    item = cursor.fetchone()

    if item is None:
        print("Kohdetta ei löytynyt")
    else:
        print(item)
        #print(f"{item['name']}, {item['year']}, {item['item_type']}")



except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()