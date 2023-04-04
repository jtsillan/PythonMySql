import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='suunnittelutehtava3')
    cursor = connection.cursor(dictionary=True, prepared=True)

    first_name = input("Anna etunimi: ")
    last_name = input("Anna sukunimi: ")
    date_of_birth = input("Anna syntymäaika:(YYYY-MM-DD) ")

    query = ("INSERT INTO actors(first_name, last_name, date_of_birth) VALUES((%s), (%s), (%s));")
    cursor.execute(query, (first_name, last_name, date_of_birth))
    connection.commit()

    print("Lisätyn näyttelijän id on: ", cursor.lastrowid)

# PALAUTE
# tästä en sakoita, koska olet seurannut minun esimerkkiä aj minun tekemistä virheistä en anna miinusta.
# mutta jatkossa on hyvä muistaa, että tämä excepct mysql.connector.Error lohko ottaa kiinni vaan yhidsämisessä tapahtuvat virheet
# (jos esim tietokannan nimi olisi väärin, tai tietokantapalvelin pois päältä)
# kaikki muut virheet, jotka voivat tapahtua, mutta eivät oel tietokannan yhdistysvirheitä, jäävät käsittelemättä
# jos haluat olla laiska käytä except Exception as e, jotta saat kaikki virheet kiinni
# tai sitten laita useampi except-lohko allekkain eri virhetyypeille


except mysql.connector.Error as e:
    print(e)
    connection.rollback()

finally:
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()