import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    check_category_query = ("SELECT * FROM categories GROUP BY id;")
    cursor.execute(check_category_query)
    categories = cursor.fetchall()

    name = input("Anna lisättävän itemin nimi: ")
    year = input("Anna vuosiluku: ")
    duration = input("Anna kesto: ")
    discription = input("Anna kuvaus: ")
    type = input("Anna tyyppi: (1)Elokuva, (2)Videopeli, (3)Äänikirja: ")

    for category in categories:
        print(f"({category['id']}) {category['category']}")

    chosen_category = input("Valitse itemin kategoria yllä olevista vaihtoehdoista: (0), (1), jne ")

    check_age_limits_query = ("SELECT * FROM age_limits;")
    cursor.execute(check_age_limits_query)
    age_limits = cursor.fetchall()

    for age_limit in age_limits:
        print(f"({age_limit['id']}) {age_limit['age_limit']}")

    chosen_age_limit = input("Valitse itemin ikäraja yllä olevista vaihtoehdoista: (0), (1), jne ")

    item_query = ("INSERT INTO items(name, year, duration, discription, item_types_id, age_limits_id) VALUES((%s), (%s), (%s), (%s), (%s), (%s));")
    cursor.execute(item_query, (name, year, duration, discription, type, chosen_age_limit))
    print("Lisätyn itemin id on: ", cursor.lastrowid)
   
    item_id = cursor.lastrowid
    add_item_to_category_query = ("INSERT INTO items_has_categories(items_id, categories_id) VALUES((%s), (%s));")
    cursor.execute(add_item_to_category_query, (item_id, chosen_category))
    connection.commit()


except mysql.connector.Error as err:
    print(err)
    connection.rollback()

except Exception as e:
    print(e)

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()