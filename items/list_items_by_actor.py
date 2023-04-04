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

    # Actor is no in database
    if actors == []:
        print("Tiedoilla ei löytynyt henkilöä")
    
    # If actor is in database, show all matching given values
    else:
        for count, actor in enumerate(actors):
            print(f"({count}) Etunimi: {actor['first_name']}, Sukunimi: {actor['last_name']}, Ikä: {actor['age']}")

        choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")
        actor_id = actors[int(choice)]['id']

        query = ("SELECT * FROM items_has_actors INNER JOIN items ON items_has_actors.items_id = items.id INNER JOIN actors ON items_has_actors.actors_id = actors.id WHERE actors.id = (%s);")    
        cursor.execute(query, (actor_id, ))

        items = cursor.fetchall()

        if items == []:
            print("Itemiä ei löytynyt")

        else:
            for item in items:
                print(f"Nimi: {item['name']}, Vuosi: {item['year']}, Kesto: {item['duration']} min")


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


