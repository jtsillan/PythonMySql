import mysql.connector

connection = None
cursor = None

def add_actor_to_item(actor_id):
    item = input("Mihin itemiin haluat lisätä näyttelijän? ")

    query = ("SELECT items.*, item_types.item_type, age_limits.age_limit FROM items INNER JOIN item_types "
            "ON items.item_types_id = item_types.id INNER JOIN age_limits ON items.age_limits_id = age_limits.id WHERE items.name = (%s) ORDER BY items.id;")    
    cursor.execute(query, (item, ))

    items = cursor.fetchall()

    if items == []:
        print("Itemiä ei löytynyt")

    else:
        for count, item in enumerate(items):
            print(f"({count}) Nimi: {item['name']}, Vuosi: {item['year']}, Tyyppi: {item['item_type']}, Kesto: {item['duration']} min, Ikäraja: {item['age_limit']} v")
        
        item_choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")
        item_id = items[int(item_choice)]['id']
        add_query = (f"INSERT INTO items_has_actors(items_id, actors_id) VALUES({item_id}, {actor_id})")
        cursor.execute(add_query)
        connection.commit()
        print("Tiedot lisätty riville: ",cursor.lastrowid)


try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    first_name = input("Anna näyttelijän etunimi: ")
    last_name = input("Anna näyttelijän sukunimi: ")

    query = ("SELECT *, TIMESTAMPDIFF(YEAR, date_of_birth, NOW()) AS age FROM actors WHERE first_name = (%s) AND last_name = (%s);")
    cursor.execute(query, (first_name, last_name))
    actors = cursor.fetchall()

    # If actor is not in database, create new 
    if actors == []:
        print("Tiedoilla ei löytynyt henkilöä")
        # date_of_birth = input("Anna syntymäaika (YYYY-MM-YY): ")
        # insert_query = ("INSERT INTO actors(first_name, last_name, date_of_birth) VALUES((%s), (%s), (%s));")
        # cursor.execute(insert_query, (first_name, last_name, date_of_birth))
        # connection.commit()
        # print("Lisätyn näyttelijän id on: ", cursor.lastrowid)

        # add_actor_to_item(cursor.lastrowid)
    
    # If actor is in database, show all matching given values
    else:
        for count, actor in enumerate(actors):
            print(f"({count}) Etunimi: {actor['first_name']}, Sukunimi: {actor['last_name']}, Ikä: {actor['age']}")

        choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")
        add_choice = actors[int(choice)]['id']

        add_actor_to_item(add_choice)


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()


