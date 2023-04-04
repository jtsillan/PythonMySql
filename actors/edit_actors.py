import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    first_name = input("Anna muokattavan näyttelijän etunimi: ")
    last_name = input("Anna muokattavan näyttelijän sukunimi: ")

    query = ("SELECT * FROM actors WHERE first_name = (%s) AND last_name = (%s);")
    cursor.execute(query, (first_name, last_name))
    actors = cursor.fetchall()

    # Actor is not in database
    if actors == []:
        print("Tiedoilla ei löytynyt henkilöä")
    
    # If actor is in database, show all matching values
    else:
        for count, actor in enumerate(actors):
            print(f"({count}) Etunimi: {actor['first_name']}, Sukunimi: {actor['last_name']}, Syntymäaika: {actor['date_of_birth']}")

        choice = input("Valitse yllä olevista vaihtoehdoista: (0), (1), jne: ")
        edited_first_name = input("Anna uusi etunimi: ")
        edited_last_name = input("Anna uusi sukunimi: ")
        edited_date_of_birth = input("Anna uusi syntymäaika: ")

        actor_id = actors[int(choice)]['id']
        edit_query = ("UPDATE actors SET first_name = (%s), last_name = (%s), date_of_birth = (%s) WHERE id = (%s)")
        cursor.execute(edit_query, (edited_first_name, edited_last_name, edited_date_of_birth, actor_id))
        connection.commit()

        success = cursor.rowcount

        if success == 1:
            print(f"Näyttelijä {first_name} {last_name} tiedot muutettu.")
            print(f"Uudet tiedot: etunimi: {edited_first_name}, sukunimi: {edited_last_name}, syntymäaika: {edited_date_of_birth}")
        else:
            print("Ei onnistunut")
           

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