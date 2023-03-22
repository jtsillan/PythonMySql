import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    # TODO: fix query || NOT WORKING NOW!
    query = ("SELECT items_has_reviews.*, (SELECT AVG(review) FROM items_has_reviews INNER JOIN items ON items_has_reviews.items_id = items.id INNER JOIN"
             " reviews ON items_has_reviews.reviews_id = reviews.id WHERE items_has_reviews.items_id = items.id) AS avg_review FROM items_has_reviews INNER JOIN items ON items_has_reviews.items_id = items.id GROUP BY items.id ORDER BY avg_review DESC LIMIT 10;")    
    cursor.execute(query)
   
    items = cursor.fetchall()

    for item in items:
        print(item)
        #print(f"Nimi: {item['name']}, Vuosi: {item['year']}, Tyyppi: {item['item_type']}, Kesto: {item['duration']} min, Ikäraja: {item['age_limit']} v")


except mysql.connector.Error as err:
    print(err)

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()