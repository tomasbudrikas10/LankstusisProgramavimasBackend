import mysql.connector
cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="")


with open("./sql/db_v1.sql") as file:
    cursor = cnx.cursor()
    cursor.execute("DROP DATABASE IF EXISTS mydb")
    cnx.commit()
    for statement in file.read().split(';'):
        if statement.strip():
            cursor.execute(statement)
    cnx.commit()
    cursor.close()


cursor = cnx.cursor()
cursor.execute("USE mydb")
cnx.commit()

add_kategorija_query = ("INSERT INTO kategorijos"
         "(pavadinimas)"
         "VALUES (%s)")

add_produktas_query = ("INSERT INTO produktai"
         "(pavadinimas, aprasymas, paveiksliukas, gamintojas, produkto_puslapis)"
         "VALUES (%s, %s, %s, %s, %s)")

add_pasirinkimai_query = ("INSERT INTO pasirinkimai"
                          "(pavadinimas)"
                          "VALUES (%s)")

add_kategorijos_pasirinkimai_query = ("INSERT INTO kategorijospasirinkimai"
                                      "(kategorijosId, pasirinkimoId)"
                                      "VALUES (%s, %s)")

add_produkto_kategorijos_pasirinkimai_query = ("INSERT INTO produktokategorijosirpasirinkimai"
                                               "(produktoId, kategorijosId, pasirinkimoId)"
                                               "VALUES (%s, %s, %s)")

try:
    cursor.execute(add_kategorija_query, ("Kategorija A",))
    cursor.execute(add_kategorija_query, ("Kategorija B",))
    cursor.execute(add_kategorija_query, ("Kategorija C",))
    cursor.execute(add_kategorija_query, ("Kategorija D",))
    cursor.execute(add_kategorija_query, ("Kategorija E",))
    cnx.commit()

    cursor.execute(add_produktas_query, ("Produktas A", "Aprasymas A", "Paveiksliukas A", "Gamintojas A", "Produkto Puslapis A"))
    cursor.execute(add_produktas_query, ("Produktas B", "Aprasymas B", "Paveiksliukas B", "Gamintojas B", "Produkto Puslapis B"))
    cursor.execute(add_produktas_query, ("Produktas C", "Aprasymas C", "Paveiksliukas C", "Gamintojas C", "Produkto Puslapis C"))
    cursor.execute(add_produktas_query, ("Produktas D", "Aprasymas D", "Paveiksliukas D", "Gamintojas D", "Produkto Puslapis D"))
    cursor.execute(add_produktas_query, ("Produktas E", "Aprasymas E", "Paveiksliukas E", "Gamintojas E", "Produkto Puslapis E"))
    cnx.commit()

    cursor.execute(add_pasirinkimai_query, ("Pasirinkimas A",))
    cursor.execute(add_pasirinkimai_query, ("Pasirinkimas B",))
    cursor.execute(add_pasirinkimai_query, ("Pasirinkimas C",))
    cursor.execute(add_pasirinkimai_query, ("Pasirinkimas D",))
    cursor.execute(add_pasirinkimai_query, ("Pasirinkimas E",))
    cnx.commit()

    cursor.execute(add_kategorijos_pasirinkimai_query, (1, 1))
    cursor.execute(add_kategorijos_pasirinkimai_query, (1, 2))
    cursor.execute(add_kategorijos_pasirinkimai_query, (2, 3))
    cursor.execute(add_kategorijos_pasirinkimai_query, (2, 4))
    cursor.execute(add_kategorijos_pasirinkimai_query, (3, 5))
    cursor.execute(add_kategorijos_pasirinkimai_query, (3, 1))
    cursor.execute(add_kategorijos_pasirinkimai_query, (4, 2))
    cursor.execute(add_kategorijos_pasirinkimai_query, (4, 3))
    cursor.execute(add_kategorijos_pasirinkimai_query, (5, 4))
    cursor.execute(add_kategorijos_pasirinkimai_query, (5, 5))
    cnx.commit()

    cursor.execute(add_produkto_kategorijos_pasirinkimai_query, (1, 1, 1))
    cursor.execute(add_produkto_kategorijos_pasirinkimai_query, (1, 1, 2))
    cursor.execute(add_produkto_kategorijos_pasirinkimai_query, (2, 2, 3))
    cursor.execute(add_produkto_kategorijos_pasirinkimai_query, (2, 2, 4))
    cursor.execute(add_produkto_kategorijos_pasirinkimai_query, (3, 3, 5))
    cursor.execute(add_produkto_kategorijos_pasirinkimai_query, (3, 3, 1))
    cursor.execute(add_produkto_kategorijos_pasirinkimai_query, (4, 4, 2))
    cursor.execute(add_produkto_kategorijos_pasirinkimai_query, (4, 4, 3))
    cursor.execute(add_produkto_kategorijos_pasirinkimai_query, (5, 5, 4))
    cursor.execute(add_produkto_kategorijos_pasirinkimai_query, (5, 5, 5))
    cnx.commit()

    print("worked")
    cursor.close()
except Exception as e:
    print(e)
    cursor.close()
