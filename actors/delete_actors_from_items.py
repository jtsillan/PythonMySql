import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    first_name = input("Anna näyttelijän etunimi: ")
    last_name = input("Anna näyttelijän sukunimi: ")

    query = ("SELECT *, TIMESTAMPDIFF(YEAR, date_of_birth, NOW()) AS age FROM actors WHERE first_name = (%s) AND last_name = (%s);")
    cursor.execute(query, (first_name, last_name))
    actors = cursor.fetchall()

    # Actor is not in database
    if actors == []:
        print("Tiedoilla ei löytynyt henkilöä")
    
    # If actor is in database, show all matching given values
    else:
        for count, actor in enumerate(actors):
            print(f"({count}) Etunimi: {actor['first_name']}, Sukunimi: {actor['last_name']}, Ikä: {actor['age']}")

        choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")
        item = input("Mistä itemistä haluat poistaa näyttelijän? ")
        actor_id = actors[int(choice)]['id']

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


            delete_query = ("DELETE FROM items_has_actors WHERE items_id = (%s) AND actors_id = (%s)")
            cursor.execute(delete_query, (item_id, actor_id))

            connection.commit()                    

            if cursor.rowcount == 1:
                print(f"Näyttelijä {first_name} {last_name} poistettu itemistä.")


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()


