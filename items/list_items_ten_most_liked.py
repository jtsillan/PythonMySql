import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    # Big up for Mr. Guru for fixing this query!
    query = ("SELECT items.*, item_types.*, AVG(review) AS avg_review FROM items INNER JOIN items_has_reviews ON"
             " items.id = items_has_reviews.items_id INNER JOIN reviews ON reviews.id = items_has_reviews.reviews_id INNER JOIN"
              " item_types ON items.item_types_id = item_types.id GROUP BY items.id, items.name, items.year ORDER BY avg_review DESC LIMIT 10;")    
    cursor.execute(query)
   
    items = cursor.fetchall()

    for item in items:
        print(f"Nimi: {item['name']}, Vuosi: {item['year']}, Tyyppi: {item['item_type']}, Arvostelu: {round(item['avg_review'], 1)} p")


except mysql.connector.Error as err:
    print(err)

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()