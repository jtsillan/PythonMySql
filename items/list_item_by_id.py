import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    _id = input("Anna itemin id: ")

    query = ("SELECT items.*, AVG(review) AS avg_review FROM items INNER JOIN items_has_reviews ON items.id = items_has_reviews.items_id INNER JOIN reviews ON reviews.id = items_has_reviews.reviews_id WHERE items.id = (%s);")
    cursor.execute(query, (_id, ))

    item = cursor.fetchone()

    if item is None:
        print("Kohdetta ei löytynyt")
    elif item['avg_review'] is None:
        print(f"Nimi: {item['name']}, Vuosi: {item['year']}, Kesto: {item['duration']} min")
        print("Itemillä ei ole arvostelua")
    else:
        print(f"Nimi: {item['name']}, Vuosi: {item['year']}, Kesto: {item['duration']} min, Arvostelu: {round(item['avg_review'], 1)} p")



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