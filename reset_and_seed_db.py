import bcrypt
import mysql.connector
import os
import json

def reset_and_seed_db():
    file_name = "./sql/db_v2.sql"
    db_name = "tomasbudrikas10$mydb"
    if os.environ.get("mode") == "test":
        with open("config.json", 'r') as file:
            mysql_settings = json.load(file)
        cnx = mysql.connector.connect(
            host=mysql_settings["host"],
            port=mysql_settings["port"],
            user=mysql_settings["user"],
            password=mysql_settings["password"],
            database="test")
        file_name = "./sql/db_v2_test.sql"
        db_name = "tomasbudrikas10$test"
    elif os.environ.get("DATABASE_URL"):
        cnx = mysql.connector.connect(
            host=os.environ.get("DATABASE_URL"),
            port=os.environ.get("DATABASE_PORT"),
            user=os.environ.get("DATABASE_USER"),
            password=os.environ.get("DATABASE_PASSWORD")
        )
    else:
        with open("./config.json", 'r') as file:
            mysql_settings = json.load(file)
        cnx = mysql.connector.connect(
            host=mysql_settings["host"],
            port=mysql_settings["port"],
            user=mysql_settings["user"],
            password=mysql_settings["password"])


    with open(file_name) as file:
        cursor = cnx.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cnx.commit()
        for statement in file.read().split(';'):
            if statement.strip():
                cursor.execute(statement)
        cnx.commit()
        cursor.close()


    cursor = cnx.cursor()
    cursor.execute(f"USE {db_name}")
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

    add_atsiliepimai_query = ("INSERT INTO atsiliepimai"
             "(produktoId, vartotojoId, vertinimas)"
             "VALUES (%s, %s, %s)")

    add_vartotojai_query = ("INSERT INTO vartotojai"
             "(pavadinimas, slaptazodis, teises)"
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

        password = "abc1"
        passwordBytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(passwordBytes, salt)
        cursor.execute(add_vartotojai_query, ("Vartotojas A", hashedPassword, "user"))
        password = "abc2"
        passwordBytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(passwordBytes, salt)
        cursor.execute(add_vartotojai_query, ("Vartotojas B", hashedPassword, "company"))
        password = "abc3"
        passwordBytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(passwordBytes, salt)
        cursor.execute(add_vartotojai_query, ("Vartotojas C", hashedPassword, "admin"))
        cnx.commit()

        cursor.execute(add_atsiliepimai_query, (1, 1, 5))
        cursor.execute(add_atsiliepimai_query, (1, 2, 9))
        cursor.execute(add_atsiliepimai_query, (2, 2, 10))
        cursor.execute(add_atsiliepimai_query, (2, 3, 1))
        cursor.execute(add_atsiliepimai_query, (3, 3, 7))
        cursor.execute(add_atsiliepimai_query, (3, 1, 2))
        cnx.commit()

        print("worked")
        cursor.close()
        cnx.close()
    except Exception as e:
        print(e)
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    reset_and_seed_db()