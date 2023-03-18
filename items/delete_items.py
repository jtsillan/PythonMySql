import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    name = input("Anna poistettavan itemin nimi: ")

    check_query = ("SELECT items.*, item_types.item_type FROM items INNER JOIN item_types ON items.item_types_id = item_types.id WHERE items.name = (%s);")
    cursor.execute(check_query, (name, ))

    items = cursor.fetchall()

    if items == []:
        print("Kohdetta ei löytynyt")
    else:
        for count, item in enumerate(items):
            print(f"({count}) {item['name']}, {item['year']}, {item['item_type']}")

        choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")
        del_choice = items[int(choice)]['id']
        
        query = ("DELETE FROM items WHERE id = (%s);")
        cursor.execute(query, (del_choice, ))
        connection.commit()

        print(f"{cursor.rowcount} itemi poistettu")


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()